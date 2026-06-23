import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

# This matches Result<...>:var = ...; pass var;
# and replaces `pass var;` with `return var;`
# We also need to find cases where there might be lines between.
# Let's just find `Result<.*>:([a-zA-Z0-9_]+) =` and store the variable,
# then replace `pass var;` with `return var;` in the same function.

def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    changed = False
    result_vars = set()
    
    for i, line in enumerate(lines):
        # find Result<...>:var = 
        m = re.search(r'Result<[^>]+>:([a-zA-Z0-9_]+)\s*=', line)
        if m:
            result_vars.add(m.group(1))
            
        # replace pass var;
        if 'pass ' in line:
            m2 = re.search(r'pass\s+([a-zA-Z0-9_]+)\s*;', line)
            if m2 and m2.group(1) in result_vars:
                lines[i] = line.replace(f'pass {m2.group(1)};', f'return {m2.group(1)};')
                changed = True
        
        if line.strip() == '};':
            result_vars.clear()

    if changed:
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print(f"Fixed passes in {filepath}")

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            process_file(os.path.join(root, file))
