import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    out = []
    lines = content.split('\n')
    in_struct = False
    for line in lines:
        if re.search(r'struct:[a-zA-Z0-9_]+\s*=\s*\{', line):
            in_struct = True
        elif in_struct and line.strip() == '}':
            line = line.replace('}', '};')
            in_struct = False
        
        # fix `if first {`
        if 'if first {' in line:
            line = line.replace('if first {', 'if (first) {')
            
        out.append(line)

    with open(path, 'w') as f:
        f.write('\n'.join(out))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

