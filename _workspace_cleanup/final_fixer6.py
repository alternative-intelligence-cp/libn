import os
import re

# 1. strfmt.npk: String literals array indexing Fix
with open('src/str/strfmt.npk', 'r') as f:
    code = f.read()
# Replace the old indexing with correct variables
if 'LOWER_STR' not in code:
    code = code.replace(
        'fixed int64:DIGITS_LOWER = @cast_unchecked<int64>(@"0123456789abcdef"[0]);',
        'fixed string:LOWER_STR = "0123456789abcdef";\nfixed int64:DIGITS_LOWER = @cast_unchecked<int64>(@LOWER_STR);'
    )
if 'UPPER_STR' not in code:
    code = code.replace(
        'fixed int64:DIGITS_UPPER = @cast_unchecked<int64>(@"0123456789ABCDEF"[0]);',
        'fixed string:UPPER_STR = "0123456789ABCDEF";\nfixed int64:DIGITS_UPPER = @cast_unchecked<int64>(@UPPER_STR);'
    )
if 'NULL_STR' not in code:
    code = code.replace(
        'sptr = @cast_unchecked<int64>(@"(null)"[0]);',
        'fixed string:NULL_STR = "(null)";\n                sptr = @cast_unchecked<int64>(@NULL_STR);'
    )
with open('src/str/strfmt.npk', 'w') as f:
    f.write(code)

# 2. stdfiles.npk: Restore raw mem_malloc
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:stdin_buf = mem_malloc(BUFSIZ);', 'Result<int64>:r_in = mem_malloc(BUFSIZ);\n    int64:stdin_buf = 0i64;\n    if (!r_in.is_error) { stdin_buf = r_in.value; }')
code = code.replace('int64:stdout_buf = mem_malloc(BUFSIZ);', 'Result<int64>:r_out = mem_malloc(BUFSIZ);\n    int64:stdout_buf = 0i64;\n    if (!r_out.is_error) { stdout_buf = r_out.value; }')
# Also fix `int64:r1 = raw fflush(stdin_fp);`
# Wait! fflush returns Result<int64> because of the `fail` in bio_flush_write_buf that fflush calls!
# So `Result<int64>:r1_r = fflush(stdin_fp); int64:r1 = 0i64; if (!r1_r.is_error) { r1 = r1_r.value; }`
code = code.replace('int64:r1 = fflush(stdin_fp);', 'Result<int64>:r1_r = fflush(stdin_fp);\n    int64:r1 = 0i64; if (!r1_r.is_error) { r1 = r1_r.value; } else { r1 = FILE_EOF; }')
code = code.replace('int64:r2 = fflush(stdout_fp);', 'Result<int64>:r2_r = fflush(stdout_fp);\n    int64:r2 = 0i64; if (!r2_r.is_error) { r2 = r2_r.value; } else { r2 = FILE_EOF; }')
code = code.replace('int64:r3 = fflush(stderr_fp);', 'Result<int64>:r3_r = fflush(stderr_fp);\n    int64:r3 = 0i64; if (!r3_r.is_error) { r3 = r3_r.value; } else { r3 = FILE_EOF; }')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

# 3. fstr.npk: fgetc returns Result<int64>!
with open('src/io/bio/fstr.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:c = fgetc(fp);', 'Result<int64>:c_r = fgetc(fp);\n        int64:c = 0i64; if (!c_r.is_error) { c = c_r.value; } else { c = FILE_EOF; }')
code = code.replace('int64:c = fputc(@cast_unchecked<int64>(p[i]), fp);', 'Result<int64>:c_r2 = fputc(@cast_unchecked<int64>(p[i]), fp);\n        int64:c = 0i64; if (!c_r2.is_error) { c = c_r2.value; } else { c = FILE_EOF; }')
with open('src/io/bio/fstr.npk', 'w') as f:
    f.write(code)

# 4. fchar.npk: bio_flush_write_buf returns Result<int64>!
with open('src/io/bio/fchar.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:r = bio_flush_write_buf(fp);', 'Result<int64>:r = bio_flush_write_buf(fp);')
with open('src/io/bio/fchar.npk', 'w') as f:
    f.write(code)

# 5. fio.npk: bio_flush_write_buf returns Result<int64>!
with open('src/io/bio/fio.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:r = bio_flush_write_buf(fp);', 'Result<int64>:r = bio_flush_write_buf(fp);')
code = code.replace('int64:r = bio_refill_read_buf(fp);', 'Result<int64>:r = bio_refill_read_buf(fp);')
with open('src/io/bio/fio.npk', 'w') as f:
    f.write(code)

# 6. file.npk: bio_alloc_buf returns Result<int64> (calls mem_malloc)
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:fp = bio_alloc_file();', 'Result<int64>:fp_r = bio_alloc_file();\n    if (fp_r.is_error) { pass 0i64; }\n    int64:fp = fp_r.value;')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

# 7. fscanf.npk: bio_scan_getc returns Result<int64> (calls fgetc)
with open('src/io/bio/fscanf.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:c = bio_scan_getc(src);', 'Result<int64>:c_r = bio_scan_getc(src);\n        int64:c = -1i64; if (!c_r.is_error) { c = c_r.value; }')
with open('src/io/bio/fscanf.npk', 'w') as f:
    f.write(code)

# 8. strerror.npk string casts
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
matches = re.findall(r'\{\s*(-?\d+i64),\s*@cast_unchecked<int64>\("([^"]+)"\)\s*\}', code)
declarations = []
for i, match in enumerate(matches):
    errnum = match[0]
    msg = match[1]
    var_name = f'err_msg_{i}'
    declarations.append(f'fixed string:{var_name} = "{msg}";')
    code = code.replace(f'@cast_unchecked<int64>("{msg}")', f'@cast_unchecked<int64>(@{var_name})')
if len(declarations) > 0 and "err_msg_0" not in code:
    code = code.replace('fixed ErrEntry[]:errno_table = [', '\n'.join(declarations) + '\n\nfixed ErrEntry[]:errno_table = [')
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 9. Ensure open.npk has 7 args for sys_safe
with open('src/io/open.npk', 'r') as f:
    code = f.read()
if 'sys_safe(SYS_OPEN, path, safe_flags, mode)' in code:
    code = code.replace('sys_safe(SYS_OPEN, path, safe_flags, mode)', 'sys_safe(SYS_OPEN, path, safe_flags, mode, 0i64, 0i64, 0i64)')
with open('src/io/open.npk', 'w') as f:
    f.write(code)

print("Applied final_fixer6.py")
