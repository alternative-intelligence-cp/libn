with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

# Replace sys(SYS_XXX, ...) with sys(XXX, ...)
import re
text = re.sub(r'\bsys\(SYS_([A-Z0-9_]+)', r'sys(\1', text)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)
