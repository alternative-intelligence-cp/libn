import re

def fix_fprintf_imports():
    path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk'
    with open(path, 'r') as f:
        content = f.read()

    if 'use "../../mem/memcpy.npk".*;' not in content:
        content = content.replace('use "../../mem/mmap.npk".*;\n', 'use "../../mem/mmap.npk".*;\nuse "../../mem/memcpy.npk".*;\n')
    
    with open(path, 'w') as f:
        f.write(content)

fix_fprintf_imports()
