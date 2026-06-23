import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = re.sub(r'\nfunc:to_lower_ascii =', '\npub func:to_lower_ascii =', content)
            new_content = re.sub(r'\nfunc:charset_build =', '\npub func:charset_build =', new_content)
            new_content = re.sub(r'\nfunc:charset_test =', '\npub func:charset_test =', new_content)
            
            # slab_free(ptr) -> slab_free(0i64, ptr) if it's missing the handle
            new_content = re.sub(r'\bslab_free\(([^,]+)\)', r'slab_free(0i64, \1)', new_content)
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed in {path}")
