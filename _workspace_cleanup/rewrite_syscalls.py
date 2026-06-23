import os
import re

def process_file(path):
    with open(path, "r") as f:
        content = f.read()

    original = content

    # Use regex with word boundaries to avoid matching things like `sys_write` or `sys_safe_something`
    # Replace sys_safe -> sys
    content = re.sub(r'\bsys_safe\s*\(', 'sys(', content)
    # Replace sys1, sys2, sys3, sys4, sys5 -> sys
    content = re.sub(r'\bsys[1-5]\s*\(', 'sys(', content)
    
    # Replace sys_fullN -> sys!!
    content = re.sub(r'\bsys_full[1-5]?\s*\(', 'sys!!(', content)
    
    # Replace sys_raw -> sys!!!
    content = re.sub(r'\bsys_raw\s*\(', 'sys!!!(', content)
    
    if content != original:
        with open(path, "w") as f:
            f.write(content)
        print(f"Updated {path}")

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            process_file(os.path.join(root, file))

