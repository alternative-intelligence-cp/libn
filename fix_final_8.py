with open('src/str/strview.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'struct StrViewIter {' in lines[i]:
        lines[i] = 'struct:StrViewIter = {\n'
    elif 'sv.@cast_unchecked<uint8->>(ptr);' in lines[i]:
        lines[i] = '    uint8->:p = @cast_unchecked<uint8->>(sv.ptr);\n'
    elif 'if c == ' in lines[i]:
        lines[i] = lines[i].replace('if c ==', 'if (c ==').replace('{', ') {')
    elif '?' in lines[i] and ':' in lines[i] and '//' not in lines[i]:
        print(f"strview.npk:{i+1}: {lines[i].strip()}")

with open('src/str/strview.npk', 'w') as f:
    f.writelines(lines)
