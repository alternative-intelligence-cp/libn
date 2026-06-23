import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    out = []
    
    for line in lines:
        # Match `stack type:name[size];`
        # e.g., `stack int64:argv[1];` -> `stack int64[1]:argv;`
        # `stack byte:candidate[4096];` -> `stack byte[4096]:candidate;`
        m = re.search(r'stack\s+([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\[([a-zA-Z0-9_\(\)\+\-\* ]+)\];', line)
        if m:
            t = m.group(1)
            name = m.group(2)
            size = m.group(3)
            line = line[:m.start()] + f"stack {t}[{size}]:{name};" + line[m.end():]
        out.append(line)

    with open(path, 'w') as f:
        f.write('\n'.join(out))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
