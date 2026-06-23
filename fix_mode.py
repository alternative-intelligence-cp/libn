import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()

            new_content = content
            
            fields = ['mode']
            for field in fields:
                new_content = re.sub(r'\bf\.' + field + r'\b', 'f->' + field, new_content)
                new_content = re.sub(r'\bcurr_f\.' + field + r'\b', 'curr_f->' + field, new_content)
                new_content = re.sub(r'\bsin\.' + field + r'\b', 'sin->' + field, new_content)
                new_content = re.sub(r'\bsout\.' + field + r'\b', 'sout->' + field, new_content)
                new_content = re.sub(r'\bserr\.' + field + r'\b', 'serr->' + field, new_content)

            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed mode in {path}")

