with open("/home/randy/Workspace/REPOS/libn/src/math/math.npk", "r") as f:
    text = f.read()

# Remove 'raw math_'
text = text.replace("raw math_", "math_")

with open("/home/randy/Workspace/REPOS/libn/src/math/math.npk", "w") as f:
    f.write(text)

