import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Fix *FILE:f = fp as *FILE;
    content = re.sub(r'\*FILE:([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_]+)\s+as\s+\*FILE;', r'FILE->:\1 = @cast_unchecked<FILE->>(\2);', content)

    # 2. Fix the ternary in fopen.npk line 70:
    # f.buf_mode = (fd == 1i64) ? _IOLBF : _IOFBF;
    # To if/else block.
    if 'f.buf_mode = (fd == 1i64) ? _IOLBF : _IOFBF;' in content:
        ternary_fix = """if (fd == 1i64) { f.buf_mode = _IOLBF; } else { f.buf_mode = _IOFBF; }"""
        content = content.replace('f.buf_mode = (fd == 1i64) ? _IOLBF : _IOFBF;', ternary_fix)

    # 3. Fix `if !is_std && fd >= 0i64 {`
    # Already done by fix_fopen.py, but let's just make sure.

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src/io/bio'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
