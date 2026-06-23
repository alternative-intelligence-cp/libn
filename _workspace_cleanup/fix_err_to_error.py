import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Replace .err with .error globally
    code = re.sub(r'\.err\b', '.error', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
