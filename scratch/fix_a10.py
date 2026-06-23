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

# fs/path.npk
replace_in_file("fs/path.npk", [
    ("path_strlen(", "_!path_strlen(")
])

# proc/env.npk
replace_in_file("proc/env.npk", [
    ("str_strlen(", "_!str_strlen("),
    ("getenv(name)", "_!getenv(name)"),
    ("ep[i] = entry;\n        pass(0i64);", "int64:old_ptr = ep[i];\n        ep[i] = entry;\n        _?mem_free(old_ptr);\n        pass(0i64);")
])

# proc/exec.npk
replace_in_file("proc/exec.npk", [
    ("str_strlen(", "_!str_strlen("),
    ("proc_getenv_from(", "_!proc_getenv_from("),
    ("int64:ret = execve(", "int64:ret = _!execve(")
])

# io/bio/fstr.npk
replace_in_file("io/bio/fstr.npk", [
    ("int64:c = fgetc(fp);", "int64:c = _!fgetc(fp);"),
    ("int64:c = fputc(", "int64:c = _!fputc(")
])

# str/strbuf.npk
replace_in_file("str/strbuf.npk", [
    ("str_strlen(str);", "_!str_strlen(str);")
])

# proc/wait.npk
replace_in_file("proc/wait.npk", [
    ("waitpid(", "_!waitpid("),
    ("wait_exited(", "_!wait_exited(")
])

# math/math.npk
def fix_math(c):
    c = c.replace("pass(math_div_floor_i64(2i64 * a + b, 2i64 * b));", "return math_div_floor_i64(2i64 * a + b, 2i64 * b);")
    c = c.replace("pass(math_sat_add_i64(a, 0i64 - b));", "return math_sat_add_i64(a, 0i64 - b);")
    return c
replace_in_file("math/math.npk", [
    ("pass", fix_math)
])

# io/bio/fscanf.npk
def fix_fscanf(c):
    c = re.sub(r'pass\(bio_scan_engine\((.*?)\)\);', r'return bio_scan_engine(\1);', c)
    return c
replace_in_file("io/bio/fscanf.npk", [
    ("pass", fix_fscanf)
])

# mem/mmap.npk
def fix_mmap(c):
    c = c.replace("pass mem_malloc(new_size);", "return mem_malloc(new_size);")
    c = c.replace("fixed int64:ALLOC_HEADER_SIZE = 16i64;", "fixed int64:ALLOC_HEADER_SIZE = 24i64;")
    c = c.replace("hdr[0] = total | 0x4D4D415000000000i64;", "hdr[0] = 0x4D4D415000000000i64;\n    hdr[1] = total;\n    hdr[2] = size;")
    c = c.replace("int64:total = hdr[0] & 0x0000FFFFFFFFFFFFi64;", "int64:total = hdr[1];")
    return c
replace_in_file("mem/mmap.npk", [
    ("pass", fix_mmap)
])

# mem/memset.npk
replace_in_file("mem/memset.npk", [
    ("volatile p[i] = fill;", "p[i] = fill;"),
    ("compiler_fence();", '_?asm!!!<int64>("x86_64", "", "~{memory}");')
])

# mem/slab.npk
replace_in_file("mem/slab.npk", [
    ("if (ptr - 16i64 => int64->)[0] == 0x4D4D415000000000i64 {", "if (ptr & 4095i64) == 16i64 {\n        if (ptr - 16i64 => int64->)[0] == 0x4D4D415000000000i64 {")
])

def fix_slab2(c):
    return c.replace("            pass(NIL);\n        }", "            pass(NIL);\n        }\n    }")
replace_in_file("mem/slab.npk", [("pass", fix_slab2)])

# str/strconv.npk
replace_in_file("str/strconv.npk", [
    ("if negative && result > (INT64_MAX + 1i64) / base {", "int64:limit = INT64_MAX / base;\n        if result > limit {"),
    ("if !negative && result > INT64_MAX / base {", "if false {") # removed as it's merged with the above
])

# io/bio/fio.npk
replace_in_file("io/bio/fio.npk", [
    ("_?bio_flush_write_buf(fp);", "Result<int64>:fr = bio_flush_write_buf(fp);\n            if fr.is_error { f->flags = f->flags | FILE_FLAG_ERROR; break; }")
])

# mem/memutil.npk
replace_in_file("mem/memutil.npk", [
    ("while i < n && (((a + i) | (b + i)) & 7i64) != 0i64 {", "while i < n && ((a + i) & 7i64) != 0i64 {")
])

print("A10 fixes script prepared.")
