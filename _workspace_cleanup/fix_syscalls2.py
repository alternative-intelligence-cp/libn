import re
with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

content = content.replace('pass raw sys_safe(', 'pass sys_safe(')
content = content.replace('pass raw sys_full(', 'pass sys_full(')

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
