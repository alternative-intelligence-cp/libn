import re

def fix_slab_sigs():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk'
    with open(path, 'r') as f:
        content = f.read()

    content = content.replace('pub func:libn_slab_alloc = int64(int64:n) {', 'pub func:libn_slab_alloc = Result<int64>(int64:n) {')
    content = content.replace('pub func:libn_slab_alloc_zero = int64(int64:n) {', 'pub func:libn_slab_alloc_zero = Result<int64>(int64:n) {')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_mmap_sigs():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk'
    with open(path, 'r') as f:
        content = f.read()

    content = content.replace('pub func:mem_malloc = int64(int64:n) {', 'pub func:mem_malloc = Result<int64>(int64:n) {')
    content = content.replace('pub func:mem_calloc = int64(int64:n, int64:size) {', 'pub func:mem_calloc = Result<int64>(int64:n, int64:size) {')
    content = content.replace('pub func:mem_realloc = int64(int64:ptr, int64:new_size) {', 'pub func:mem_realloc = Result<int64>(int64:ptr, int64:new_size) {')
    
    with open(path, 'w') as f:
        f.write(content)

fix_slab_sigs()
fix_mmap_sigs()
