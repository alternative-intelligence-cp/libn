import re

path = '/home/randy/Workspace/REPOS/libn/src/io/printf.npk'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('@cast_unchecked<uint8->>(num_buf)', '@cast_unchecked<uint8->>(@num_buf[0])')

with open(path, 'w') as f:
    f.write(content)
print("Fixed printf")
