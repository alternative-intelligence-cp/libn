import re
with open('src/io/bio/fscanf.npk', 'r') as f:
    code = f.read()

code = code.replace(
    "if c != 32i64 && c != 9i64 && c != 10i64 &&\n           c != 13i64 && c != 12i64 && c != 11i64 {",
    "if (c != 32i64 && c != 9i64 && c != 10i64 &&\n           c != 13i64 && c != 12i64 && c != 11i64) {"
)
code = code.replace(
    "if c == 32i64 || c == 9i64 || c == 10i64 ||\n           c == 13i64 || c == 12i64 || c == 11i64 {",
    "if (c == 32i64 || c == 9i64 || c == 10i64 ||\n           c == 13i64 || c == 12i64 || c == 11i64) {"
)
code = code.replace(
    "if f[fi] == 108u8 || f[fi] == 104u8 || f[fi] == 122u8 ||\n           f[fi] == 106u8 || f[fi] == 116u8 {",
    "if (f[fi] == 108u8 || f[fi] == 104u8 || f[fi] == 122u8 ||\n           f[fi] == 106u8 || f[fi] == 116u8) {"
)

with open('src/io/bio/fscanf.npk', 'w') as f:
    f.write(code)
print("Fixed fscanf.npk")
