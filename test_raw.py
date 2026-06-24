with open('src/str/strlen.npk', 'r') as f:
    lines = f.readlines()
lines[150] = "    int64:n = raw str_strnlen(s, max_len + 1i64);\n"
with open('src/str/strlen.npk', 'w') as f:
    f.writelines(lines)
