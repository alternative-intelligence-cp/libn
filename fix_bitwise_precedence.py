import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Look for expressions like `something & 7i64 != 0i64`
            # Specifically `(s + i) & 7i64 != 0i64`
            # And `((a + i) | (b + i)) & 7i64 != 0i64`
            new_content = content.replace('(s + i) & 7i64 != 0i64', '((s + i) & 7i64) != 0i64')
            new_content = new_content.replace('(((a + i) | (b + i)) & 7i64 != 0i64', '((((a + i) | (b + i)) & 7i64) != 0i64')
            new_content = new_content.replace('((a + i) | (b + i)) & 7i64 != 0i64', '((((a + i) | (b + i)) & 7i64) != 0i64')
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed precedence in {path}")

