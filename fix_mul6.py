with open('src/math/math.npk', 'r') as f:
    lines = f.readlines()

start = -1
end = -1
for i, line in enumerate(lines):
    if line.startswith('pub func:math_sat_mul_i64 ='):
        start = i
    elif start != -1 and line.startswith('};'):
        end = i
        break

new_body = [
    "pub func:math_sat_mul_i64 = int64(int64:a, int64:b) {\n",
    "    if (a == 0i64 || b == 0i64) { pass 0i64; }\n",
    "    if (a == 1i64) { pass b; }\n",
    "    if (b == 1i64) { pass a; }\n",
    "    pass asm!!!<int64>(\"x86_64\", \"mov %1, %0\\nimul %2, %0\\njno 1f\\nmov %1, %0\\nxor %2, %0\\nsar $$63, %0\\nnot %0\\nbtc $$63, %0\\n1:\", \"=r,r,r\", a, b);\n",
    "};\n"
]

lines[start:end+1] = new_body

with open('src/math/math.npk', 'w') as f:
    f.writelines(lines)
