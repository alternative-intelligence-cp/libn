import os
import sys

def build_map():
    with open('/home/randy/Workspace/REPOS/libn/src/all.npk', 'r') as f:
        all_lines = f.readlines()
    
    mapping = []
    current_global_line = 1
    
    # In npkc, 'use' works by finding the file and tokenizing it. 
    # Let's count the lines of each included file!
    # Wait, the 'use' directive itself is on a line. 
    # Does 'use' insert the file IN PLACE? Yes, it recursively lexes.
    
    for line in all_lines:
        if line.startswith('use "'):
            filename = line.split('"')[1]
            with open(filename, 'r') as inc:
                inc_lines = inc.readlines()
                for i in range(len(inc_lines)):
                    mapping.append((filename, i + 1))
            mapping.append(('/home/randy/Workspace/REPOS/libn/src/all.npk', current_global_line))
        else:
            mapping.append(('/home/randy/Workspace/REPOS/libn/src/all.npk', current_global_line))
        current_global_line += 1
        
    return mapping

mapping = build_map()

# read errors
with open('/tmp/all_errors.log', 'r') as f:
    errors = f.read()

import re
import sys
# Strip ANSI
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
errors = ansi_escape.sub('', errors)

for line in errors.split('\n'):
    if 'error: Line ' in line:
        # extract line number
        m = re.search(r'error: Line (\d+),', line)
        if m:
            gline = int(m.group(1))
            if gline <= len(mapping):
                orig_file, orig_line = mapping[gline - 1]
                print(line.replace(f'all.npk:0:0: error: Line {gline}', f'{orig_file}:{orig_line}: error:'))
            else:
                print(f"Global line {gline} out of bounds (max {len(mapping)})")

