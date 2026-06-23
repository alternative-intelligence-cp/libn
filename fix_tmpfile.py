with open("src/io/bio/tmpfile.npk", "r") as f:
    content = f.read()

content = content.replace('pub fixed byte:TMP_DIR[]  = "/tmp/";', '')
content = content.replace('pub fixed byte:TMP_PREFIX[] = "npk_";', '')

content = content.replace('if (!(pid_r.is_error) { pid = pid_r.value; }', 'if (!(pid_r.is_error)) { pid = pid_r.value; }')

content = content.replace('fixed byte:hex[] = "0123456789abcdef";', 'uint8->:hex = @cast_unchecked<uint8->>("0123456789abcdef");')

content = content.replace('fixed byte:pfx[] = "/tmp/npk_XXXXXX";', 'int64:pfx = @cast_unchecked<int64>("/tmp/npk_XXXXXX");')
content = content.replace('int64:pfx_len = str_strlen(@cast_unchecked<int64>(pfx));', 'int64:pfx_len = str_strlen(pfx);')
content = content.replace('drop mem_memcpy(@cast_unchecked<int64>(tmpl), @cast_unchecked<int64>(pfx), pfx_len + 1i64);', 'drop mem_memcpy(@cast_unchecked<int64>(tmpl), pfx, pfx_len + 1i64);')

content = content.replace('int64:fp = fdopen(fd, "w+b" as int64);', 'int64:fp = fdopen(fd, @cast_unchecked<int64>("w+b"));')

content = content.replace('if (!(buf != 0i64) { dst = @cast_unchecked<int64>(g_tmpnam_buf); }', 'if (!(buf != 0i64)) { dst = @cast_unchecked<int64>(g_tmpnam_buf); }')

content = content.replace('fixed byte:pfx[] = "/tmp/npk_";', 'int64:pfx = @cast_unchecked<int64>("/tmp/npk_");')
content = content.replace('drop mem_memcpy(dst, @cast_unchecked<int64>(pfx), pfx_len);', 'drop mem_memcpy(dst, pfx, pfx_len);')

with open("src/io/bio/tmpfile.npk", "w") as f:
    f.write(content)
