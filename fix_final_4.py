import re

# strconv.npk
with open('src/str/strconv.npk', 'r') as f:
    c = f.read()
c = re.sub(r'\blimit\b', 'max_val', c)
c = c.replace('else if base == 16i64 && p[i] == 48u8 &&\n              (p[i + 1i64] == 120u8 || p[i + 1i64] == 88u8) {',
              'else if (base == 16i64 && p[i] == 48u8 &&\n              (p[i + 1i64] == 120u8 || p[i + 1i64] == 88u8)) {')
with open('src/str/strconv.npk', 'w') as f:
    f.write(c)

# fio.npk
with open('src/io/bio/fio.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if '<-(@cast_unchecked<uint8->>(dst)) = f->@cast_unchecked<uint8>(unget);' in lines[i]:
        lines[i] = '            (@cast_unchecked<uint8->>(dst))[0] = @cast_unchecked<uint8>(f->unget);\n'
    elif 'int64:to_copy = (buffered < remaining) ? buffered : remaining;' in lines[i]:
        lines[i] = '            int64:to_copy = remaining; if (buffered < remaining) { to_copy = buffered; }\n'
    elif 'int64:to_copy = (buf_space < remaining) ? buf_space : remaining;' in lines[i]:
        lines[i] = '        int64:to_copy = remaining; if (buf_space < remaining) { to_copy = buf_space; }\n'
with open('src/io/bio/fio.npk', 'w') as f:
    f.writelines(lines)

# strchr.npk
with open('src/str/strchr.npk', 'r') as f:
    c = f.read()
c = c.replace('while n[j] != 0u8 && h[i + j] != 0u8 &&\n                  _!to_lower_ascii(h[i + j]) == _!to_lower_ascii(n[j]) {',
              'while (n[j] != 0u8 && h[i + j] != 0u8 &&\n                  _!to_lower_ascii(h[i + j]) == _!to_lower_ascii(n[j])) {')
with open('src/str/strchr.npk', 'w') as f:
    f.write(c)

