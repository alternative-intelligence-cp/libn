import re

# math.npk: limit -> max_len
with open('src/math/math.npk', 'r') as f:
    c = f.read()
c = re.sub(r'\blimit\b', 'max_len', c)
with open('src/math/math.npk', 'w') as f:
    f.write(c)

# strfmt.npk
with open('src/str/strfmt.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'struct FmtState {' in lines[i]:
        lines[i] = lines[i].replace('struct FmtState {', 'struct:FmtState = {')
    elif '?' in lines[i] and ':' in lines[i] and 'int64:' not in lines[i]:
        # just print to see
        print(f"strfmt.npk:{i+1}: {lines[i].strip()}")
        # Let's fix specific lines based on what they are
with open('src/str/strfmt.npk', 'w') as f:
    f.writelines(lines)

# fopen.npk
with open('src/io/bio/fopen.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if '?' in lines[i] and ':' in lines[i]:
        print(f"fopen.npk:{i+1}: {lines[i].strip()}")
with open('src/io/bio/fopen.npk', 'w') as f:
    f.writelines(lines)

# strchr.npk
with open('src/str/strchr.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'while n >' in lines[i]:
        lines[i] = lines[i].replace('while n >', 'while (n >').replace('{', ') {')
with open('src/str/strchr.npk', 'w') as f:
    f.writelines(lines)

