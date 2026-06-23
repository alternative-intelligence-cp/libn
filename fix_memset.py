import re
with open('/home/randy/Workspace/REPOS/libn/src/mem/memset.npk', 'r') as f:
    content = f.read()

content = content.replace('drop compiler_fence();', '// drop compiler_fence();')

with open('/home/randy/Workspace/REPOS/libn/src/mem/memset.npk', 'w') as f:
    f.write(content)
print("Fixed memset")
