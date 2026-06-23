import os
import re

def rewrite(filepath, callback):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    new_content = callback(content)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

def fix_mmap(c):
    c = c.replace('pub func:mem_malloc = Result<int64>(int64:n)', 'pub func:mem_malloc = int64(int64:n)')
    c = c.replace('pub func:mem_malloc = Result<int64>(int64:size)', 'pub func:mem_malloc = int64(int64:size)')
    return c
rewrite('src/mem/mmap.npk', fix_mmap)

def fix_slab(c):
    c = c.replace('pub func:slab_alloc = Result<int64>(int64:n)', 'pub func:slab_alloc = int64(int64:n)')
    c = c.replace('pub func:slab_alloc_zero = Result<int64>(int64:n)', 'pub func:slab_alloc_zero = int64(int64:n)')
    
    # slab_alloc calling mem_malloc
    # int64:r_val = raw(mem_malloc(n));
    # if (r.is_error) { fail r.error; }
    # pass r.value;
    # We will just replace it with: pass mem_malloc(n);
    c = re.sub(r'int64:r_val = raw\(mem_malloc\(n\)\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*pass r\.value;', r'pass mem_malloc(n);', c)
    # also the original one in case it wasn't modified correctly
    c = re.sub(r'Result<int64>:r = mem_malloc\(n\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*pass r\.value;', r'pass mem_malloc(n);', c)

    # slab_alloc_zero calling slab_alloc
    c = re.sub(r'Result<int64>:r = slab_alloc\(n\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*int64:ptr = r\.value;', r'int64:ptr = slab_alloc(n);', c)

    # mem_malloc(c.size * count) inside slab.npk
    c = re.sub(r'int64:r_val = raw\(mem_malloc\(c\.size \* count\)\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*int64:p = r_val;', r'int64:p = mem_malloc(c.size * count);', c)
    c = re.sub(r'Result<int64>:r = mem_malloc\(c\.size \* count\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*int64:p = r\.value;', r'int64:p = mem_malloc(c.size * count);', c)

    # mem_malloc(c.size) inside slab.npk
    c = re.sub(r'int64:r_val = raw\(mem_malloc\(c\.size\)\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*int64:ptr = r_val;', r'int64:ptr = mem_malloc(c.size);', c)
    c = re.sub(r'Result<int64>:r = mem_malloc\(c\.size\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*int64:ptr = r\.value;', r'int64:ptr = mem_malloc(c.size);', c)

    return c
rewrite('src/mem/slab.npk', fix_slab)

def fix_strcpy(c):
    c = re.sub(r'Result<int64>:r = slab_alloc\(alloc_size\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*uint8->:p = @cast_unchecked<uint8->>\(r\.value\);', r'uint8->:p = @cast_unchecked<uint8->>(slab_alloc(alloc_size));', c)
    return c
rewrite('src/str/strcpy.npk', fix_strcpy)
