import os
import re

allocators = ['mem_malloc', 'mem_calloc', 'mem_realloc', 'libn_slab_alloc', 'libn_slab_alloc_zero', 'libn_slab_realloc']

def fix_mmap():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk'
    with open(path, 'r') as f: content = f.read()
    
    # Ensure raw is used for allocator calls
    for alloc in allocators:
        content = re.sub(r'(?<!raw )(?<!func:)(?<!pub func:)\b' + alloc + r'\s*\(', r'raw ' + alloc + '(', content)

    # Fix the pass new_map + ALLOC_HEADER_SIZE;
    content = content.replace('        pass new_map + ALLOC_HEADER_SIZE;\n', 
                              '        Result<int64>:_ret1 = new_map + ALLOC_HEADER_SIZE;\n        pass _ret1;\n')

    with open(path, 'w') as f: f.write(content)

def fix_slab():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk'
    with open(path, 'r') as f: content = f.read()

    # Ensure raw is used for allocator calls
    for alloc in allocators:
        content = re.sub(r'(?<!raw )(?<!func:)(?<!pub func:)\b' + alloc + r'\s*\(', r'raw ' + alloc + '(', content)

    # Fix the pass user_ptr;
    content = content.replace('    pass user_ptr;\n', '    Result<int64>:_ret1 = user_ptr;\n    pass _ret1;\n')
    
    # Fix pass ptr;
    content = content.replace('    pass ptr;\n', '    Result<int64>:_ret2 = ptr;\n    pass _ret2;\n')
    content = content.replace('            pass ptr;\n', '            Result<int64>:_ret3 = ptr;\n            pass _ret3;\n')

    # Fix pass new_ptr;
    content = content.replace('    pass new_ptr;\n', '    Result<int64>:_ret4 = new_ptr;\n    pass _ret4;\n')

    with open(path, 'w') as f: f.write(content)

fix_mmap()
fix_slab()
