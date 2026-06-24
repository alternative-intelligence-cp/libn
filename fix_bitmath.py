with open('src/math/math.npk', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith('pub func:math_popcount ='):
        new_lines.append("pub func:math_popcount = int64(int64:v) {\n")
        new_lines.append("    pass asm!!!<int64>(\"x86_64\", \"popcnt %1, %0\", \"=r,r\", v);\n")
        new_lines.append("};\n")
        skip = True
    elif line.startswith('pub func:math_clz ='):
        new_lines.append("pub func:math_clz = int64(int64:v) {\n")
        new_lines.append("    pass asm!!!<int64>(\"x86_64\", \"lzcnt %1, %0\", \"=r,r\", v);\n")
        new_lines.append("};\n")
        skip = True
    elif line.startswith('pub func:math_ctz ='):
        new_lines.append("pub func:math_ctz = int64(int64:v) {\n")
        new_lines.append("    pass asm!!!<int64>(\"x86_64\", \"tzcnt %1, %0\", \"=r,r\", v);\n")
        new_lines.append("};\n")
        skip = True
    elif skip and line.startswith('};'):
        skip = False
    elif not skip:
        new_lines.append(line)

with open('src/math/math.npk', 'w') as f:
    f.writelines(new_lines)
