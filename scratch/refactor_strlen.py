import re
with open('src/str/strlen.npk', 'r') as f:
    text = f.read()

text = text.replace("pub func:str_strlen = int64(int64:s) {", "pub func:str_strlen = int64(any->:s) {")
text = text.replace("pub func:str_strlen_safe = int64(int64:s, int64:max_len) {", "pub func:str_strlen_safe = int64(any->:s, int64:max_len) {")
text = text.replace("pub func:str_strnlen = int64(int64:s, int64:n) {", "pub func:str_strnlen = int64(any->:s, int64:n) {")

text = text.replace("uint8->:p = @cast_unchecked<uint8->>(s);", "")
text = text.replace("int64:i = 0i64;", "uint8->:p = @cast_unchecked<uint8->>(s);\n    int64:i = 0i64;")

text = text.replace("if (s == 0i64) {", "if (s == NULL) {")

with open('src/str/strlen.npk', 'w') as f:
    f.write(text)

