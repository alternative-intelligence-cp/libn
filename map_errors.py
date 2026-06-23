import os
import re

# Simulate the `use` expansion to build line mapping
merged_lines = []
line_map = {} # merged_line_idx -> (filename, orig_line_idx, line_text)

def expand_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        m = re.match(r'^use\s+"([^"]+)"\.\*;\s*$', line.strip())
        if m:
            dep_path = m.group(1)
            # In our case we changed them to absolute paths, let's open them
            expand_file(dep_path)
            # the use statement itself is replaced? Let's see. In C #include, the line is replaced by the file.
        else:
            merged_idx = len(merged_lines)
            merged_lines.append(line)
            line_map[merged_idx] = (filepath, i, line)

expand_file("test_all.npk")

print(f"Total merged lines: {len(merged_lines)}")
# Check line 79 to see if it matches "ERR_EOF"
if 78 in line_map:
    f, l, txt = line_map[78]
    print(f"Line 79: {f}:{l+1} -> {txt.strip()}")
    
if 174 in line_map:
    f, l, txt = line_map[173]
    print(f"Line 174: {f}:{l+1} -> {txt.strip()}")
