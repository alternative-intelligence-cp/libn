path = 'src/syscall/errno.npk'
with open(path, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i] == '}\n':
        lines[i] = '};\n'
    elif lines[i] == '}':
        lines[i] = '};'

with open(path, 'w') as f:
    f.writelines(lines)
