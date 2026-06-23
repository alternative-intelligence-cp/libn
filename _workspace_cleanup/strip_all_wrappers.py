with open("src/syscall/syscall.npk", "r") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if line.startswith("pub func:sys_"):
        skip = True
    
    if not skip:
        out.append(line)
        
    if skip and line.strip() == "};":
        skip = False

with open("src/syscall/syscall.npk", "w") as f:
    f.writelines(out)
