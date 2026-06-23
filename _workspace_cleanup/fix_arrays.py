import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Match `prefix type:name[size];` -> `prefix type[size]:name;`
    # Also handles empty brackets like `prefix type:name[] = ...;` -> `prefix type[]:name = ...;`
    code = re.sub(r'((?:pub\s+)?(?:stack\s+|fixed\s+)?)([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\[([0-9]*)\](\s*[;=])', r'\1\2[\4]:\3\5', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print("Fixed arrays in", path)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
