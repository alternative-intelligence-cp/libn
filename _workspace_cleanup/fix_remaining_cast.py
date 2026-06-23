import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Just replace `@cast_unchecked<int64>(r)` with `@cast_unchecked<int64>(r.error)` everywhere it's inside `libn_errno_set` or similar.
    content = re.sub(r'@cast_unchecked<int64>\((r|wr|r1|r2)\)', r'@cast_unchecked<int64>(\1.error)', content)

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    if 'io' not in root: continue
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
