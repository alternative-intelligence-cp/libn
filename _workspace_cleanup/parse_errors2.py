import re

with open("build.log", "r") as f:
    text = f.read()

errors = re.findall(r'([A-Za-z0-9_./]+):(\d+):\d+: error: Line \d+, Column \d+: (Undefined identifier: .*)', text)
for e in errors:
    print(f"{e[0]}: {e[2]}")
    break
