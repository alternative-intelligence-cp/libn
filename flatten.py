import os

with open('/home/randy/Workspace/REPOS/libn/src/all.npk', 'r') as f:
    all_lines = f.readlines()

out = []
for line in all_lines:
    out.append(line)
    if line.startswith('use "'):
        filename = line.split('"')[1]
        with open(filename, 'r') as inc:
            out.extend(inc.readlines())

with open('/tmp/flat.npk', 'w') as f:
    f.writelines(out)
