import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = re.sub(r'\bsys_read\b', 'libn_read', content)
            new_content = re.sub(r'\bsys_write\b', 'libn_write', new_content)
            new_content = re.sub(r'\bsys_open\b', 'libn_open', new_content)
            new_content = re.sub(r'\bsys_close\b', 'libn_close', new_content)
            new_content = re.sub(r'\bsys_lseek\b', 'libn_lseek', new_content)
            new_content = re.sub(r'\bERR_RANGE\b', 'ERANGE', new_content)
            new_content = re.sub(r'\berrno_get\b', 'libn_errno_get', new_content)
            new_content = re.sub(r'\bstr_snprintf5\b', 'str_snprintf8', new_content)
            new_content = re.sub(r'\bstr_snprintf7\b', 'str_snprintf8', new_content)
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed identifiers in {path}")

print("Done")
