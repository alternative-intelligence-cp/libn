import re

with open('src/str/strlen.npk', 'r') as f:
    text = f.read()

text = text.replace('pub func:str_strlen = int64(int64:s) {', 'pub func:str_strlen = int64(any->:s) {')
text = text.replace('pub func:str_strnlen = int64(int64:s, int64:max_len) {', 'pub func:str_strnlen = int64(any->:s, int64:max_len) {')

with open('src/str/strlen.npk', 'w') as f:
    f.write(text)

