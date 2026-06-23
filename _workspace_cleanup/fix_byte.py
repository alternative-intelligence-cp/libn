import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Replace 'byte' with 'uint8' when used as a type
    # This includes byte, byte->, byte@, byte[24], etc.
    code = re.sub(r'\bbyte\b', 'uint8', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
