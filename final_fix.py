import re

def fix_file(path, replacements):
    with open(path, 'r') as f:
        s = f.read()
    for old, new in replacements:
        s = s.replace(old, new)
    with open(path, 'w') as f:
        f.write(s)

# syscall.npk
fix_file('src/syscall/syscall.npk', [
    ('Result<int64>:ret = sys(nr, a1, a2, a3, a4, a5, a6);', 'Result<int64>:ret = sys!!(nr, a1, a2, a3, a4, a5, a6);'),
])

# mmap.npk
fix_file('src/mem/mmap.npk', [
    ('if (r.val < 0i64 {', 'if (r.val < 0i64) {'),
])

# file.npk
fix_file('src/io/bio/file.npk', [
    ('if (unread > 0i64 {', 'if (unread > 0i64) {'),
])

# strfmt.npk
fix_file('src/str/strfmt.npk', [
    ('if (precision < 0i64 {', 'if (precision < 0i64) {'),
    ('if (padding > 0i64 {', 'if (padding > 0i64) {'),
])

# math.npk
fix_file('src/math/math.npk', [
    ('if (a < 0i64 {', 'if (a < 0i64) {'),
    ('if (b < 0i64 {', 'if (b < 0i64) {'),
    ('if (a < b {', 'if (a < b) {'),
    ('if (b < a {', 'if (b < a) {'),
])

# memutil.npk
fix_file('src/mem/memutil.npk', [
    ('if (a < b {', 'if (a < b) {'),
    ('if (len > 0i64 {', 'if (len > 0i64) {'),
])

# strlen.npk
fix_file('src/str/strlen.npk', [
    ('while (n > 0i64 {', 'while (n > 0i64) {'),
])

# slab.npk
fix_file('src/mem/slab.npk', [
    ('if (n <= 2048i64 {', 'if (n <= 2048i64) {'),
])

# More targeted regex for 'if (X {' -> 'if (X) {'
import glob
for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        s = f.read()
    s = re.sub(r'if\s*\(([^)]+?)\s*\{', r'if (\1) {', s)
    s = re.sub(r'while\s*\(([^)]+?)\s*\{', r'while (\1) {', s)
    with open(filepath, 'w') as f:
        f.write(s)
