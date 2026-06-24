import os

def revert_signatures():
    # mmap.npk
    path = '/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace('pub func:mem_malloc = Result<int64>(int64:n) {', 'pub func:mem_malloc = int64(int64:n) {')
    content = content.replace('pub func:mem_calloc = Result<int64>(int64:n, int64:size) {', 'pub func:mem_calloc = int64(int64:n, int64:size) {')
    content = content.replace('pub func:mem_realloc = Result<int64>(int64:ptr, int64:new_size) {', 'pub func:mem_realloc = int64(int64:ptr, int64:new_size) {')
    
    content = content.replace('    pass r;\n', '    pass r.value;\n')
    content = content.replace('    pass new_r;\n', '    pass new_r.value;\n')
    
    with open(path, 'w') as f:
        f.write(content)

    # slab.npk
    path = '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk'
    with open(path, 'r') as f:
        content = f.read()

    content = content.replace('pub func:libn_slab_alloc = Result<int64>(int64:n) {', 'pub func:libn_slab_alloc = int64(int64:n) {')
    content = content.replace('pub func:libn_slab_alloc_zero = Result<int64>(int64:n) {', 'pub func:libn_slab_alloc_zero = int64(int64:n) {')
    
    with open(path, 'w') as f:
        f.write(content)

def remove_raw_from_allocators():
    for root, dirs, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
        for file in files:
            if file.endswith('.npk'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                
                content = content.replace('raw mem_malloc', 'mem_malloc')
                content = content.replace('raw mem_calloc', 'mem_calloc')
                content = content.replace('raw mem_realloc', 'mem_realloc')
                content = content.replace('raw libn_slab_alloc', 'libn_slab_alloc')
                content = content.replace('raw libn_slab_alloc_zero', 'libn_slab_alloc_zero')
                
                with open(path, 'w') as f:
                    f.write(content)

revert_signatures()
remove_raw_from_allocators()
