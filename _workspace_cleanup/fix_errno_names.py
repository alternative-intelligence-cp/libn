import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()

    orig = code
    code = code.replace('errno_set(', 'libn_errno_set(')
    code = code.replace('errno_get(', 'libn_errno_get(')
    code = re.sub(r'\bERR_RANGE\b', 'ERANGE', code)

    # Also add missing import to strconv.npk
    if "strconv.npk" in filepath:
        if 'use "src/str/strcpy.npk".*;' not in code:
            code = code.replace('use "src/str/strlen.npk".*;', 'use "src/str/strlen.npk".*;\nuse "src/str/strcpy.npk".*;')

    if code != orig:
        with open(filepath, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_file(os.path.join(root, f))
