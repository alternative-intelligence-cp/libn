import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace .err with .error
    new_content = re.sub(r'\.err\b', '.error', content)
    
    # Replace byte with uint8 (as a whole word)
    new_content = re.sub(r'\bbyte\b', 'uint8', new_content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            process_file(os.path.join(root, file))
