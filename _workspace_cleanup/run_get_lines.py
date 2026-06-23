import re
import os

with open("clean_errors.txt", "r") as f:
    errors = f.readlines()

targets = []
for line in errors:
    if "Cannot assign value of type 'Result<int64>' to variable of type 'int64'" in line:
        m = re.search(r'Line (\d+)', line)
        if m:
            targets.append(int(m.group(1)))

def expand_file(filepath, lines_out, visited):
    if filepath in visited: return
    visited.add(filepath)
    with open(filepath, 'r') as f:
        content = f.read()
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    for line in content.split('\n'):
        m = re.match(r'^\s*use\s+"([^"]+)".*;', line)
        if m:
            expand_file(m.group(1), lines_out, visited)
        else:
            lines_out.append((filepath, line))

lines = []
expand_file("test_root.npk", lines, set())

for t in targets:
    if t <= len(lines):
        print(f"Global {t} = {lines[t-1][0]}: {lines[t-1][1].strip()}")
