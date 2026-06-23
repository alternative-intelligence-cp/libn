import os
src_dir = "/home/randy/Workspace/REPOS/libn/src"
target_lines = [54, 61, 79, 94, 96, 118]
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                lines = f.readlines()
            for line_num in target_lines:
                idx = line_num - 1
                if idx < len(lines):
                    if "==" in lines[idx] or "!=" in lines[idx]:
                        print(f"File {path}, Line {line_num}: {lines[idx].strip()}")
