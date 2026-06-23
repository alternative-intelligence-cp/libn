import re

with open("build.log", "r") as f:
    text = f.read()

errors = re.findall(r'([A-Za-z0-9_./]+):(\d+):\d+: error: Line (\d+), Column \d+: (Cannot compare incompatible types: \'byte\' and \'uint8\')', text)
for e in errors[:5]:
    print(e)

errors2 = re.findall(r'([A-Za-z0-9_./]+):(\d+):\d+: error: Line (\d+), Column \d+: (Cannot assign value of type \'uint8\' to variable of type \'byte\')', text)
for e in errors2[:5]:
    print(e)
