import re

# math.npk
with open('src/math/math.npk', 'r') as f:
    c = f.read()
c = re.sub(r'if \(v & (0x[0-9A-Fa-fi]+64)\) == 0i64 \{', r'if ((v & \1) == 0i64) {', c)
c = c.replace('while (x + 1i64) <= v / (x + 1i64) {', 'while ((x + 1i64) <= v / (x + 1i64)) {')
with open('src/math/math.npk', 'w') as f:
    f.write(c)

# memutil.npk
with open('src/mem/memutil.npk', 'r') as f:
    c = f.read()
c = c.replace('int64->) ? pw = (ptr + i) => int64->;', 'int64->:pw = (ptr + i) => int64->;')
c = c.replace('uint8->) ? pb = (ptr + i) => uint8->;', 'uint8->:pb = (ptr + i) => uint8->;')
with open('src/mem/memutil.npk', 'w') as f:
    f.write(c)

# file.npk
with open('src/io/bio/file.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'oflags[0] = (has_plus) ? O_RDWR : O_RDONLY;' in lines[i]:
        lines[i] = '        if (has_plus) { oflags[0] = O_RDWR; } else { oflags[0] = O_RDONLY; }\n'
    elif 'oflags[0] = (has_plus) ? O_RDWR | O_APPEND : O_WRONLY | O_APPEND;' in lines[i]:
        lines[i] = '        if (has_plus) { oflags[0] = O_RDWR | O_APPEND; } else { oflags[0] = O_WRONLY | O_APPEND; }\n'
    elif 'oflags[0] = (has_plus) ? O_RDWR | O_CREAT | O_TRUNC : O_WRONLY | O_CREAT | O_TRUNC;' in lines[i]:
        lines[i] = '        if (has_plus) { oflags[0] = O_RDWR | O_CREAT | O_TRUNC; } else { oflags[0] = O_WRONLY | O_CREAT | O_TRUNC; }\n'
with open('src/io/bio/file.npk', 'w') as f:
    f.writelines(lines)

# strcpy.npk
with open('src/str/strcpy.npk', 'r') as f:
    c = f.read()
c = c.replace('(r.@cast_unchecked<uint8->>(val))[actual_len] = 0u8;', '(@cast_unchecked<uint8->>(r.val))[actual_len] = 0u8;')
with open('src/str/strcpy.npk', 'w') as f:
    f.write(c)
