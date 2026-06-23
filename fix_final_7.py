with open('src/fs/path.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'int64:total = a_end + (((add_slash)) ? 1i64 : 0i64) + blen;' in lines[i]:
        lines[i] = '    int64:total = a_end + blen; if (add_slash) { total = total + 1i64; }\n'
with open('src/fs/path.npk', 'w') as f:
    f.writelines(lines)

with open('src/io/bio/fstate.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'int64:cap = (size > 0i64) ? size : BUFSIZ;' in lines[i]:
        lines[i] = '    int64:cap = BUFSIZ; if (size > 0i64) { cap = size; }\n'
    elif 'int64:newbuf = bio_alloc_buf(cap) ? 0i64;' in lines[i]:
        lines[i] = '    int64:newbuf = _?bio_alloc_buf(cap);\n'
with open('src/io/bio/fstate.npk', 'w') as f:
    f.writelines(lines)

with open('src/str/strbuf.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'int64:new_cap = (s->cap > 0i64) ? s->cap : STRBUF_MIN_CAP;' in lines[i]:
        lines[i] = '        int64:new_cap = STRBUF_MIN_CAP; if (s->cap > 0i64) { new_cap = s->cap; }\n'
    elif 'int64:cap = (init_cap > STRBUF_MIN_CAP) ? init_cap : STRBUF_MIN_CAP;' in lines[i]:
        lines[i] = '    int64:cap = STRBUF_MIN_CAP; if (init_cap > STRBUF_MIN_CAP) { cap = init_cap; }\n'
with open('src/str/strbuf.npk', 'w') as f:
    f.writelines(lines)
