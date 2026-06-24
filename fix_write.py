import re

with open("src/io/write.npk", "r") as f:
    lines = f.readlines()

new_lines = []
in_loop = False
for line in lines:
    if "if (r.value == 0i64) {" in line:
        new_lines.append("        } else {\n")
        new_lines.append("            if (r.value == 0i64) {\n")
    elif "total = total + r.value;" in line:
        new_lines.append(line)
        new_lines.append("        }\n")
    elif "fail r.error;" in line:
        new_lines.append(line)
    else:
        new_lines.append(line)

with open("src/io/write.npk", "w") as f:
    f.writelines(new_lines)

