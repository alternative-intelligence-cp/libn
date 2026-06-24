import re

def fix_slab():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk'
    with open(path, 'r') as f:
        content = f.read()

    # Fix includes
    if 'use "../mem/memcpy.npk".*;' not in content:
        content = content.replace('use "../mem/mmap.npk".*;\n', 'use "../mem/mmap.npk".*;\nuse "../mem/memcpy.npk".*;\n')

    # Fix int64:r = libn_slab_alloc(n) -> int64:r = raw libn_slab_alloc(n)
    content = content.replace('int64:r = libn_slab_alloc(n);', 'int64:r = raw libn_slab_alloc(n);')
    content = content.replace('int64:new_ptr = libn_slab_alloc(n);', 'int64:new_ptr = raw libn_slab_alloc(n);')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_memset():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/memset.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    # fix drop(memset(...)) -> int8->:ignored = memset(...)
    content = content.replace('drop(memset(ptr, c, n));', 'int8->:ign = memset(ptr, c, n);')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_memcpy():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/memcpy.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace('drop(mcpy(dst, src, num_bytes));', 'int8->:ign = mcpy(dst, src, num_bytes);')
    content = content.replace('drop(mmov(dst, src, num_bytes));', 'int8->:ign = mmov(dst, src, num_bytes);')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_fopen():
    path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    # Line 81: int64:buf = bio_alloc_buf(BUFSIZ); -> raw
    content = content.replace('int64:buf = bio_alloc_buf(BUFSIZ);', 'int64:buf = raw bio_alloc_buf(BUFSIZ);')
    
    # Line 139 / 160: Function expects 1 argument(s), but 2 provided
    # Wait, bio_init_stream expects 4 arguments!
    # Ah! In fopen.npk, bio_alloc_file returns Result<int64> maybe?
    # No, bio_alloc_file has no arguments.
    # Where is an error in fopen.npk? Let's fix bio_init_stream?
    # wait, I will check what else expects 1 argument.
    
    with open(path, 'w') as f:
        f.write(content)

fix_slab()
fix_memset()
fix_memcpy()
fix_fopen()
