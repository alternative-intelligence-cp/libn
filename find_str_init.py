import os

src_dir = "/home/randy/Workspace/REPOS/libn/src"
target_lines = [163, 50, 51, 235, 278]

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
                    if '@"' in line_str and not line_str.startswith('//'):
                        print(f"File {path}, Line {line_num}: {line_str}")

