import re
with open("src/io/bio/fopen.npk", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == "}":
        if line.startswith("}"):
            lines[i] = "};\n"

with open("src/io/bio/fopen.npk", "w") as f:
    f.writelines(lines)
