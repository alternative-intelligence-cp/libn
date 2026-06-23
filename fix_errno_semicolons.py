path = 'src/syscall/errno.npk'
with open(path, 'r') as f:
    lines = f.readlines()

def fix_line(num):
    idx = num - 1
    if lines[idx].strip() == '}':
        lines[idx] = lines[idx].replace('}', '};')

# These lines have } that end functions
fix_line(242)
fix_line(253)
fix_line(263)
fix_line(367)
fix_line(379)
fix_line(389)
fix_line(396)
fix_line(399)

with open(path, 'w') as f:
    f.writelines(lines)
