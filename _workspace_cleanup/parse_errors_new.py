import os
import re

with open('compile_errors.txt', 'r') as f:
    lines = f.readlines()

errors = []
for line in lines:
    line = line.strip()
    if 'test_root.npk:0:0: error:' in line:
        # Extract the error message after the line number
        m = re.search(r'test_root\.npk:0:0: error:\s*Line\s*\d+,\s*Column\s*\d+:\s*(.*)', line)
        if m:
            errors.append(m.group(1))

from collections import Counter
counts = Counter(errors)
for err, count in counts.most_common():
    print(f"{count}x: {err}")
