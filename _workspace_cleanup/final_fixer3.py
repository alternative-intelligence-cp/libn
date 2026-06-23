import os
import re

# 1. Add missing 0i64 args to sys_safe in open.npk
with open('src/io/open.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'Result<int64>:r = sys_safe(SYS_OPEN, path, safe_flags, mode);',
    'Result<int64>:r = sys_safe(SYS_OPEN, path, safe_flags, mode, 0i64, 0i64, 0i64);'
)
with open('src/io/open.npk', 'w') as f:
    f.write(code)

# 2. Fix errno_table string cast in strerror.npk
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
code = code.replace('fixed ErrEntry[]:errno_table = [', 'fixed ErrEntry:errno_table[] = [')
# Use a regex to extract all string literals in the table and declare them outside
matches = re.findall(r'\{\s*(-?\d+i64),\s*@cast_unchecked<int64>\("([^"]+)"\)\s*\}', code)
declarations = []
for i, match in enumerate(matches):
    errnum = match[0]
    msg = match[1]
    var_name = f'err_msg_{i}'
    declarations.append(f'fixed string:{var_name} = "{msg}";')
    code = code.replace(f'@cast_unchecked<int64>("{msg}")', f'@cast_unchecked<int64>(@{var_name})')
if len(declarations) > 0 and "err_msg_0" not in code:
    code = code.replace('fixed ErrEntry:errno_table[] = [', '\n'.join(declarations) + '\n\nfixed ErrEntry:errno_table[] = [')
# rename str_int64_to_dec to str_itoa
code = code.replace('str_int64_to_dec(', 'str_itoa(')
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 3. Add ERR_EOF to errno.npk
with open('src/syscall/errno.npk', 'r') as f:
    code = f.read()
if 'ERR_EOF' not in code:
    code += '\n// Custom internal error codes\npub fixed int64:ERR_EOF = 999i64;\n'
with open('src/syscall/errno.npk', 'w') as f:
    f.write(code)

# 4. Fix raw unwrapping in stdfiles.npk and file.npk
files_to_fix = [
    ('src/io/bio/stdfiles.npk', [
        ('int64:stdin_buf = mem_malloc(BUFSIZ);', 'int64:stdin_buf = raw mem_malloc(BUFSIZ);'),
        ('int64:stdout_buf = mem_malloc(BUFSIZ);', 'int64:stdout_buf = raw mem_malloc(BUFSIZ);')
    ]),
    ('src/io/bio/file.npk', [
        ('int64:parse_ok = bio_parse_mode', 'int64:parse_ok = raw bio_parse_mode'),
        ('int64:init_r = bio_ensure_std_init', 'int64:init_r = raw bio_ensure_std_init'),
        ('int64:fp = bio_alloc_file', 'int64:fp = raw bio_alloc_file')
    ]),
    ('src/io/bio/fstr.npk', [
        ('int64:c = fgetc(fp);', 'int64:c = raw fgetc(fp);'),
        ('int64:c = fputc(@cast_unchecked<int64>(p[i]), fp);', 'int64:c = raw fputc(@cast_unchecked<int64>(p[i]), fp);'),
    ]),
    ('src/io/bio/fio.npk', [
        ('Result<int64>:r = bio_flush_write_buf(fp);', 'Result<int64>:r = raw bio_flush_write_buf(fp);'), # Wait! If bio_flush returns int64, then it shouldn't be Result
        ('Result<int64>:r = bio_refill_read_buf(fp);', 'Result<int64>:r = raw bio_refill_read_buf(fp);')
    ]),
    ('src/io/bio/fprintf.npk', [
        ('drop bio_ensure_std_init();', 'drop raw bio_ensure_std_init();')
    ])
]
for filepath, replacements in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            c = f.read()
        for old, new in replacements:
            c = c.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(c)

# 5. Fix bio_refill_read_buf and bio_flush_write_buf Result<> handling
# Wait, if bio_flush_write_buf returns int64 (not Result), then it shouldn't be assigned to Result<int64>:r
with open('src/io/bio/fio.npk', 'r') as f:
    code = f.read()
code = code.replace('Result<int64>:r = raw bio_flush_write_buf(fp);', 'int64:r = bio_flush_write_buf(fp);')
code = code.replace('Result<int64>:r = bio_flush_write_buf(fp);', 'int64:r = bio_flush_write_buf(fp);')
code = code.replace('Result<int64>:r = raw bio_refill_read_buf(fp);', 'int64:r = bio_refill_read_buf(fp);')
code = code.replace('Result<int64>:r = bio_refill_read_buf(fp);', 'int64:r = bio_refill_read_buf(fp);')
# Replace r.is_error with r == FILE_EOF in fio.npk
code = code.replace('if (r.is_error) {', 'if (r == FILE_EOF) {')
code = code.replace('if (r.value == 0i64) {', 'if (r == 0i64) {')
with open('src/io/bio/fio.npk', 'w') as f:
    f.write(code)

with open('src/io/bio/fchar.npk', 'r') as f:
    code = f.read()
code = code.replace('Result<int64>:r = bio_flush_write_buf(fp);', 'int64:r = bio_flush_write_buf(fp);')
code = code.replace('if (r.is_error) {', 'if (r == FILE_EOF) {')
with open('src/io/bio/fchar.npk', 'w') as f:
    f.write(code)

print("Applied final_fixer3.py")
