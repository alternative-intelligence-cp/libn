import re

path = '/home/randy/Workspace/REPOS/libn/src/str/strcpy.npk'
with open(path, 'r') as f:
    content = f.read()

orig1 = """    int64:r = slab_alloc(alloc_size);
    if (r.is_error) {
        fail r.error;
    }

      // Copy including NUL terminator
    drop mem_memcpy(r.value, src, alloc_size);
    pass r.value;"""
new1 = """    int64:r = slab_alloc(alloc_size);
    if (r == 0i64) {
        fail @cast_unchecked<tbb32>(ENOMEM);
    }

      // Copy including NUL terminator
    drop mem_memcpy(r, src, alloc_size);
    pass r;"""

orig2 = """    int64:r = slab_alloc(alloc_size);
    if (r.is_error) {
        fail r.error;
    }

      // Copy actual_len bytes, then NUL-terminate
    drop mem_memcpy(r.value, src, actual_len);
    (@cast_unchecked<uint8->>(r.value))[actual_len] = 0u8;
    pass r.value;"""
new2 = """    int64:r = slab_alloc(alloc_size);
    if (r == 0i64) {
        fail @cast_unchecked<tbb32>(ENOMEM);
    }

      // Copy actual_len bytes, then NUL-terminate
    drop mem_memcpy(r, src, actual_len);
    (@cast_unchecked<uint8->>(r))[actual_len] = 0u8;
    pass r;"""

content = content.replace(orig1, new1).replace(orig2, new2)

with open(path, 'w') as f:
    f.write(content)

print("Fixed strcpy")
