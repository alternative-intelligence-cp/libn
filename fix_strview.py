with open('src/str/strview.npk', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    # fix end_idx -> we'll change end/end_idx to limit_val
    if 'end_idx' in lines[i]:
        lines[i] = lines[i].replace('end_idx', 'limit_val')
    if 'int64:end,' in lines[i]:
        lines[i] = lines[i].replace('int64:end,', 'int64:limit_val,')
    if '(end <' in lines[i]:
        lines[i] = lines[i].replace('(end <', '(limit_val <')
    if '> end)' in lines[i]:
        lines[i] = lines[i].replace('> end)', '> limit_val)')
    if ' end;' in lines[i]:
        lines[i] = lines[i].replace(' end;', ' limit_val;')
    if ' end)' in lines[i]:
        lines[i] = lines[i].replace(' end)', ' limit_val)')
    if '= end;' in lines[i]:
        lines[i] = lines[i].replace('= end;', '= limit_val;')
    if ' end -' in lines[i]:
        lines[i] = lines[i].replace(' end -', ' limit_val -')

    # ternaries
    if 'sv->len = (len < 0i64) ? 0i64 : len;' in lines[i]:
        lines[i] = '    sv->len = len; if (len < 0i64) { sv->len = 0i64; }\n'
    if 'int64:min_len = (sa->len < sb->len) ? sa->len : sb->len;' in lines[i]:
        lines[i] = '    int64:min_len = sb->len; if (sa->len < sb->len) { min_len = sa->len; }\n'
    if 'int64:plen = (prefix != 0i64) ? _!str_strlen(prefix) : 0i64;' in lines[i]:
        lines[i] = '        int64:plen = 0i64; if (prefix != 0i64) { plen = _!str_strlen(prefix); }\n'
    if 'int64:xlen = (suffix != 0i64) ? _!str_strlen(suffix) : 0i64;' in lines[i]:
        lines[i] = '        int64:xlen = 0i64; if (suffix != 0i64) { xlen = _!str_strlen(suffix); }\n'
    if 'int64:n = (s->len < buflen) ? s->len : buflen;' in lines[i]:
        lines[i] = '    int64:n = buflen; if (s->len < buflen) { n = s->len; }\n'
    if 'int64:n = (s->len < max) ? s->len : max;' in lines[i]:
        lines[i] = '    int64:n = max; if (s->len < max) { n = s->len; }\n'

    # cast uncheck
    if '(r.@cast_unchecked<uint8->>(val))[s->len] = 0u8;' in lines[i]:
        lines[i] = '    (@cast_unchecked<uint8->>(r.val))[s->len] = 0u8;\n'

with open('src/str/strview.npk', 'w') as f:
    f.writelines(lines)
