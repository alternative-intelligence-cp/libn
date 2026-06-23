with open('/home/randy/Workspace/REPOS/libn/src/str/strconv.npk', 'r') as f:
    lines = f.readlines()
for l in [79, 139, 145, 150, 164, 232, 238, 242]:
    print(f"Line {l}: {lines[l-1].strip()}")
