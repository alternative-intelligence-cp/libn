import os
import re

file_path = '/home/randy/Workspace/REPOS/libn/src/syscall/syscall.npk'
with open(file_path, 'r') as f:
    content = f.read()

# Add raw() back to sys!!(...) but NOT sys!!!(...)
# We only want to wrap sys!!(...)
content = re.sub(r'int64:ret = sys!!\((.*?)\);', r'int64:ret = raw(sys!!(\1));', content)

with open(file_path, 'w') as f:
    f.write(content)
print("Added raw to sys!! in syscall.npk")
