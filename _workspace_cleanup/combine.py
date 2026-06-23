import os
import re

visited = set()
lines = []

def process_file(filepath):
    if filepath in visited:
        return
    visited.add(filepath)
    try:
        with open(filepath, "r") as f:
            content = f.readlines()
    except Exception as e:
        return

    for line in content:
        m = re.match(r'^\s*use\s+"([^"]+)".*;', line)
        if m:
            # Nitpick replaces the 'use' line with the contents of the imported file
            # Wait, does it replace it, or does it process it first?
            process_file(m.group(1))
        else:
            lines.append((filepath, line))

process_file("test_root.npk")

lines_to_check = [308, 309, 310, 325, 326, 327, 342, 343, 344]
for l in lines_to_check:
    if l <= len(lines):
        print(f"Global {l} -> {lines[l-1][0]}: {lines[l-1][1].strip()}")
