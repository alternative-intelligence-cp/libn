with open('src/str/strview.npk', 'r') as f:
    c = f.read()

c = c.replace(
'''        int64:plen = is (prefix != 0i64) : raw str_strlen(prefix) : 0i64;''',
'''        int64:plen = 0i64;
        if (prefix != 0i64) { plen = raw str_strlen(prefix); }''')

c = c.replace(
'''        int64:xlen = is (suffix != 0i64) : raw str_strlen(suffix) : 0i64;''',
'''        int64:xlen = 0i64;
        if (suffix != 0i64) { xlen = raw str_strlen(suffix); }''')

with open('src/str/strview.npk', 'w') as f:
    f.write(c)

