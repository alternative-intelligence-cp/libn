import os, re

def process(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    changed = False
    
    for i, line in enumerate(lines):
        # 1. Fix extra closing parentheses
        stripped = line.rstrip('\n')
        if stripped.endswith('{'):
            open_count = line.count('(')
            close_count = line.count(')')
            if close_count > open_count:
                diff = close_count - open_count
                new_line = line
                for _ in range(diff):
                    new_line = re.sub(r'\)\s*\{', ' {', new_line)
                if new_line != line:
                    lines[i] = new_line
                    changed = True

        # 2. Fix ^}$ to };
        if lines[i] == '}\n' or lines[i] == '}':
            lines[i] = '};\n' if lines[i].endswith('\n') else '};'
            changed = True
            
        # 3. Fix struct:NAME { to struct:NAME = {
        new_line = re.sub(r'struct:([a-zA-Z0-9_]+)\s*\{', r'struct:\1 = {', lines[i])
        if new_line != lines[i]:
            lines[i] = new_line
            changed = True

    if changed:
        with open(filepath, "w") as f:
            f.writelines(lines)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            process(os.path.join(root, file))
