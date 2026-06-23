import re

with open("/home/randy/Workspace/REPOS/libn/src/math/math.npk", "r") as f:
    text = f.read()

def repl(m):
    return m.group(1) + "raw math_" + m.group(2) + "("

text = re.sub(r'([^a-zA-Z0-9_:/])math_([a-zA-Z0-9_]+)\(', repl, text)

with open("/home/randy/Workspace/REPOS/libn/src/math/math.npk", "w") as f:
    f.write(text)

