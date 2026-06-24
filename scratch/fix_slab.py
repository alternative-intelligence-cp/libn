import re

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

# Fix imports
text = text.replace('use "../mem/mmap.npk".*;', 'use "../mem/mmap.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/memcpy.npk".*;')

# Fix array lookups returning Result
text = text.replace("pass SLAB_SIZES[i];", "pass raw SLAB_SIZES[i];")
text = text.replace("pass SLAB_SLOTS[i];", "pass raw SLAB_SLOTS[i];")

# Rename slab_free to libn_slab_free
text = text.replace("pub func:slab_free", "pub func:libn_slab_free")
text = text.replace("slab_free(ptr)", "libn_slab_free(ptr)")

# The `Result<int64>:r` and `.value` fixes (maybe they aren't needed if I just use `raw`? Wait, I saw "Cannot use Result<int64> as int64 in arithmetic". The error was from line 190, which I fixed by raw in slab_class_size.
# But what about the `r` and `.value` errors?
# "Line 205: Undefined identifier 'r'"
# Wait, look at line 204: Result<int64>:r = libn_mmap(...)
# Why would `r` be undefined?
# Because `libn_mmap` was undefined, so the declaration of `r` failed and was skipped by the parser!
# YES! In a custom compiler, if a statement fails to parse or typecheck, it's often skipped, so variables declared in it are "Undefined" later!
# So fixing `libn_mmap` (by importing syscall) will fix `r`!
# Fixing `mem_memcpy` will fix its cascading errors!

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)

