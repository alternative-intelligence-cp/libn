import os
import re
from collections import defaultdict

with open("compile_output_clean.txt", "r") as f:
    output = f.read()

errors = []
for line in output.split('\n'):
    m = re.search(r'Line (\d+), Column (\d+): (.*)', line)
    if m:
        errors.append((int(m.group(1)), int(m.group(2)), m.group(3)))

src_dir = "/home/randy/Workspace/REPOS/libn/src"
files_map = {} # path -> list of lines
for root, _, files in os.walk(src_dir):
    for f in files:
        if f.endswith(".npk"):
            path = os.path.join(root, f)
            with open(path, "r") as file:
                files_map[path] = file.readlines()

file_errors = defaultdict(list)

# Map errors to files
for l, c, msg in errors:
    idx = l - 1
    col = c - 1
    
    matched_files = []
    
    if "Member access (.) requires struct" in msg:
        for path, lines in files_map.items():
            if idx < len(lines):
                line_text = lines[idx]
                if col < len(line_text) and line_text[col] == '.':
                    matched_files.append((path, "dot"))
                    
    elif "Undefined identifier:" in msg and "Did you mean" in msg:
        m2 = re.search(r"Undefined identifier: '(.*?)'\. Did you mean '(.*?)'\?", msg)
        if m2:
            old_id = m2.group(1)
            new_id = m2.group(2)
            for path, lines in files_map.items():
                if idx < len(lines):
                    line_text = lines[idx]
                    if line_text[col:col+len(old_id)] == old_id:
                        matched_files.append((path, ("rename", old_id, new_id)))

    # Only assign if exactly 1 file matches
    if len(matched_files) == 1:
        path, action = matched_files[0]
        file_errors[path].append((l, c, action))

# Apply fixes from bottom to top to avoid column shifting
for path, errs in file_errors.items():
    lines = files_map[path]
    errs.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    for l, c, action in errs:
        idx = l - 1
        col = c - 1
        new_line = lines[idx]
        
        if action == "dot":
            new_line = new_line[:col] + "->" + new_line[col+1:]
        elif isinstance(action, tuple) and action[0] == "rename":
            old_id = action[1]
            new_id = action[2]
            new_line = new_line[:col] + new_id + new_line[col+len(old_id):]
            
        lines[idx] = new_line
        
    with open(path, "w") as f:
        f.writelines(lines)

print(f"Applied fixes to {len(file_errors)} files.")
