import re

# Fix slab.npk
with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

text = text.replace('int64:head = slab_freelist_get(cls);', 'int64:head = raw slab_freelist_get(cls);')
text = text.replace('int64:old_head = slab_freelist_get(cls);', 'int64:old_head = raw slab_freelist_get(cls);')
text = text.replace('int64:sz   = slab_class_size(cls);', 'int64:sz = raw slab_class_size(cls);')

text = text.replace('Result<int64>:r = slab_alloc(n);\n    if (r.is_error) {\n        fail r.error;\n    }\n    int64:ptr = r.value;', 'int64:ptr = raw slab_alloc(n);')

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)

# Fix file.npk
with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

text = text.replace('byte:first = m[0];', 'uint8:first = m[0];')
text = text.replace('pub func:bio_parse_mode = int64(int64:mode_str, int64->:fmode, int64->:oflags) {', 'pub func:bio_parse_mode = int64(int64:mode_str) {')

# The original bio_parse_mode used fmode[0] = ... and oflags[0] = ...
# We'll replace all fmode[0] and oflags[0] with local variables and pass them out
text = text.replace('    fmode[0]  = 0i64;\n    oflags[0] = 0i64;\n', '    int64:fmode_val = 0i64;\n    int64:oflags_val = 0i64;\n')
text = text.replace('fmode[0]', 'fmode_val')
text = text.replace('oflags[0]', 'oflags_val')
text = text.replace('pass 0i64;', 'pass (oflags_val << 32i64) | fmode_val;')

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

# Fix fopen.npk
with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

text = text.replace('libn_errno_set(EINVAL);', 'drop libn_errno_set(EINVAL);')
text = text.replace('libn_errno_set(@cast_unchecked<int64>(r.error));', 'drop libn_errno_set(@cast_unchecked<int64>(r.error));')
text = text.replace('libn_errno_set(ENOMEM);', 'drop libn_errno_set(ENOMEM);')

text = text.replace('''    int64[1]:file_mode_out;
    int64[1]:open_flags_out;
    int64:parse_ok = bio_parse_mode(mode, @cast_unchecked<int64>(file_mode_out), @cast_unchecked<int64>(open_flags_out));
    if (parse_ok != 0i64) {
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }

    int64:file_mode  = file_mode_out[0];
    int64:open_flags = open_flags_out[0];''', '''    int64:parse_res = bio_parse_mode(mode);
    if (parse_res < 0i64) {
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:open_flags = parse_res >> 32i64;
    int64:file_mode = parse_res & 0xFFFFFFFFi64;''')

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

