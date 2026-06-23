import re

with open('src/str/strview.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'pub struct StrView {' in lines[i]:
        lines[i] = 'pub struct:StrView = {\n'
    if 'end' in lines[i] and i in [394, 395, 396, 397, 398, 399, 400, 401, 402]:
        lines[i] = re.sub(r'\bend\b', 'limit_val', lines[i])
    if 'if c != 32u8 &&' in lines[i]:
        lines[i] = lines[i].replace('if c != 32u8 &&', 'if (c != 32u8 &&')
    if 'c != 13u8 && c != 12u8 && c != 11u8 {' in lines[i]:
        lines[i] = lines[i].replace('11u8 {', '11u8) {')
with open('src/str/strview.npk', 'w') as f:
    f.writelines(lines)

with open('src/proc/signal.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if '&set_val,' in lines[i]:
        lines[i] = lines[i].replace('&set_val,', '@set_val => int64,')
    if '&old_val' in lines[i]:
        lines[i] = lines[i].replace('&old_val', '@old_val => int64')
    if '*(@cast_unchecked<*int64>(old_ptr)) = old_val;' in lines[i]:
        lines[i] = '        (@cast_unchecked<int64->>(old_ptr))[0] = old_val;\n'

with open('src/proc/signal.npk', 'w') as f:
    f.writelines(lines)

