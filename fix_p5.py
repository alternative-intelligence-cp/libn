import re

def fix_slab():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk'
    with open(path, 'r') as f:
        content = f.read()

    if 'use "../syscall/syscall.npk".*;' not in content:
        content = content.replace('use "../syscall/errno.npk".*;\n', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\n')
    
    with open(path, 'w') as f:
        f.write(content)

fix_slab()
