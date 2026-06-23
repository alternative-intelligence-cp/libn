import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()

            # Remove 'raw ' from func declarations: `func:name = raw Type(`
            new_content = re.sub(r'(func:\w+\s*=\s*)raw\s+([a-zA-Z0-9_<>]+)\s*\(', r'\1\2(', content)

            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed decls in {path}")
