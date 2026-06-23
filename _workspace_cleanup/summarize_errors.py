import sys
import collections
import re

with open('build_output.txt', 'r') as f:
    lines = f.readlines()

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

errors = []
for line in lines:
    clean_line = ansi_escape.sub('', line)
    if 'error:' in clean_line:
        parts = clean_line.split('error:', 1)
        if len(parts) > 1:
            msg = parts[1].strip()
            msg = re.sub(r'^Line \d+, Column \d+: ', '', msg)
            errors.append(msg)

counts = collections.Counter(errors)
for e, c in counts.most_common(50):
    print(f"{c}: {e}")
