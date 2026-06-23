with open('src/io/bio/tmpfile.npk', 'r') as f:
    text = f.read()

text = text.replace('pub fixed byte:TMP_DIR[]  = "/tmp/";', 'pub fixed string:TMP_DIR  = "/tmp/";')
text = text.replace('pub fixed byte:TMP_PREFIX[] = "npk_";', 'pub fixed string:TMP_PREFIX = "npk_";')

text = text.replace('int64:pid = pid_r.is_error ? 1i64 : pid_r.value;',
"""int64:pid = pid_r.value;
    if (pid_r.is_error) { pid = 1i64; }""")

text = text.replace('stack int64:ts[2];  // timespec: tv_sec (int64), tv_nsec (int64)', 'int64[2]:ts;  // timespec: tv_sec (int64), tv_nsec (int64)')
text = text.replace('@cast_unchecked<int64>(&ts[0])', '@cast_unchecked<int64>(ts)')

text = text.replace('stack byte:tmpl[32];', 'uint8[32]:tmpl;')
text = text.replace('uint8->:tp = &tmpl[0] as *byte;', 'uint8->:tp = @cast_unchecked<uint8->>(tmpl);')

text = text.replace('fixed byte:pfx[] = "/tmp/npk_XXXXXX";', 'int64:pfx = @cast_unchecked<int64>(@"/tmp/npk_XXXXXX");')
text = text.replace('@cast_unchecked<int64>(&pfx[0])', 'pfx')

text = text.replace('@cast_unchecked<int64>(&tmpl[0])', '@cast_unchecked<int64>(tmpl)')

text = text.replace('"w+b" as int64', '@cast_unchecked<int64>(@"w+b")')

text = text.replace('byte:g_tmpnam_buf[256];', 'uint8[256]:g_tmpnam_buf;')

text = text.replace('int64:dst = buf != 0i64 ? buf : @cast_unchecked<int64>(&g_tmpnam_buf[0]);',
"""int64:dst = buf;
    if (buf == 0i64) { dst = @cast_unchecked<int64>(g_tmpnam_buf); }""")

text = text.replace('fixed byte:pfx[] = "/tmp/npk_";', 'int64:pfx = @cast_unchecked<int64>(@"/tmp/npk_");')

with open('src/io/bio/tmpfile.npk', 'w') as f:
    f.write(text)
