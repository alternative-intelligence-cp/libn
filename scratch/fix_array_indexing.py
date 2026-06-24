import re

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

replacement1 = """func:slab_class_size = int64(int64:i) {
    if (i == 0i64) { pass 8i64; }
    if (i == 1i64) { pass 16i64; }
    if (i == 2i64) { pass 32i64; }
    if (i == 3i64) { pass 64i64; }
    if (i == 4i64) { pass 128i64; }
    if (i == 5i64) { pass 256i64; }
    if (i == 6i64) { pass 512i64; }
    if (i == 7i64) { pass 1024i64; }
    if (i == 8i64) { pass 2048i64; }
    if (i == 9i64) { pass 4096i64; }
    pass 0i64;
};"""

replacement2 = """func:slab_class_slots = int64(int64:i) {
    if (i == 0i64) { pass 256i64; }
    if (i == 1i64) { pass 170i64; }
    if (i == 2i64) { pass 102i64; }
    if (i == 3i64) { pass 56i64; }
    if (i == 4i64) { pass 30i64; }
    if (i == 5i64) { pass 15i64; }
    if (i == 6i64) { pass 7i64; }
    if (i == 7i64) { pass 3i64; }
    if (i == 8i64) { pass 1i64; }
    if (i == 9i64) { pass 0i64; }
    pass 0i64;
};"""

# Replace slab_class_size body
text = re.sub(r'func:slab_class_size = int64\(int64:i\) \{.*?pass SLAB_SIZES\[i\];\n\};', replacement1, text, flags=re.DOTALL)

# Replace slab_class_slots body
text = re.sub(r'func:slab_class_slots = int64\(int64:i\) \{.*?pass SLAB_SLOTS\[i\];\n\};', replacement2, text, flags=re.DOTALL)

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)

