import re
with open("src/io/bio/fio.npk", "r") as f:
    content = f.read()

content = content.replace('int64:to_copy = buffered < remaining ? buffered : remaining;',
                          'int64:to_copy = 0i64;\n            if (buffered < remaining) { to_copy = buffered; } else { to_copy = remaining; }')
content = content.replace('if @cast_unchecked<uint8->>(src)[si] == 10u8 {  // \'\\n\'',
                          'if (@cast_unchecked<uint8->>(src)[si] == 10u8) {  // \'\\n\'')

with open("src/io/bio/fio.npk", "w") as f:
    f.write(content)
