import os
import re

def rewrite_file(filepath, callback):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    new_content = callback(content)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

# 1. Fix string literal casts in strerror.npk
def fix_strerror(c):
    return re.sub(r'@cast_unchecked<int64>\("([^"]+)"\)', r'@cast_unchecked<int64>(@"\1")', c)

rewrite_file('src/io/bio/strerror.npk', fix_strerror)

# 2. Fix has_zero_byte in memutil.npk and strlen.npk
def fix_has_zero(c):
    return c.replace('has_zero_byte', 'has_zero_uint8')

rewrite_file('src/mem/memutil.npk', fix_has_zero)
rewrite_file('src/str/strlen.npk', fix_has_zero)

# 3. Fix errno_clear in strconv.npk
def fix_errno_clear(c):
    return c.replace('errno_clear()', 'libn_errno_set(0i64)')

rewrite_file('src/str/strconv.npk', fix_errno_clear)

# 4. Add missing mmap.npk import to file.npk
def fix_file_imports(c):
    if 'use "src/mem/mmap.npk".*;' not in c:
        return c.replace('use "src/mem/slab.npk".*;\n', 'use "src/mem/slab.npk".*;\nuse "src/mem/mmap.npk".*;\n')
    return c

rewrite_file('src/io/bio/file.npk', fix_file_imports)

# 5. Remove compiler_fence from memset.npk
def fix_memset(c):
    return re.sub(r'^\s*drop\(compiler_fence\(\)\);\n', '', c, flags=re.MULTILINE)

rewrite_file('src/mem/memset.npk', fix_memset)

# 6. Add ERR_EOF to errno.npk
def fix_errno(c):
    if 'ERR_EOF' not in c:
        return c + '\n// Added ERR_EOF\npub fixed int64:ERR_EOF = 61i64;\n'
    return c

rewrite_file('src/syscall/errno.npk', fix_errno)

