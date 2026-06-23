import re

with open('src/mem/slab.npk', 'r') as f:
    content = f.read()

# Replace signatures for functions that return Result<int64>
signatures_to_fix = [
    'pub func:mem_init = int64()',
    'pub func:slab_alloc = int64(int64:n)',
    'pub func:slab_alloc_zero = int64(int64:n)',
    'pub func:mem_malloc = int64(int64:n)',
    'pub func:mem_free = int64(int64:ptr)'
]

for sig in signatures_to_fix:
    new_sig = sig.replace('int64', 'Result<int64>', 1)
    content = content.replace(sig, new_sig)

with open('src/mem/slab.npk', 'w') as f:
    f.write(content)
