import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

# Regex to match standalone function calls
# Matches: <spaces>func_name(args...);
# Does NOT match assignments: var = func(); or Result:r = func();
# Keywords to ignore: return, pass, fail, drop, raw, if, while, else, struct, func
ignore_keywords = {'return', 'pass', 'fail', 'drop', 'raw', 'if', 'while', 'else', 'struct', 'func', 'use'}

call_pattern = re.compile(r'^(\s*)([a-zA-Z0-9_]+)\s*\(.*\)\s*;\s*$')

def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    changed = False
    for i, line in enumerate(lines):
        m = call_pattern.match(line)
        if m:
            indent = m.group(1)
            func_name = m.group(2)
            if func_name not in ignore_keywords:
                lines[i] = f"{indent}drop {line.lstrip()}"
                changed = True

    if changed:
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print(f"Fixed drops in {filepath}")

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            process_file(os.path.join(root, file))
