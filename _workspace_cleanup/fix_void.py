import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Replace = void( with = NIL(
    code = re.sub(r'=\s*void\s*\(', '= NIL(', code)

    # Prefix raw to common assignments
    code = re.sub(r'int64:([a-zA-Z0-9_]+)\s*=\s*(str_strlen|str_snprintf\d+|str_strerror)\(', r'int64:\1 = raw \2(', code)
    code = re.sub(r'int64:([a-zA-Z0-9_]+)\s*=\s*(mem_memchr)\(', r'int64:\1 = raw \2(', code)
    code = re.sub(r'int64:([a-zA-Z0-9_]+)\s*=\s*(mem_malloc)\(', r'int64:\1 = raw \2(', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
