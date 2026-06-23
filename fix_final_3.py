with open('src/str/strfmt.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'uint8->:digits = ((upper) ? DIGITS_UPPER : DIGITS_LOWER) => uint8->;' in lines[i]:
        lines[i] = '    uint8->:digits = DIGITS_LOWER => uint8->;\n    if (upper) { digits = DIGITS_UPPER => uint8->; }\n'
    elif 'prefix[prefix_len + 1i64] = (is_upper) ? 88u8 : 120u8;' in lines[i]:
        lines[i] = '        if (is_upper) { prefix[prefix_len + 1i64] = 88u8; } else { prefix[prefix_len + 1i64] = 120u8; }\n'
with open('src/str/strfmt.npk', 'w') as f:
    f.writelines(lines)

with open('src/io/bio/fopen.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'f->buf_mode = ((fd == 1i64)) ? _IOLBF : _IOFBF;' in lines[i]:
        lines[i] = '        if (fd == 1i64) { f->buf_mode = _IOLBF; } else { f->buf_mode = _IOFBF; }\n'
    elif 'int64:buf = bio_alloc_buf(BUFSIZ) ? 0i64;' in lines[i]:
        lines[i] = '        int64:buf = _?bio_alloc_buf(BUFSIZ);\n'
    elif 'int64:fp = bio_alloc_file() ? 0i64;' in lines[i]:
        lines[i] = '    int64:fp = _?bio_alloc_file();\n'
    elif 'buf_mode = ((fd == 1i64)) ? _IOLBF : _IOFBF;' in lines[i]:
        lines[i] = '        if (fd == 1i64) { f->buf_mode = _IOLBF; } else { f->buf_mode = _IOFBF; }\n'
with open('src/io/bio/fopen.npk', 'w') as f:
    f.writelines(lines)
