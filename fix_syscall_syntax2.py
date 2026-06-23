import re
with open('src/syscall/syscall.npk', 'r') as f:
    s = f.read()

# Fix `if condition {` -> `if (condition) {`
s = re.sub(r'if\s+([^{]*?)\s*\{', r'if (\1) {', s)
# Fix `while condition {` -> `while (condition) {`
s = re.sub(r'while\s+([^{]*?)\s*\{', r'while (\1) {', s)

# Undo double parens if we made them by mistake? Let's check `if ( (r.is_error) )`
s = re.sub(r'if\s+\(\((.*?)\)\)\s*\{', r'if (\1) {', s)
s = re.sub(r'while\s+\(\((.*?)\)\)\s*\{', r'while (\1) {', s)

# Fix missing semicolons on functions
s = re.sub(r'\}\n(?=pub func|func|//)', r'};\n', s)
if s.strip().endswith('}'): s = s.rstrip() + ';\n'

# Fix `r.error as int64` -> `@cast_unchecked<int64>(r.error)`
# Match `(\w+(?:\.\w+)?)\s+as\s+(\w+)`
s = re.sub(r'([\w.]+)\s+as\s+(\w+)', r'@cast_unchecked<\2>(\1)', s)

# Fix `pass ret` -> `pass(ret)` ? NO, `pass` is a keyword. `pass ret;` is fine.

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(s)
