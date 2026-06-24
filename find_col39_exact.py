import os
import glob

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if '==' in line or '!=' in line:
                    if len(line) >= 40:
                        op_idx = -1
                        if '==' in line:
                            op_idx = line.find('==')
                        elif '!=' in line:
                            op_idx = line.find('!=')
                        
                        if op_idx == 38 or op_idx == 39 or op_idx == 37:
                            print(f"{filepath}:{i}: {line.rstrip()}")

