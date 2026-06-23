import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"
target_lines = [164, 165, 236, 237, 279, 280]

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                lines = f.readlines()
            
            for line_num in target_lines:
                idx = line_num - 1
                if idx < len(lines):
                    line_str = lines[idx]
                    # Print lines with [
                    if '[' in line_str:
                        print(f"File {path}, Line {line_num}: {line_str.strip()}")

