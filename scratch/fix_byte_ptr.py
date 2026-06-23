import os
import glob
import re

src_dir = '/home/randy/Workspace/REPOS/libn/src'
npk_files = glob.glob(os.path.join(src_dir, '**', '*.npk'), recursive=True)

for filepath in npk_files:
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = re.sub(r'\*byte', 'uint8->', content)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
