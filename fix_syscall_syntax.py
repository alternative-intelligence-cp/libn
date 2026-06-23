import re
with open('src/syscall/syscall.npk', 'r') as f:
    s = f.read()

# Fix `if condition {` -> `if (condition) {`
s = re.sub(r'if\s+([^({][^{]*?)\s*\{', r'if (\1) {', s)
# Fix `while condition {` -> `while (condition) {`
s = re.sub(r'while\s+([^({][^{]*?)\s*\{', r'while (\1) {', s)
# Fix missing semicolons on functions
s = re.sub(r'\}\s*\n\s*(?=pub func|func)', r'};\n\n', s)
if s.strip().endswith('}'): s += ';'

# Fix specific `if (r == -1i64 as tbb8)` -> `if (r == @cast_unchecked<tbb8>(-1i64))`
s = re.sub(r'([-\w]+)\s+as\s+(\w+)', r'@cast_unchecked<\2>(\1)', s)

# Fix `pass ret` -> `pass(ret)` (if pass is treated like function? NO, pass is `pass ret;`)
# Nitpick v0.12 might require `pass ...;` or `pass(...)` ? Let's look at `all_chunks.json` for exit.npk: it used `pass(-1i64);`?
# NO, my previous agent changed `pass r` to `pass(r)` because it thought it was needed. But `pass` works fine as `pass r;`. Let's just fix the `if/while` and `as`.
with open('src/syscall/syscall.npk', 'w') as f:
    f.write(s)
