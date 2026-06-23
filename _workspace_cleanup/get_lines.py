import re
import os

def expand_file(filepath, lines_out, visited):
    if filepath in visited: return
    visited.add(filepath)
    with open(filepath, 'r') as f:
        content = f.read()
    # remove block comments since they might contain uses
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    for line in content.split('\n'):
        # single line comments are preserved but we don't process uses inside them
        m = re.match(r'^\s*use\s+"([^"]+)".*;', line)
        if m:
            expand_file(m.group(1), lines_out, visited)
        else:
            lines_out.append((filepath, line))

lines = []
expand_file("test_root.npk", lines, set())

targets = [308, 309, 310, 325, 326, 327, 342, 343, 344]
for t in targets:
    if t <= len(lines):
        print(f"Global {t} = {lines[t-1][0]}: {lines[t-1][1].strip()}")
