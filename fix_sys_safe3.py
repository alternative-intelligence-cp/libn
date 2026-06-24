with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

import re

def repl(m):
    return f"({m.group(1)}) {{ Result<int64>:r = sys!!(nr, a1, a2, a3, a4, a5, a6); if (r.is_error) {{ fail r.error; }} pass r.value; }},"

content = re.sub(r'\((SYS_[A-Z0-9_]+)\) \{ pass sys\!\!\(nr, a1, a2, a3, a4, a5, a6\); \},', repl, content)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)

