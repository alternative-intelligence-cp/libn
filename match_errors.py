import re
import os

with open('build_errors.txt', 'r') as f:
    content = f.read()

# Remove ANSI codes
content = re.sub(r'\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]', '', content)
lines = content.split('\n')

errors = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'error: Line' in line or ('error:' in line and 'Column' in line):
        msg = line
        i += 1
        # skip over the line pointing to column ^
        while i < len(lines) and lines[i].strip() == '|':
            i+=1
            
        if i < len(lines) and ' | ' in lines[i]:
            literal = lines[i].split('|', 1)[1]
            errors.append((msg, literal))
    i += 1

files = []
for root, _, fs in os.walk('src'):
    for file in fs:
        if file.endswith('.npk'):
            files.append(os.path.join(root, file))

for msg, literal in errors:
    literal = literal.rstrip('\n\r')
    matched = False
    for path in files:
        with open(path, 'r') as f:
            f_content = f.read().split('\n')
        for idx, cl in enumerate(f_content):
            if literal in cl and len(literal.strip()) > 2:
                print(f"{path}:{idx+1}: {msg}")
                matched = True
                break
        if matched:
            break
    if not matched:
        print(f"UNKNOWN: {msg} (literal: {literal})")

