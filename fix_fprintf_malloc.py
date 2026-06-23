import re

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk'
with open(path, 'r') as f:
    content = f.read()

# Replace int64:p = mem_malloc with Result<int64>:r_p = mem_malloc
content = re.sub(r'int64:p\s*=\s*mem_malloc\(([^)]+)\);', r'int64:p = raw mem_malloc(\1);', content)

with open(path, 'w') as f:
    f.write(content)

print("Fixed mem_malloc unwraps in fprintf.npk")
