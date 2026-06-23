import os
src_dir = "/home/randy/Workspace/REPOS/libn/src"
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                lines = f.readlines()
            for line_num in [126, 133, 143, 173, 178, 187]:
                idx = line_num - 1
                if idx < len(lines):
                    line_str = lines[idx].strip()
                    if 'fp' in line_str:
                        print(f"File {path}, Line {line_num}: {line_str}")
