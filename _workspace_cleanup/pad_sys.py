import re

def pad_sys(match):
    inner = match.group(1)
    commas = inner.count(',')
    needed = 6 - commas
    if needed > 0:
        return 'sys(' + inner + ', 0i64' * needed + ')'
    return match.group(0)

with open('src/mem/mmap.npk', 'r') as f:
    content = f.read()

content = re.sub(r'sys\(([^()]+)\)', pad_sys, content)

with open('src/mem/mmap.npk', 'w') as f:
    f.write(content)
