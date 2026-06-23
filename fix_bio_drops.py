import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

funcs_to_drop = ['bio_free_buf', 'bio_discard_read_buf', 'bio_free_file', 'bio_refill_read_buf']

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = content
            for func in funcs_to_drop:
                # Add drop before func if it's preceded by whitespace or {
                # Ensure we don't add drop if drop is already there
                new_content = re.sub(r'(?<!drop )(?<!raw )\b' + func + r'\(', 'drop ' + func + '(', new_content)
                new_content = re.sub(r'drop drop ' + func, 'drop ' + func, new_content)
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Added drop to {path}")

