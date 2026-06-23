import re

with open("build.log", "r") as f:
    text = f.read()

errors = re.findall(r'([A-Za-z0-9_./]+):(\d+):\d+: error: Line \d+, Column \d+: (Cannot compare incompatible types: \'byte\' and \'uint8\')', text)
print(set(errors))

errors2 = re.findall(r'([A-Za-z0-9_./]+):(\d+):\d+: error: Line (\d+), Column \d+: (Undefined identifier: \'.*\')', text)
# Just print the first 10 undefined identifiers with line numbers
for e in errors2[:10]:
    print(e)
