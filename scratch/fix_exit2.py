import re

with open('src/proc/exit.npk', 'r') as f:
    content = f.read()

# Fix void to NIL
content = re.sub(r'\bvoid\b', r'NIL', content)

with open('src/proc/exit.npk', 'w') as f:
    f.write(content)
