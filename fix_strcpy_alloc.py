import re

with open('src/str/strcpy.npk', 'r') as f:
    c = f.read()

c = re.sub(r'Result<int64>:r = slab_alloc\(alloc_size\);\n\s*if \(r\.is_error\) \{\n\s*fail r\.error;\n\s*\}', r'int64:r = slab_alloc(alloc_size);\n    if (r == 0i64) {\n        fail @cast_unchecked<tbb32>(12i64);\n    }', c)

with open('src/str/strcpy.npk', 'w') as f:
    f.write(c)

