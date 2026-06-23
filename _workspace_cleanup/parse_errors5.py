import re

with open("build.log", "r") as f:
    text = f.read()

errors = re.findall(r'([A-Za-z0-9_./]+):(\d+):\d+: error: Line (\d+), Column \d+: (Bitwise operators require same integer type on both sides. Got \'int64\' and \'uint8\'.)', text)
for e in set(errors):
    print(e)
