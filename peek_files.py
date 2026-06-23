def p(f, line):
    with open(f, 'r') as fp:
        lines = fp.readlines()
    if line-1 < len(lines):
        print(f"{f}:{line}: {lines[line-1].strip()}")

p('src/str/strview.npk', 57)
p('src/str/strview.npk', 399)
p('src/str/strview.npk', 400)
p('src/str/strview.npk', 433)
p('src/str/strview.npk', 451)

p('src/proc/signal.npk', 214)
p('src/proc/signal.npk', 224)
p('src/proc/signal.npk', 242)
