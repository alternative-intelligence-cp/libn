import re, os

errors = []
with open('build_errors.txt', 'r') as f:
    for line in f:
        line = re.sub(r'\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]', '', line).strip()
        if 'error: Line ' in line:
            m = re.search(r'Line (\d+), Column (\d+): (.*)', line)
            if m:
                errors.append((int(m.group(1)), m.group(3)))

files = []
for r, d, f in os.walk('src'):
    for file in f:
        if file.endswith('.npk'):
            files.append(os.path.join(r, file))

for line_num, msg in errors:
    print(f"--- Error: {msg} (Line {line_num})")
    for f in files:
        with open(f, 'r') as file:
            lines = file.readlines()
            if line_num <= len(lines):
                content = lines[line_num - 1].strip()
                if content and not content.startswith('//'):
                    print(f"  {f}:{line_num}: {content}")
