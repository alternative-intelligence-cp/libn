import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Change function signatures:
    # pub func:name = Result<int64>(...) -> pub func:name = int64(...)
    code = re.sub(r'=\s*Result<([a-zA-Z0-9_]+)>\s*\(', r'= \1(', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print("Fixed returns in", path)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
