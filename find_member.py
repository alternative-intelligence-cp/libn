import os

src_dir = "/home/randy/Workspace/REPOS/libn/src"
target_lines = [360, 363, 171, 176, 178, 204, 209, 210, 212, 334]

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                lines = f.readlines()
            
            for line_num in target_lines:
                idx = line_num - 1
                if idx < len(lines):
                    line_str = lines[idx].strip()
                    if '.' in line_str and not line_str.startswith('//'):
                        print(f"File {path}, Line {line_num}: {line_str}")

