import os

with open('src/proc/exec.npk', 'r') as f:
    lines = f.readlines()

out = []
for line in lines:
    if line.startswith('extern int64:environ;'):
        out.append('use "src/proc/env.npk".*;\n')
    else:
        out.append(line)

with open('src/proc/exec.npk', 'w') as f:
    f.writelines(out)

