import os
import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    
    # regex to match a standalone function call
    # e.g. "    foo(bar);"
    # exclude keywords, comments, assignments
    pattern = re.compile(r'^(\s*)([a-zA-Z0-9_]+)\((.*)\);(\s*(?://.*)?)$')
    
    keywords = {"if", "while", "pass", "fail", "drop", "continue", "break"}
    
    for line in lines:
        m = pattern.match(line)
        if m:
            indent = m.group(1)
            func_name = m.group(2)
            args = m.group(3)
            tail = m.group(4)
            
            if func_name not in keywords:
                # Wrap in drop
                new_line = f"{indent}drop({func_name}({args}));{tail}\n"
                new_lines.append(new_line)
                changed = True
                continue
                
        new_lines.append(line)
        
    if changed:
        with open(filepath, "w") as f:
            f.writelines(new_lines)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            fix_file(os.path.join(root, file))
