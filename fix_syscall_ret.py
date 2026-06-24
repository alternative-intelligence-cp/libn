import re

with open("src/syscall/syscall.npk", "r") as f:
    text = f.read()

text = re.sub(r'pub func:(sys_safe\d*) = int64', r'pub func:\1 = Result<int64>', text)
text = re.sub(r'pub func:(sys_full\d*) = int64', r'pub func:\1 = Result<int64>', text)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(text)
