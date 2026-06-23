import re

out = []
current_file = "test_all.npk"

with open('compiler_errors.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    line = re.sub(r'\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]', '', line).strip()
    if line.startswith('[DEBUG parseFuncDecl]'):
        continue
    if "Failed to parse module" in line:
        m = re.search(r"'(.*?)'", line)
        if m: current_file = m.group(1)
    if "test_all.npk:0:0: error:" in line:
        out.append(f"{current_file} -> {line.split('error:', 1)[1].strip()}")

# print first 30 unique errors
seen = set()
for x in out:
    if x not in seen:
        print(x)
        seen.add(x)
        if len(seen) >= 30:
            break
