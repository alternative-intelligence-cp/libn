import re

with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

content = content.replace("(_) {", "(*) {")
content = content.replace("        }\n    }\n}\n", "        }\n    }\n};\n")

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)
