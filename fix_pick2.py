import re

with open('src/syscall/errno.npk', 'r') as f:
    text = f.read()

# We know the block starts with `pick e {` and ends with `}`.
start = text.find('pick e {')
end = text.find('    }', start)

pick_block = text[start:end+5]

lines = pick_block.split('\n')
new_lines = []

first = True
for line in lines:
    m = re.match(r'\s*([0-9]+i64)\s*=>\s*pass\s+(".+");', line)
    if m:
        val = m.group(1)
        msg = m.group(2)
        if first:
            new_lines.append(f'    if (e == {val}) {{ pass {msg}; }}')
            first = False
        else:
            new_lines.append(f'    else if (e == {val}) {{ pass {msg}; }}')
    elif re.match(r'\s*_\s*=>\s*pass\s+(".+");', line):
        m2 = re.match(r'\s*_\s*=>\s*pass\s+(".+");', line)
        msg = m2.group(1)
        new_lines.append(f'    else {{ pass {msg}; }}')
    elif 'pick e {' not in line and '}' not in line and line.strip():
        # Keep comments
        new_lines.append(line)

new_block = '\n'.join(new_lines)
text = text[:start] + new_block + text[end+5:]

with open('src/syscall/errno.npk', 'w') as f:
    f.write(text)

