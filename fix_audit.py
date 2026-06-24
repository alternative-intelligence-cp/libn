import os
import re

def rewrite(path, func):
    if not os.path.exists(path): return
    with open(path, "r") as f:
        content = f.read()
    content = func(content)
    with open(path, "w") as f:
        f.write(content)

# Phase 1.1: memcpy.npk and memset.npk
def fix_requires(content):
    content = content.replace("requires dst != 0i64 requires src != 0i64", "requires dst != 0i64 && src != 0i64")
    content = content.replace("requires dst != 0i64 requires", "requires dst != 0i64 &&")
    return content
rewrite("src/mem/memcpy.npk", fix_requires)

# Phase 1.3: raw unwraps
def fix_mmap(c):
    c = c.replace("int64:total = page_align_up", "int64:total = raw page_align_up")
    c = c.replace("int64:new_total = page_align_up", "int64:new_total = raw page_align_up")
    return c
rewrite("src/mem/mmap.npk", fix_mmap)

def fix_slab(c):
    c = c.replace("int64:slot_full = slab_class_size", "int64:slot_full = raw slab_class_size")
    return c
rewrite("src/mem/slab.npk", fix_slab)

def fix_fopen(c):
    c = c.replace("int64:parse_ok = bio_parse_mode", "int64:parse_ok = raw bio_parse_mode")
    c = c.replace("int64:fp = bio_alloc_file", "int64:fp = raw bio_alloc_file")
    return c
rewrite("src/io/bio/fopen.npk", fix_fopen)

def fix_tmpfile(c):
    c = c.replace("int64:fd = mkstemp", "int64:fd = raw mkstemp")
    c = c.replace("int64:entropy = tmpfile_get_entropy", "int64:entropy = raw tmpfile_get_entropy")
    # Phase 1.7: string literal pointer mismatch
    c = c.replace('fixed int64:hex = @"0123456789abcdef";', 'fixed int64:hex = @cast_unchecked<int64>(@"0123456789abcdef");')
    return c
rewrite("src/io/bio/tmpfile.npk", fix_tmpfile)

# Phase 1.4: Pointer Member Access (. vs ->)
# In strbuf.npk and strview.npk
def fix_ptr_access(c):
    c = c.replace("s.cap", "s->cap")
    c = c.replace("s.len", "s->len")
    c = c.replace("s.ptr", "s->ptr")
    c = c.replace("sv.len", "sv->len")
    c = c.replace("sv.ptr", "sv->ptr")
    c = c.replace("o.ptr", "o->ptr")
    c = c.replace("o.len", "o->len")
    c = c.replace("i.len", "i->len")
    return c
rewrite("src/str/strbuf.npk", fix_ptr_access)
rewrite("src/str/strview.npk", fix_ptr_access)
rewrite("src/str/strtok.npk", fix_ptr_access)

# Phase 1.6: Invalid raw on ternary
def fix_fscanf(c):
    c = c.replace("int64:max = raw is (width > 0i64) : width : 4096i64;", "int64:max = is (width > 0i64) : width : 4096i64;")
    return c
rewrite("src/io/bio/fscanf.npk", fix_fscanf)

# Phase 1.8: Inline Assembly
def fix_signal(c):
    c = c.replace('asm!!!<int64>("x86_64", "mov rax, 15\\nsyscall", "")', 'asm!!!<int64>("x86_64", "movq $15, %rax\\n\\tsyscall", "")')
    return c
rewrite("src/proc/signal.npk", fix_signal)

# Phase 2.1: fprintf stack buffer overread
def fix_fprintf(c):
    for i in range(9):
        snprintf = f"str_snprintf{i}"
        # we find "int64:len = str_snprintf" or "raw str_snprintf" and replace the block
        # Actually let's just do a regex
        c = re.sub(
            r'int64:len = (?:raw )?str_snprintf' + str(i) + r'\(tmp_ptr, 4096i64,([^\)]+)\);\s*'
            r'Result<int64>:alloc_r = mem_malloc\(len \+ 1i64\);\s*'
            r'if \(alloc_r.is_error\) \{ pass 0i64; \}\s*'
            r'int64:p = alloc_r.value;\s*'
            r'drop\(mem_memcpy\(p, tmp_ptr, len \+ 1i64\)\);\s*'
            r'\(@cast_unchecked<uint8->>\(p\) \+ len\)\[0\] = 0u8;',
            
            f'int64:len = raw str_snprintf{i}(tmp_ptr, 4096i64,\\1);\n'
            f'    int64:actual_len = is (len > 4095i64) : 4095i64 : len;\n'
            f'    Result<int64>:alloc_r = mem_malloc(actual_len + 1i64);\n'
            f'    if (alloc_r.is_error) {{ pass 0i64; }}\n'
            f'    int64:p = alloc_r.value;\n'
            f'    drop(mem_memcpy(p, tmp_ptr, actual_len));\n'
            f'    (@cast_unchecked<uint8->>(p))[actual_len] = 0u8;',
            c
        )
    return c
rewrite("src/io/bio/fprintf.npk", fix_fprintf)

# Phase 2.2 & 2.5: Use-After-Free and Memory Leak in fopen.npk
def fix_fopen_uaf(c):
    unlink_logic = """    if (g_open_files == fp) {
        g_open_files = f->next_global;
    } else {
        int64:curr = g_open_files;
        while (curr != 0i64) {
            FILE->:curr_f = @cast_unchecked<FILE->>(curr);
            if (curr_f->next_global == fp) {
                curr_f->next_global = f->next_global;
                break;
            }
            curr = curr_f->next_global;
        }
    }"""
    # Replace bio_free_file(fp) in fclose
    if "drop(bio_free_file(fp));" in c:
        c = c.replace("drop(bio_free_file(fp));", unlink_logic + "\n    drop(bio_free_file(fp));", 1) # Only first one is in fclose?
        # Actually let's just do it securely
    
    # In freopen:
    if "f->fd = -1i64;\n        pass 0i64;" in c:
        c = c.replace("f->fd = -1i64;\n        pass 0i64;", f"f->fd = -1i64;\n{unlink_logic}\n        drop(bio_free_file(fp));\n        pass 0i64;")
    return c
rewrite("src/io/bio/fopen.npk", fix_fopen_uaf)

# Phase 2.3: Unsigned Integer Parse Corruption
def fix_strconv(c):
    # This is tricky without seeing the code, but the audit says:
    # Cast variables to uint64 and execute purely in 64-bit unsigned space.
    # Let's read strconv.npk first, we'll do this one manually or via targeted regex later
    return c
rewrite("src/str/strconv.npk", fix_strconv)

# Phase 2.4: TBB Error Code Truncation
def fix_errno(c):
    c = c.replace("ERR_OVERFLOW    = 200i64", "ERR_OVERFLOW    = -10i64")
    c = c.replace("ERR_BADARG      = 201i64", "ERR_BADARG      = -11i64")
    c = c.replace("ERR_EOF         = 202i64", "ERR_EOF         = -12i64")
    c = c.replace("ERR_INTERNAL    = 202i64", "ERR_INTERNAL    = -13i64")
    c = c.replace("ERR_UNSUPPORTED = 203i64", "ERR_UNSUPPORTED = -14i64")
    c = c.replace("ERR_TRUNCATED   = 204i64", "ERR_TRUNCATED   = -15i64")
    c = c.replace("ERR_NOTFOUND    = 205i64", "ERR_NOTFOUND    = -16i64")
    c = c.replace("ERR_AGAIN       = 206i64", "ERR_AGAIN       = -17i64")
    return c
rewrite("src/syscall/errno.npk", fix_errno)

# Phase 3.1: Hardware Acceleration
def fix_memcpy_intrinsics(c):
    # We will overwrite mem_memcpy and mem_memmove
    # This is better done directly via sed or python script that completely replaces the functions.
    pass

