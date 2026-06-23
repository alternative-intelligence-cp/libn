import re
from collections import Counter

with open("build.log", "r") as f:
    text = f.read()

errors = re.findall(r'error: Line \d+, Column \d+: (.*)', text)
c = Counter(errors)
for msg, count in c.most_common():
    print(f"{count}: {msg}")
