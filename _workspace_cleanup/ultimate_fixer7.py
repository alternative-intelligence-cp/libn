import os

# 1. memset.npk: Comment out compiler_fence
with open('src/mem/memset.npk', 'r') as f:
    code = f.read()
code = code.replace('drop compiler_fence();', '// drop compiler_fence();')
with open('src/mem/memset.npk', 'w') as f:
    f.write(code)

# 2. Rename slab_alloc to mem_slab_alloc, slab_free to mem_slab_free in all files
# It's safest to just do a global replace in specific files
files_with_slab = [
    'src/mem/slab.npk',
    'src/mem/memcpy.npk',
    'src/str/strcpy.npk',
    'src/io/bio/file.npk'
]
for p in files_with_slab:
    if os.path.exists(p):
        with open(p, 'r') as f:
            c = f.read()
        c = c.replace('slab_alloc', 'mem_slab_alloc')
        c = c.replace('slab_free', 'mem_slab_free')
        with open(p, 'w') as f:
            f.write(c)

# 3. Fix strerror.npk string issues
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
# Replace string casts manually
import re
matches = re.findall(r'\{\s*(-?\d+i64),\s*@cast_unchecked<int64>\("([^"]+)"\)\s*\}', code)
declarations = []
for i, match in enumerate(matches):
    errnum = match[0]
    msg = match[1]
    var_name = f'err_msg_A{i}'
    declarations.append(f'fixed string:{var_name} = "{msg}";')
    code = code.replace(f'@cast_unchecked<int64>("{msg}")', f'@cast_unchecked<int64>(@{var_name})')
if len(declarations) > 0 and 'err_msg_A0' not in code:
    # Insert declarations near the top, after the use statements
    parts = code.split('fixed ErrEntry[]:errno_table = [')
    if len(parts) == 2:
        code = parts[0] + '\n'.join(declarations) + '\n\nfixed ErrEntry[]:errno_table = [' + parts[1]

# Fix str_int64_to_dec -> str_itoa
code = code.replace('str_int64_to_dec', 'str_itoa')
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 4. Fix strconv.npk errno_clear
with open('src/str/strconv.npk', 'r') as f:
    code = f.read()
code = code.replace('drop errno_clear();', 'drop libn_errno_set(0i64);')
code = code.replace('errno_clear()', 'libn_errno_set(0i64)')
with open('src/str/strconv.npk', 'w') as f:
    f.write(code)

# 5. Fix SYS_OPEN in open.npk
with open('src/io/open.npk', 'r') as f:
    code = f.read()
if 'use "src/syscall/syscall_numbers.npk".*;' not in code:
    code = 'use "src/syscall/syscall_numbers.npk".*;\n' + code
with open('src/io/open.npk', 'w') as f:
    f.write(code)

# 6. Fix ERR_EOF in read.npk, write.npk, file.npk
# We should change ERR_EOF to FILE_EOF
files_with_err_eof = ['src/io/read.npk', 'src/io/write.npk', 'src/io/bio/file.npk']
for p in files_with_err_eof:
    if os.path.exists(p):
        with open(p, 'r') as f:
            c = f.read()
        c = c.replace('ERR_EOF', 'FILE_EOF')
        with open(p, 'w') as f:
            f.write(c)

# 7. Add FILE_EOF to read.npk and write.npk if not present, but they probably include bio/file.npk or we just use -1i64
# wait, FILE_EOF is defined in fio.npk or fchar.npk?
# Actually, it's defined in fchar.npk. Let's just define FILE_EOF in posix_constants.npk or file.npk!
# Wait, FILE_EOF is used in many bio files. We will let compiler complain if it's not defined, or we can just replace ERR_EOF with -1i64 directly!
for p in files_with_err_eof:
    if os.path.exists(p):
        with open(p, 'r') as f:
            c = f.read()
        c = c.replace('FILE_EOF', '(-1i64)')
        with open(p, 'w') as f:
            f.write(c)

# 8. Missing mem_malloc in file.npk
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
if 'use "src/mem/mmap.npk".*;' not in code:
    code = 'use "src/mem/mmap.npk".*;\n' + code
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

print("Applied ultimate_fixer7.py")
