import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # 1. Fix *type:var to type->:var
    code = re.sub(r'\*([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)', r'\1->:\2', code)

    # 2. Fix expr as type -> @cast_unchecked<type>(expr)
    # We'll use a regex that captures word/field expressions
    code = re.sub(r'([a-zA-Z0-9_.]+)\s+as\s+([a-zA-Z0-9_]+)', r'@cast_unchecked<\2>(\1)', code)
    code = re.sub(r'([a-zA-Z0-9_.]+)\s+as\s+\*([a-zA-Z0-9_]+)', r'@cast_unchecked<\2->>(\1)', code)
    
    # Wait, ERR_EOF as tbb8 => @cast_unchecked<tbb8>(ERR_EOF)
    # mode_str as *byte => @cast_unchecked<byte->>(mode_str) -> @cast_unchecked<uint8->>(mode_str)
    code = code.replace('@cast_unchecked<byte->>', '@cast_unchecked<uint8->>')

    # 3. Fix struct:Name =) {
    code = re.sub(r'struct:([a-zA-Z0-9_]+)\s*\=\)\s*\{', r'struct:\1 = {', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
