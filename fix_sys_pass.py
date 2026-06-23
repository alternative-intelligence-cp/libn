import os
import re

filepath = "/home/randy/Workspace/REPOS/libn/src/syscall/syscall.npk"

with open(filepath, 'r') as f:
    content = f.read()

# Replace `pass raw sys_safe` with `return sys_safe`
content = re.sub(r'pass\s+raw\s+sys_safe', 'return sys_safe', content)
content = re.sub(r'pass\s+raw\s+sys_full', 'return sys_full', content)

with open(filepath, 'w') as f:
    f.write(content)

print(f"Fixed passes in {filepath}")
