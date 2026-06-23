import re

with open('compile_errors.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Strip ansi codes
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
text = ansi_escape.sub('', text)

errors = []
for line in text.split('\n'):
    line = line.strip()
    if 'error: Line' in line:
        m = re.search(r'error: Line \d+, Column \d+: (.*)', line)
        if m:
            errors.append(m.group(1))

from collections import Counter
for err, count in Counter(errors).most_common():
    print(f"{count}x: {err}")
