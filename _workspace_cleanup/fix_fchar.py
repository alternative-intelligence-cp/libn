import re
with open("src/io/bio/fchar.npk", "r") as f:
    content = f.read()

content = content.replace('stack byte:one[1];', 'stack uint8[1]:one;')
content = content.replace('pass one[0] as int64;', 'pass @cast_unchecked<int64>(one[0]);')
content = content.replace('byte:ch = (f.buf as *byte)[f.buf_pos];', 'uint8:ch = @cast_unchecked<uint8->>(f.buf)[f.buf_pos];')
content = content.replace('pass ch as int64;', 'pass @cast_unchecked<int64>(ch);')
content = content.replace('byte:b = c as byte;', 'uint8:b = @cast_unchecked<uint8>(c);')
content = content.replace('(f.buf as *byte)[f.buf_pos] = b;', '@cast_unchecked<uint8->>(f.buf)[f.buf_pos] = b;')

with open("src/io/bio/fchar.npk", "w") as f:
    f.write(content)
