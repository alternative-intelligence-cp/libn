import re

def fix_strcpy():
    path = '/home/randy/Workspace/REPOS/libn/src/str/strcpy.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace('int64:r = libn_slab_alloc(alloc_size);', 'int64:r = raw libn_slab_alloc(alloc_size);')
    
    with open(path, 'w') as f:
        f.write(content)

fix_strcpy()
