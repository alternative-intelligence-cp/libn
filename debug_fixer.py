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
files_map = {} 
for root, _, files in os.walk(src_dir):
    for f in files:
        if f.endswith(".npk"):
            path = os.path.join(root, f)
            with open(path, "r") as file:
                files_map[path] = file.readlines()

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
        if len(matched_files) != 1:
            print(f"Failed dot match at L{l} C{c}: len={len(matched_files)}")
            # Show the character at the given column for all files that have enough length
            chars = []
            for path, lines in files_map.items():
                if idx < len(lines) and col < len(lines[idx]):
                    chars.append(lines[idx][col])
            print(f"Chars found: {set(chars)[:10]}")
            break
