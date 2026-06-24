import os
import glob

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if '==' in line or '!=' in line or '<' in line or '>' in line:
                    if '0i64' in line or 'int64' in line:
                        print(f"{filepath}:{i}: {line.rstrip()}")

