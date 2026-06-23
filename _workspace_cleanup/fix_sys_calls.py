import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()
    orig = code

    # Replace sys_safe( to sys(
    code = code.replace('sys_safe(', 'sys(')
    # Replace sys_full( to sys!!(
    code = code.replace('sys_full(', 'sys!!(')
    # Replace sys1(, sys2( ... to sys(
    code = re.sub(r'\bsys[1-6]\(', 'sys(', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
