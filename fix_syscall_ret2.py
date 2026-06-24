with open("src/syscall/syscall.npk", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    line = line.replace("pub func:sys_fullfunc:sys_full", "pub func:sys_full")
    out.append(line)

with open("src/syscall/syscall.npk", "w") as f:
    f.writelines(out)
