import re

with open('/home/randy/Workspace/REPOS/libn/src/mem/slab.npk', 'r') as f:
    text = f.read()

# Fix slab_alloc signature and returns
text = text.replace('pub func:slab_alloc = int64(int64:n)', 'pub func:slab_alloc = Result<int64>(int64:n)')
text = text.replace('pass n;', 'pass r;')

# Fix slab_refill usage
text = re.sub(r'int64:rr = slab_refill\(cls\);\n\s*if \(rr\.is_error\) \{', 
              r'Result<int64>:rr = slab_refill(cls);\n        if (rr.is_error) {', text)
text = text.replace('int64:rr = slab_refill(n);\n        if (rr.is_error) {',
                    'Result<int64>:rr = slab_refill(n);\n        if (rr.is_error) {')

# Fix int64->next_ptr
text = text.replace('int64:next = raw next_ptr[0];', 'int64:next = next_ptr[0];')
text = text.replace('slab_freelist_set(n, n);', 'slab_freelist_set(cls, next);')

# Fix slab_free signature
text = text.replace('pub func:slab_free = int64(int64:ptr)', 'pub func:slab_free = Result<NIL>(int64:ptr)')
text = text.replace('int64:r = mem_free(ptr);\n        pass hdr;', 'Result<NIL>:r = mem_free(ptr);\n        pass r;')

# Fix slab_alloc_zero signature
text = text.replace('pub func:slab_alloc_zero = int64(int64:n)', 'pub func:slab_alloc_zero = Result<int64>(int64:n)')
text = text.replace('int64:r = slab_alloc(n);\n    if (r->is_error) {\n        fail r.error;\n    }\n    int64:ptr = r->value;', 
                    'Result<int64>:r = slab_alloc(n);\n    if (r.is_error) {\n        fail r.error;\n    }\n    int64:ptr = r.value;')
text = text.replace('uint8->:p    = @cast_unchecked<uint8->>(r);', 'uint8->:p    = @cast_unchecked<uint8->>(ptr);')
text = text.replace('int64:sz   = slab_class_size(r);', 'int64:sz   = slab_class_size(cls);')
text = text.replace('while (zi < zi)', 'while (zi < sz)')

# Fix slab_refill loop variables
text = text.replace('int64:slab_base = i->value;', 'int64:slab_base = r.value;')

# Fix map methods in sizes? Wait, slab doesn't use map.
text = text.replace('map.size()', 'map_size') # Wait, earlier error: "Type 'map' has no method 'size'"
# Let's check slab.npk for map_size. The error was Line 298: Type 'map' has no method 'size'
# Line 308: Type 'map' has no method 'size'

with open('/home/randy/Workspace/REPOS/libn/src/mem/slab.npk', 'w') as f:
    f.write(text)

