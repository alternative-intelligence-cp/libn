import re

with open("src/io/bio/fprintf.npk", "r") as f:
    content = f.read()

# 1. Add correct imports
if 'use "src/mem/mmap.npk".*;' not in content:
    content = content.replace('use "src/mem/slab.npk".*;\n', 'use "src/mem/slab.npk".*;\nuse "src/mem/memcpy.npk".*;\nuse "src/mem/mmap.npk".*;\n')

# 2. Add semicolons to function ends
content = re.sub(r'\}\n\n', r'};\n\n', content)
content = re.sub(r'\}$', r'};', content)
content = re.sub(r'\}\n(// ──)', r'};\n\1', content)

# 3. Parenthesize ifs
content = re.sub(r'if\s+len\s+==\s+0i64\s+\{', r'if (len == 0i64) {', content)
content = re.sub(r'if\s+written\s+<\s+len\s+\{', r'if (written < len) {', content)
content = re.sub(r'if\s+p\s+==\s+0i64\s+\{', r'if (p == 0i64) {', content)
content = re.sub(r'if\s+out_len\s+!=\s+0i64\s+\{', r'if (out_len != 0i64) {', content)

# 4. Fix byte arrays
content = content.replace("stack byte:buf[4096];", "stack uint8[4096]:buf;")
content = content.replace("stack byte:tmp[4096];", "stack uint8[4096]:tmp;")
content = content.replace("&buf[0] as int64", "raw fprintf_ptr_to_int_u8(buf)")
content = content.replace("&tmp[0] as int64", "raw fprintf_ptr_to_int_u8(tmp)")
content = content.replace("(out_len as *int64)", "@cast_unchecked<int64->>(out_len)")

# 5. Fix bio_fprint_rendered block scope
content = re.sub(
    r'func:bio_fprint_rendered = int64\(int64:fp, int64:rendered_buf\) \{.*?\n\};',
    r'''func:bio_fprint_rendered = int64(int64:fp, int64:rendered_buf) {
    int64:len = 0i64;
    int64:written = 0i64;
    len = str_strlen(rendered_buf);
    if (len == 0i64) {
        pass 0i64;
    }
    written = fwrite(rendered_buf, 1i64, len, fp);
    if (written < len) {
        pass -1i64;
    }
    pass written;
};''',
    content,
    flags=re.DOTALL
)

# 6. Fix asprintf block scopes and results
def repl_asprintf(match):
    num = match.group(1)
    args_sig = match.group(2)
    args_call = re.sub(r'int64:', '', args_sig)
    return f"""pub func:asprintf{num} = int64(int64:out_len, int64:fmt{args_sig}) {{
    stack uint8[4096]:tmp;
    int64:tmp_ptr = 0i64;
    int64:len = 0i64;
    Result<int64>:r_p = ok_i64(0i64);
    int64:p = 0i64;

    tmp_ptr = raw fprintf_ptr_to_int_u8(tmp);
    drop str_snprintf{num}(tmp_ptr, 4096i64, fmt{args_call});
    len = str_strlen(tmp_ptr);
    r_p = mem_malloc(len + 1i64);
    if (r_p.is_error) {{ pass 0i64; }}
    p = r_p.value;
    drop mem_memcpy(p, tmp_ptr, len + 1i64);
    if (out_len != 0i64) {{ @cast_unchecked<int64->>(out_len)[0] = len; }}
    pass p;
}};"""

content = re.sub(
    r'pub func:asprintf(\d+) = int64\(int64:out_len, int64:fmt((?:,\s*int64:a\d+)*)\) \{.*?\n\};',
    repl_asprintf,
    content,
    flags=re.DOTALL
)

with open("src/io/bio/fprintf.npk", "w") as f:
    f.write(content)

