import re

counts = {}
with open('build_errors.txt', 'r') as f:
    for line in f:
        m = re.search(r'error: Line \d+, Column \d+: (.*)', line)
        if m:
            msg = m.group(1)
            # normalize msg
            msg = re.sub(r"'.*?'", "'X'", msg)
            counts[msg] = counts.get(msg, 0) + 1

for msg, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"{count}: {msg}")
