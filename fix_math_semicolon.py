with open("/home/randy/Workspace/REPOS/libn/src/math/math.npk", "r") as f:
    text = f.read()

# Replace any `^}$` or `^} $` that is at the end of a function with `};`
import re
text = re.sub(r'^}(\s*)$', r'};\1', text, flags=re.MULTILINE)

with open("/home/randy/Workspace/REPOS/libn/src/math/math.npk", "w") as f:
    f.write(text)

