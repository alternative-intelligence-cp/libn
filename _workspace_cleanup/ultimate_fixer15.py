import os
import re

with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()

code = re.sub(r'Result<NIL>:_r_init\s*=\s*bio_ensure_std_init\(\);\s*(if\s*\(_r_init\.is_error\)\s*\{\s*\})?', r'drop(bio_ensure_std_init());', code)

with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

print("Fixed strerror.npk")
