import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    new_content = content
    new_content = new_content.replace('raw to_lower_ascii', 'to_lower_ascii')
    new_content = new_content.replace('raw strcmp_has_nul', 'strcmp_has_nul')
    new_content = new_content.replace('raw fmt_puts_n', 'fmt_puts_n')
    new_content = new_content.replace('raw libn_clock_gettime', 'libn_clock_gettime')
    
    if new_content != content:
        with open(path, 'w') as f:
            f.write(new_content)
        print(f"Fixed {path}")

for root, dirs, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))

print("Done fixing raw")
