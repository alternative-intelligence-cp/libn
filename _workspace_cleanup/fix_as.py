with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

content = content.replace("fail ERR_BADARG as tbb8;", "fail ERR_BADARG;")
content = content.replace("if ((r.error as int64) == EINTR) {", "if (@cast_unchecked<int64>(r.error) == EINTR) {")

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
