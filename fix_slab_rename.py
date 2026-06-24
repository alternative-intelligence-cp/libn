import os
def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Fix file.npk
    if 'file.npk' in path:
        content = content.replace('slab_free(0i64, ', 'slab_free(')
    
    # Rename functions
    content = content.replace('func:slab_free', 'func:libn_slab_free')
    content = content.replace('func:slab_alloc', 'func:libn_slab_alloc')
    content = content.replace('func:slab_realloc', 'func:libn_slab_realloc')
    
    content = content.replace('slab_free(', 'libn_slab_free(')
    content = content.replace('slab_alloc(', 'libn_slab_alloc(')
    content = content.replace('slab_realloc(', 'libn_slab_realloc(')
    
    with open(path, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))
