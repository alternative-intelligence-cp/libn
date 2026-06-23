with open("src/io/bio/fio.npk", "r") as f:
    lines = f.readlines()
lines[92] = lines[92].replace(") {", ")) {")
lines[102] = lines[102].replace(") {", ")) {")
lines[234] = lines[234].replace(") {", ")) {")
with open("src/io/bio/fio.npk", "w") as f:
    f.writelines(lines)

with open("src/str/strbuf.npk", "r") as f:
    lines = f.readlines()
for i in [79, 111, 229, 243, 272, 297, 308, 319, 331, 343, 355, 368, 381, 394]:
    lines[i] = lines[i].replace(") {", ")) {")
with open("src/str/strbuf.npk", "w") as f:
    f.writelines(lines)

with open("src/math/math.npk", "r") as f:
    lines = f.readlines()
lines[103:108] = [
    "    if ((a ^ b) < 0i64) {\n",
    "        if (a < 0i64) { pass a; }\n",
    "        pass b;\n",
    "    }\n",
    "    if (a > b) { pass a; }\n",
    "    pass b;\n",
    "};\n",
]
with open("src/math/math.npk", "w") as f:
    f.writelines(lines)
