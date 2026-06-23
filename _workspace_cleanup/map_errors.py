import os

lines_to_find = [174, 196, 216, 219, 285, 355, 356, 359, 365, 368, 372, 226, 100, 62, 72, 105, 116, 171, 172, 177, 179, 204, 205, 210, 211, 213, 86, 87, 263, 168, 169, 73, 74, 268, 269, 273]

files = []
for root, dirs, filenames in os.walk('src'):
    for filename in filenames:
        if filename.endswith('.npk'):
            files.append(os.path.join(root, filename))

for line_num in set(lines_to_find):
    print(f"--- Line {line_num} ---")
    for filepath in files:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if line_num <= len(lines):
                content = lines[line_num - 1].strip()
                if content:
                    print(f"  {filepath}:{line_num}: {content}")
