import os
import re

# 1. memutil.npk: pub func:has_zero_byte
with open('src/mem/memutil.npk', 'r') as f:
    code = f.read()
code = code.replace('\nfunc:has_zero_byte', '\npub func:has_zero_byte')
with open('src/mem/memutil.npk', 'w') as f:
    f.write(code)

# 2. strlen.npk and strchr.npk: use bool properly
for p in ['src/str/strlen.npk', 'src/str/strchr.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        # The previous code might look like: if ((has_zero_byte(w) & ~w & 0x8080...) != 0i64) {
        # But has_zero_byte ALREADY does exactly that and returns a bool!
        # So we just replace it with: if (has_zero_byte(w)) {
        # Wait, if I replace `(has_zero_byte(w) & ~w & 0x8080808080808080i64) != 0i64` with `has_zero_byte(w)`
        code = re.sub(r'\(has_zero_byte\(w\)\s*&\s*~w\s*&\s*0x8080808080808080i64\)\s*!=\s*0i64', r'has_zero_byte(w)', code)
        code = re.sub(r'has_zero_byte\(w\)\s*!=\s*0i64', r'has_zero_byte(w)', code)
        with open(p, 'w') as f:
            f.write(code)

# 3. strerror.npk: drop bio_ensure_std_init()
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
code = re.sub(r'drop bio_ensure_std_init\(\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 4. Find the pass r.value;
# It's at Line 100 in file.npk or fio.npk. Let's just fix it globally by regex again if it exists.
for p in ['src/io/bio/file.npk', 'src/io/bio/fio.npk', 'src/io/bio/fopen.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        # Check if pass r.value; exists
        if 'pass r.value;' in code:
            code = code.replace('pass r.value;', 'if (!r.is_error) { pass r.value; } pass 0i64;')
        with open(p, 'w') as f:
            f.write(code)

print("Applied ultimate_fixer12.py")
