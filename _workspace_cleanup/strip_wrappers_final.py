with open("src/syscall/syscall.npk", "r") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if line.startswith("pub func:sys") and ("sys = " in line or "sys!! = " in line or "sys!!! = " in line or "sys1 = " in line or "sys2 = " in line or "sys3 = " in line or "sys4 = " in line or "sys5 = " in line or "sys6 = " in line):
        skip = True
    
    if not skip:
        out.append(line)
        
    if skip and line.strip() == "};":
        skip = False

with open("src/syscall/syscall.npk", "w") as f:
    f.writelines(out)
