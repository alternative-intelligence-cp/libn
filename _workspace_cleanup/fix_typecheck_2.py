import re

# Fix slab.npk
with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

text = text.replace('head = slab_freelist_get(cls);', 'head = raw slab_freelist_get(cls);')
text = text.replace('int64:ptr = raw slab_alloc(n);', 'int64:ptr = slab_alloc(n);')

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)


# Fix fopen.npk calls
with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

# Replace `int64:parse_res = bio_parse_mode(mode);` with `int64:parse_res = raw bio_parse_mode(mode);`
text = text.replace('int64:parse_res = bio_parse_mode(mode);', 'int64:parse_res = raw bio_parse_mode(mode);')

# Now fix the other calls to bio_parse_mode
def repl(m):
    return '''    int64:parse_res = raw bio_parse_mode(mode);
    if (parse_res < 0i64) {
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:open_flags = parse_res >> 32i64;
    int64:file_mode = parse_res & 0xFFFFFFFFi64;'''

text = re.sub(r'    int64\[1\]:file_mode_out;\n    int64\[1\]:open_flags_out;\n    int64:parse_ok = bio_parse_mode\(mode, @cast_unchecked<int64>\(file_mode_out\), @cast_unchecked<int64>\(open_flags_out\)\);\n    if \(parse_ok != 0i64\) \{\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \}\n\n    int64:file_mode  = file_mode_out\[0\];\n    int64:open_flags = open_flags_out\[0\];', repl, text)
text = re.sub(r'    int64\[1\]:file_mode_out;\n    int64\[1\]:open_flags_out;\n    int64:parse_ok = bio_parse_mode\(mode, file_mode_out, open_flags_out\);\n    if \(parse_ok != 0i64\) \{\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \}\n\n    int64:file_mode  = file_mode_out\[0\];\n    int64:open_flags = open_flags_out\[0\];', repl, text)

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

