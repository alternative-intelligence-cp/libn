import os
import re

# 1. Remove all drop(_nil_r); globally
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            p = os.path.join(root, file)
            with open(p, 'r') as f:
                code = f.read()
            if 'drop(_nil_r);' in code:
                code = code.replace('drop(_nil_r);', '')
                with open(p, 'w') as f:
                    f.write(code)

# 2. Fix strlen.npk and strchr.npk has_zero_byte
for p in ['src/str/strlen.npk', 'src/str/strchr.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        # Add import
        if 'src/mem/memutil.npk' not in code:
            code = 'use "src/mem/memutil.npk".*;\n' + code
        # Fix Bitwise bool vs int64
        # Original: if ((has_zero_byte(w)) != 0i64)
        # We need to make sure the inner is NOT bool. has_zero_byte returns int64.
        # But wait! I changed the definition in strlen.npk? I did not.
        code = code.replace('has_zero_byte(w) != 0i64', 'has_zero_byte(w)')
        code = re.sub(r'if \(\(has_zero_byte\(w\)(.*?)\)\s*\{', r'if ((has_zero_byte(w)\1) != 0i64) {', code)
        code = code.replace('!= 0i64 != 0i64', '!= 0i64')
        with open(p, 'w') as f:
            f.write(code)

# 3. Fix file.npk line 100
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
# We look for "pass r.value;" in file.npk and replace it with safe unwrapping
code = code.replace('if (!r.is_error) { if (!r.is_error) { pass r.value; }', 'if (!r.is_error) { pass r.value; }')
code = code.replace('pass r.value;', 'if (!r.is_error) { pass r.value; }\n    pass 0i64;')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

print("Applied ultimate_fixer9.py")
