with open('src/proc/exec.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'extern { int64:environ; };' in lines[i]:
        lines[i] = 'extern "C" { int64:environ; };\n'
with open('src/proc/exec.npk', 'w') as f:
    f.writelines(lines)

with open('src/fs/path.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if '?' in lines[i] and ':' in lines[i] and '//' not in lines[i]:
        print(f"path.npk:{i+1}: {lines[i].strip()}")

with open('src/io/bio/fstate.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if '?' in lines[i] and ':' in lines[i] and '//' not in lines[i]:
        print(f"fstate.npk:{i+1}: {lines[i].strip()}")

with open('src/str/strbuf.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'struct StrBuf {' in lines[i]:
        lines[i] = 'struct:StrBuf = {\n'
    elif '?' in lines[i] and ':' in lines[i] and '//' not in lines[i]:
        print(f"strbuf.npk:{i+1}: {lines[i].strip()}")
with open('src/str/strbuf.npk', 'w') as f:
    f.writelines(lines)

