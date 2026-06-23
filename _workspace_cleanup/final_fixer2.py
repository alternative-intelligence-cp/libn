import os
import re

# 1. Fix missing sys_safe wrap in syscall.npk
with open('src/syscall/syscall.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'int64:ret = sys!!(nr, a1, a2, a3, a4, a5, a6);',
    'Result<int64>:r_sys = sys!!(nr, a1, a2, a3, a4, a5, a6);\n    if (r_sys.is_error) { fail r_sys.error; }\n    int64:ret = r_sys.value;'
)
with open('src/syscall/syscall.npk', 'w') as f:
    f.write(code)

# 2. Fix uint8 vs int64 bitwise op in memutil.npk
with open('src/mem/memutil.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'diff = diff | (@cast_unchecked<int64>(@cast_unchecked<int64>(pa[i]) ^ pb[i]));',
    'diff = diff | (@cast_unchecked<int64>(pa[i]) ^ @cast_unchecked<int64>(pb[i]));'
)
code = code.replace(
    'int64:tword = raw replicate_byte(c);',
    'int64:tword = raw replicate_byte(@cast_unchecked<uint8>(c));'
)
# And the commented variable declaration:
code = code.replace(
    '// Match is somewhere in this word — find exact uint8 int64:word_base = ptr + i + wi * 8i64;',
    '// Match is somewhere in this word — find exact uint8\n            int64:word_base = ptr + i + wi * 8i64;'
)
with open('src/mem/memutil.npk', 'w') as f:
    f.write(code)

# 3. Fix slab.npk
with open('src/mem/slab.npk', 'r') as f:
    code = f.read()
code = code.replace('head = slab_freelist_get(cls);', 'head = raw slab_freelist_get(cls);')
code = code.replace('int64:head = slab_freelist_get(cls);', 'int64:head = raw slab_freelist_get(cls);')
code = code.replace('Result<int64>:r = mem_slab_alloc(n);', 'int64:r = mem_slab_alloc(n);')
code = code.replace('Result<int64>:r = slab_alloc(n);', 'int64:r = mem_slab_alloc(n);')
code = code.replace('if (r.is_error) {\n            fail r.error;\n        }\n        pass r.value;', 'if (r == 0i64) {\n            fail @cast_unchecked<tbb8>(ERR_NOMEM);\n        }\n        pass r;')
code = code.replace('int64:sz = slab_get_class_size(cls);', 'int64:sz = raw slab_get_class_size(cls);')
# Replace any remaining slab_alloc with mem_slab_alloc
code = code.replace('slab_alloc_zero', 'mem_slab_alloc_zero')
code = code.replace('slab_alloc', 'mem_slab_alloc')
code = code.replace('mem_mem_slab_alloc', 'mem_slab_alloc') # Just in case

# Fix the rest of slab_alloc usages in the codebase
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                c = f.read()
            changed = False
            if 'slab_alloc_zero' in c:
                c = c.replace('slab_alloc_zero', 'mem_slab_alloc_zero')
                changed = True
            if 'slab_alloc(' in c:
                c = c.replace('slab_alloc(', 'mem_slab_alloc(')
                changed = True
            if changed:
                with open(filepath, 'w') as f:
                    f.write(c)

with open('src/mem/slab.npk', 'w') as f:
    f.write(code)

print("Applied final_fixer2.py")
