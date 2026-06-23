import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

func_sig_re = re.compile(r'(pub\s+)?func:([a-zA-Z0-9_]+)\s*=\s*Result<([a-zA-Z0-9_]+)>\s*\(')

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = func_sig_re.sub(r'\1func:\2 = \3(', content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            process_file(os.path.join(root, file))

