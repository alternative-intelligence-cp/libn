import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()

            new_content = re.sub(r'=\s*raw\s+([a-zA-Z_]\w*\s*\()', r'= \1', content)

            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Stripped raw from {path}")
