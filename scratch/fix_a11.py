import os
import re

base_dir = "/home/randy/Workspace/REPOS/libn/src"

def replace_in_file(rel_path, replacements):
    filepath = os.path.join(base_dir, rel_path)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        content = f.read()
    
    for old, new in replacements:
        if callable(new):
            content = new(content)
        else:
            content = content.replace(old, new)
            
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {rel_path}")

# 1. mmap.npk
def fix_mmap(c):
    c = c.replace("pub fixed int64:ALLOC_HEADER_SIZE = 24i64;", 
                  "pub fixed int64:ALLOC_HEADER_SIZE = 24i64;\npub fixed int64:ALLOC_MAP_SIZE_OFFSET  = 8i64;\npub fixed int64:ALLOC_USER_SIZE_OFFSET = 16i64;")
    
    # mem_malloc
    c = c.replace("""    hdr[0] = 0x4D4D415000000000i64;
    hdr[1] = total;
    hdr[2] = size;  // map_size + magic at offset 0
    hdr[1] = n;      // user_size at offset 8
    
    // Return pointer past the header.
    pass map_start + ALLOC_HEADER_SIZE;""", """    hdr[0] = 0x4D4D415000000000i64; // Magic
    hdr[1] = total;                 // Map size
    hdr[2] = n;                     // User size

    // Return pointer past the header.
    pass(map_start + ALLOC_HEADER_SIZE);""")
    
    c = c.replace("""    hdr[0] = 0x4D4D415000000000i64;
    hdr[1] = total;
    hdr[2] = size;  // map_size + magic at offset 0
    hdr[1] = n;      // user_size at offset 8

    // Return pointer past the header.
    pass map_start + ALLOC_HEADER_SIZE;""", """    hdr[0] = 0x4D4D415000000000i64; // Magic
    hdr[1] = total;                 // Map size
    hdr[2] = n;                     // User size

    // Return pointer past the header.
    pass(map_start + ALLOC_HEADER_SIZE);""")
    
    c = c.replace("""    int64:map_start = r.val;
    int64->:hdr = map_start => int64->;
    hdr[0] = 0x4D4D415000000000i64;
    hdr[1] = total;
    hdr[2] = size;  // map_size + magic at offset 0
    hdr[1] = n;      // user_size at offset 8""", """    int64:map_start = r.val;
    int64->:hdr = map_start => int64->;
    hdr[0] = 0x4D4D415000000000i64; // Magic
    hdr[1] = total;                 // Map size
    hdr[2] = n;                     // User size""")
    c = c.replace("pass map_start + ALLOC_HEADER_SIZE;", "pass(map_start + ALLOC_HEADER_SIZE);")

    # mem_realloc
    c = c.replace("""    int64:old_map_size  = hdr[0] & 0x00000000FFFFFFFFi64;
    int64:old_user_size = hdr[1];""", """    if hdr[0] != 0x4D4D415000000000i64 { fail(ERR_BADARG => tbb8); }
    int64:old_map_size  = hdr[1];
    int64:old_user_size = hdr[2];""")
    
    c = c.replace("""        new_hdr[0] = new_total | 0x4D4D415000000000i64;
        new_hdr[1] = new_size;""", """        new_hdr[0] = 0x4D4D415000000000i64;
        new_hdr[1] = new_total;
        new_hdr[2] = new_size;""")
        
    c = c.replace("pass new_map + ALLOC_HEADER_SIZE;", "pass(new_map + ALLOC_HEADER_SIZE);")
    c = c.replace("pass new_ptr;", "pass(new_ptr);")

    # mem_free
    c = c.replace("""    int64:map_size = hdr[0] & 0x00000000FFFFFFFFi64;

    if map_size <= 0i64 {
        // Corrupted header — likely double-free or invalid pointer
        fail(ERR_BADARG => tbb8);
    }

    // Scrub the header to detect double-free in debug builds
    // (In release builds, this is elided by the compiler as a dead write.)
    hdr[0] = 0i64;
    hdr[1] = 0i64;""", """    if hdr[0] != 0x4D4D415000000000i64 { fail(ERR_BADARG => tbb8); }
    int64:map_size = hdr[1];

    if map_size <= 0i64 {
        // Corrupted header — likely double-free or invalid pointer
        fail(ERR_BADARG => tbb8);
    }

    // Scrub the header to detect double-free in debug builds
    // (In release builds, this is elided by the compiler as a dead write.)
    hdr[0] = 0i64; hdr[1] = 0i64; hdr[2] = 0i64; // Scrub header""")

    # accessors
    c = c.replace("""    int64->:hdr = (ptr - ALLOC_HEADER_SIZE) => int64->;
    pass hdr[1];""", """    int64->:hdr = (ptr - ALLOC_HEADER_SIZE) => int64->;
    pass(hdr[2]);""")
    
    c = c.replace("""    int64->:hdr = (ptr - ALLOC_HEADER_SIZE) => int64->;
    pass(hdr[0] & 0x00000000FFFFFFFFi64);""", """    int64->:hdr = (ptr - ALLOC_HEADER_SIZE) => int64->;
    pass(hdr[1]);""")

    # Nested Results
    c = c.replace("Result<int64>:r = libn_mmap(addr, length, prot, flags, fd, offset);\n    pass r;", "return libn_mmap(addr, length, prot, flags, fd, offset);")
    c = c.replace("Result<int64>:r = libn_munmap(addr, length);\n    pass r;", "return libn_munmap(addr, length);")
    c = c.replace("Result<int64>:r = libn_mprotect(addr, length, prot);\n    pass r;", "return libn_mprotect(addr, length, prot);")
    c = c.replace("Result<int64>:r = libn_mremap(old_addr, old_size, new_size, flags, new_addr);\n    pass r;", "return libn_mremap(old_addr, old_size, new_size, flags, new_addr);")
    c = c.replace("Result<int64>:r = libn_madvise(addr, length, advice);\n    pass r;", "return libn_madvise(addr, length, advice);")
    c = c.replace("Result<int64>:r = libn_msync(addr, length, flags);\n    pass r;", "return libn_msync(addr, length, flags);")

    c = c.replace("Result<int64>:r = mem_malloc(total_bytes);\n    pass r;", "return mem_malloc(total_bytes);")
    
    c = c.replace("Result<int64>:r = libn_mmap(0i64, size, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    pass r;", "Result<int64>:r = libn_mmap(0i64, size, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    pass(r.val);")
    c = c.replace("Result<int64>:r = libn_munmap(addr, size);\n    pass r;", "Result<int64>:r = libn_munmap(addr, size);\n    pass(r.val);")
    c = c.replace("Result<int64>:r = libn_munmap(base, total_size);\n    pass r;", "Result<int64>:r = libn_munmap(base, total_size);\n    pass(r.val);")
    
    c = c.replace("fail new_r.err;", "fail(new_r.err);")

    return c

replace_in_file("mem/mmap.npk", [("pass", fix_mmap)])

# 2. mem/slab.npk
def fix_slab(c):
    c = c.replace("""    if (ptr & 4095i64) == 16i64 {
        if (ptr - 16i64 => int64->)[0] == 0x4D4D415000000000i64 {
            return mem_free(ptr);
        }
    }""", """    if (ptr & 4095i64) == 24i64 {
        int64->:hdr64 = (ptr - 24i64) => int64->;
        if hdr64[0] == 0x4D4D415000000000i64 {
            return mem_free(ptr);
        }
    }""")
    c = c.replace("pass(mem_malloc(n));", "return mem_malloc(n);")
    c = c.replace("pass(mem_free(ptr));", "return mem_free(ptr);")
    c = c.replace("int64:ptr = r;", "int64:ptr = r.val;")
    return c

replace_in_file("mem/slab.npk", [("pass", fix_slab)])

# 3. io/open.npk
def fix_io_open(c):
    c = c.replace("pass(r);", "pass(r.val);")
    return c

replace_in_file("io/open.npk", [("pass", fix_io_open)])

# 3. io/printf.npk
def fix_io_printf(c):
    c = c.replace("if r.is_error { pass(r); }", "if r.is_error { fail(r.err); }")
    c = c.replace('": " => int64', '@": "[0] => int64')
    return c

replace_in_file("io/printf.npk", [("pass", fix_io_printf)])

# 3. io/write.npk
def fix_io_write(c):
    c = c.replace("if r.is_error { pass(r); }", "if r.is_error { fail(r.err); }")
    return c

replace_in_file("io/write.npk", [("pass", fix_io_write)])

# 3. str/strview.npk
def fix_str_strview(c):
    c = c.replace("""    Result<int64>:r = str_parse_i64(buf);
    _?mem_free(buf);
    pass(r);""", """    Result<int64>:r = str_parse_i64(buf);
    _?mem_free(buf);
    if r.is_error { fail(r.err); }
    pass(r.val);""")
    c = c.replace("""    Result<int64>:r = str_parse_u64(buf);
    _?mem_free(buf);
    pass(r);""", """    Result<int64>:r = str_parse_u64(buf);
    _?mem_free(buf);
    if r.is_error { fail(r.err); }
    pass(r.val);""")
    
    # Missing unwraps in strview.npk
    c = re.sub(r'(?<!_!)(mem_memcmp\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(mem_memchr\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(mem_memrchr\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(mem_memmem\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(str_strlen\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(fwrite\()', r'_!\1', c)
    return c

replace_in_file("str/strview.npk", [("pass", fix_str_strview)])

# 4. exec.npk
def fix_exec(c):
    c = c.replace('"/usr/local/bin/" => int64', '@"/usr/local/bin/"[0] => int64')
    c = c.replace('"/usr/bin/" => int64', '@"/usr/bin/"[0] => int64')
    c = c.replace('"/bin/" => int64', '@"/bin/"[0] => int64')
    c = c.replace('"/usr/sbin/" => int64', '@"/usr/sbin/"[0] => int64')
    c = c.replace('"/sbin/" => int64', '@"/sbin/"[0] => int64')
    c = c.replace('"PATH" => int64', '@"PATH"[0] => int64')
    return c
replace_in_file("proc/exec.npk", [("pass", fix_exec)])

# 4. tmpfile.npk
def fix_tmpfile(c):
    c = c.replace('"w+b" => int64', '@"w+b"[0] => int64')
    return c
replace_in_file("io/bio/tmpfile.npk", [("pass", fix_tmpfile)])

# 4. strfmt.npk
def fix_strfmt(c):
    c = c.replace("raw fmt_putc", "_?fmt_putc")
    c = c.replace("raw fmt_pad", "_?fmt_pad")
    c = c.replace("raw fmt_puts_n", "_?fmt_puts_n")
    c = c.replace("raw render_uint", "_!render_uint")
    c = c.replace("raw str_strlen", "_!str_strlen")
    c = c.replace("raw str_format_args", "_!str_format_args")
    return c
replace_in_file("str/strfmt.npk", [("pass", fix_strfmt)])

# 4. strcpy.npk
def fix_strcpy(c):
    c = c.replace("raw str_strlen", "_!str_strlen")
    c = c.replace("raw str_strnlen", "_!str_strnlen")
    c = c.replace("raw str_strscpy", "_!str_strscpy")
    return c
replace_in_file("str/strcpy.npk", [("pass", fix_strcpy)])

# 4. strcmp.npk
def fix_strcmp(c):
    c = c.replace("raw to_lower_ascii", "_!to_lower_ascii")
    return c
replace_in_file("str/strcmp.npk", [("pass", fix_strcmp)])

# 4. wait.npk
def fix_wait(c):
    c = c.replace("if _!wait_signaled(status) { pass(128i64 + wait_termsig(status)); }", "if _!wait_signaled(status) { pass(128i64 + _!wait_termsig(status)); }")
    c = c.replace("if wait_signaled(status) { pass(128i64 + wait_termsig(status)); }", "if _!wait_signaled(status) { pass(128i64 + _!wait_termsig(status)); }")
    c = c.replace("return _!waitpid(", "return waitpid(")
    return c
replace_in_file("proc/wait.npk", [("pass", fix_wait)])

# 4. fscanf.npk
def fix_fscanf(c):
    # Missing unwraps
    c = re.sub(r'(?<!_!)(?<!_)(bio_scan_getc\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(?<!_)(bio_scan_ungetc\()', r'_?\1', c)
    c = re.sub(r'(?<!_!)(?<!_)(bio_scan_skip_ws\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(?<!_)(bio_scan_int\()', r'_!\1', c)
    c = re.sub(r'(?<!_!)(?<!_)(bio_scan_str\()', r'_!\1', c)
    
    # Check if width is checked for %s
    if 'if width == 0i64 && out != 0i64' not in c:
        c = c.replace("if spec == 115u8 {", "if spec == 115u8 {\n            if width == 0i64 && out != 0i64 { fail(ERR_BADARG => tbb8); }")
    return c
replace_in_file("io/bio/fscanf.npk", [("pass", fix_fscanf)])

# 4. path.npk
def fix_path(c):
    c = c.replace("fail ENAMETOOLONG => tbb8;", "fail(ENAMETOOLONG => tbb8);")
    c = c.replace("pass blen;", "pass(blen);")
    return c
replace_in_file("fs/path.npk", [("pass", fix_path)])

# 4. seek.npk
def fix_seek(c):
    c = c.replace("fail saved.err;", "fail(saved.err);")
    c = c.replace("fail end_pos.err;", "fail(end_pos.err);")
    return c
replace_in_file("io/seek.npk", [("pass", fix_seek)])

# 4. fio.npk
def fix_fio(c):
    c = c.replace("pass bytes_written / size;", "pass(bytes_written / size);")
    c = c.replace("""        if buf_space == 0i64 {
            Result<int64>:r = bio_flush_write_buf(fp);
            if r.is_error { f->flags = f->flags | FILE_FLAG_ERROR; break; }
            continue;
        }""", """        if buf_space == 0i64 {
            Result<int64>:r = bio_flush_write_buf(fp);
            if r.is_error {
                f->flags = f->flags | FILE_FLAG_ERROR;
                break;
            }
            continue;
        }""")
    return c
replace_in_file("io/bio/fio.npk", [("pass", fix_fio)])

# 4. memset.npk
def fix_memset(c):
    c = c.replace('_?asm!!!<int64>("x86_64", "", "~{memory}");', 'int64:_fence = asm!!!<int64>("x86_64", "", "~{memory}");')
    return c
replace_in_file("mem/memset.npk", [("pass", fix_memset)])

# 5. env.npk
def fix_env(c):
    if "int64:old_ptr = ep[i];" not in c:
        c = c.replace("""        if match && es[nlen] == 61u8 {
            ep[i] = entry;
            pass(0i64);
        }""", """        if match && es[nlen] == 61u8 {
            int64:old_ptr = ep[i];
            ep[i] = entry;
            _?mem_free(old_ptr);
            pass(0i64);
        }""")
    return c
replace_in_file("proc/env.npk", [("pass", fix_env)])

# 6. memutil.npk
def fix_memutil(c):
    c = c.replace("while i < n && (((a + i) | (b + i)) & 7i64) != 0i64 {", "while i < n && ((a + i) & 7i64) != 0i64 {")
    return c
replace_in_file("mem/memutil.npk", [("pass", fix_memutil)])

# 6. strconv.npk
def fix_strconv(c):
    if "int64:max_digit = INT64_MAX % base;" not in c:
        c = c.replace("""        int64:limit = INT64_MAX / base;
        if result > limit {""", """        int64:limit = INT64_MAX / base;
        int64:max_digit = INT64_MAX % base;
        if negative { max_digit = max_digit + 1i64; } // |INT64_MIN| is 1 higher

        if result > limit || (result == limit && dv > max_digit) {""")

    c = c.replace("""        result = result * base + dv;""", """        int64:new_res = result * base + dv;
        if _!math_max_u64(new_res, result) != new_res {
            overflow = true;
            break;
        }
        result = new_res;""")
    return c
replace_in_file("str/strconv.npk", [("pass", fix_strconv)])

# 6. strlcpy.npk
def fix_strlcpy(c):
    # Only replace the last `pass(0i64);` in `str_strscpy`
    return c.replace("pass(0i64);\n}", "pass(i);\n}")
replace_in_file("str/strlcpy.npk", [("pass", fix_strlcpy)])

print("A11 changes applied.")
