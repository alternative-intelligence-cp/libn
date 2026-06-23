import sys
with open('test_root.npk', 'r') as f:
    lines = f.readlines()

with open('build_output.txt', 'r') as f:
    output = f.read()

import re
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
output = ansi_escape.sub('', output)

for line in output.split('\n'):
    if 'error:' in line and 'Cannot ' in line:
        m = re.search(r'Line (\d+),', line)
        if m:
            ln = int(m.group(1))
            print("--- Error at line", ln, "---")
            print(line)
            start = max(0, ln - 2)
            end = min(len(lines), ln + 1)
            for i in range(start, end):
                print(f"{i+1}: {lines[i].rstrip()}")
