import re

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

# Add imports
text = text.replace('use "../syscall/errno.npk".*;', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/memcpy.npk".*;')

# Rename slab_free to libn_slab_free in declaration and calls
text = text.replace("pub func:slab_free", "pub func:libn_slab_free")
text = text.replace("slab_free(", "libn_slab_free(")

# But wait, we have slab_freelist_get, etc. The replacement above will replace "slab_free(" but not "slab_freelist".
# "slab_free(" => "libn_slab_free("

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)

