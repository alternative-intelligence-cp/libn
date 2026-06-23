import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    
    for line in lines:
        # Arrays: int64:_atexit_handlers[32]; -> int64[32]:_atexit_handlers;
        # Works for global and stack arrays
        line = re.sub(r'\b(stack\s+|global\s+|pub\s+|pub\s+global\s+|pub\s+stack\s+)?([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_]+)\s*\[([^\]]+)\]\s*;', r'\1\2[\4]:\3;', line)
        
        # Un-declare array if it has no type (fallback)
        # Actually, Nitpick arrays are `type[size]:name;` or `type:name[size];` (old)
        
        # Specifically fix exit.npk function call
        if 'call fn();' in line:
            indent = line[:len(line) - len(line.lstrip())]
            out.append(f"{indent}void():f = @cast_unchecked<void()>(fn);\n")
            out.append(f"{indent}f();\n")
            continue
            
        out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

