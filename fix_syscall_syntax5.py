with open('src/syscall/syscall.npk', 'r') as f:
    s = f.read()

s = s.replace(')) {', ') {')
s = s.replace('};;', '};')

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(s)
