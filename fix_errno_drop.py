import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

changed = 0

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Match errno_set(...) that is NOT preceded by 'drop(' or 'raw '
            # and ends with ';'
            # We must be careful about newlines inside errno_set, but usually it's on one line.
            new_content = re.sub(r'(?<!drop\()(?<!raw\s)\berrno_set\(([^)]+)\);', r'drop(errno_set(\1));', content)
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                changed += 1
                print(f"Fixed errno_set drops in {path}")

print(f"Total files changed: {changed}")
