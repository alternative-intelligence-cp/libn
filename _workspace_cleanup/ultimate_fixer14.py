import os
import re

# 1. strlen.npk
with open('src/str/strlen.npk', 'r') as f:
    code = f.read()

# Replace `while ((s + i) & 7i64 != 0i64)` with `while (((s + i) & 7i64) != 0i64)`
code = code.replace('while ((s + i) & 7i64 != 0i64) {', 'while (((s + i) & 7i64) != 0i64) {')

# Replace `while (i < max_len && (s + i) & 7i64 != 0i64)` with `while (i < max_len && ((s + i) & 7i64) != 0i64)`
code = code.replace('while (i < max_len && (s + i) & 7i64 != 0i64) {', 'while (i < max_len && ((s + i) & 7i64) != 0i64) {')

with open('src/str/strlen.npk', 'w') as f:
    f.write(code)


# 2. fprintf.npk
with open('src/io/bio/fprintf.npk', 'r') as f:
    code = f.read()
# Replace `Result<NIL>:_r_init = bio_ensure_std_init();` optionally followed by `if (_r_init.is_error) {}`
code = re.sub(r'Result<NIL>:_r_init\s*=\s*bio_ensure_std_init\(\);\s*(if\s*\(_r_init\.is_error\)\s*\{\s*\})?', r'drop(bio_ensure_std_init());', code)
with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(code)


# 3. stdfiles.npk
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
code = re.sub(r'Result<NIL>:_r_init\s*=\s*bio_ensure_std_init\(\);\s*(if\s*\(_r_init\.is_error\)\s*\{\s*\})?', r'drop(bio_ensure_std_init());', code)
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)


# 4. Global replace of `drop bio_ensure_std_init();` to `drop(bio_ensure_std_init());`
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                code = f.read()
            if 'drop bio_ensure_std_init();' in code:
                code = code.replace('drop bio_ensure_std_init();', 'drop(bio_ensure_std_init());')
                with open(filepath, 'w') as f:
                    f.write(code)

print("Applied ultimate_fixer14.py")
