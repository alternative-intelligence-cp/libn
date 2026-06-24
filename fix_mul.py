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
    "    int128:res = @cast_unchecked<int128>(a) * @cast_unchecked<int128>(b);\n",
    "    if (res > @cast_unchecked<int128>(INT64_MAX)) { pass INT64_MAX; }\n",
    "    if (res < @cast_unchecked<int128>(INT64_MIN)) { pass INT64_MIN; }\n",
    "    pass @cast_unchecked<int64>(res);\n",
    "};\n"
]

lines[start:end+1] = new_body

with open('src/math/math.npk', 'w') as f:
    f.writelines(lines)
