import re
with open('src/str/strview.npk', 'r') as f:
    c = f.read()
# Find all StrView->:var and then replace var.len and var.ptr with var->len and var->ptr
# Actually, just replace all \b(sv|v|p|x|o|lo|ro|to|left|right|cur|tok|tmp)\.(len|ptr)\b with \1->\2
c = re.sub(r'\b(sv|s|v|p|x|o|lo|ro|to|left|right|cur|tok|tmp|sa|sb)\.(len|ptr)\b', r'\1->\2', c)
with open('src/str/strview.npk', 'w') as f:
    f.write(c)

