import glob, re

def fix_file(path, replacements):
    with open(path, 'r') as f:
        s = f.read()
    for old, new in replacements:
        s = s.replace(old, new)
    with open(path, 'w') as f:
        f.write(s)

fix_file('src/mem/slab.npk', [('if (cls > SLAB_MAX_CLASS)) {', 'if (cls > SLAB_MAX_CLASS) {')])
fix_file('src/mem/mmap.npk', [('if (r.val < 0i64 {', 'if (r.val < 0i64) {')])
fix_file('src/io/bio/file.npk', [('if (unread > 0i64 {', 'if (unread > 0i64) {')])
fix_file('src/str/strfmt.npk', [('if (precision < 0i64 {', 'if (precision < 0i64) {'), ('if (padding > 0i64 {', 'if (padding > 0i64) {')])
fix_file('src/math/math.npk', [('if (a < 0i64 {', 'if (a < 0i64) {'), ('if (b < 0i64 {', 'if (b < 0i64) {'), ('if (a < b {', 'if (a < b) {'), ('if (b < a {', 'if (b < a) {')])
fix_file('src/mem/memutil.npk', [('if (a < b {', 'if (a < b) {'), ('if (len > 0i64 {', 'if (len > 0i64) {')])
fix_file('src/str/strlen.npk', [('while (n > 0i64 {', 'while (n > 0i64) {')])

for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        s = f.read()
    s = s.replace(')) {', ') {')
    s = re.sub(r'if\s*\(([^()]+)\s*\{', r'if (\1) {', s)
    s = re.sub(r'while\s*\(([^()]+)\s*\{', r'while (\1) {', s)
    with open(filepath, 'w') as f:
        f.write(s)
