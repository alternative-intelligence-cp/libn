import os

def fix():
    # 1. strfmt.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strfmt.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("nlen = render_uint(", "nlen = raw render_uint(")
    with open(path, "w") as f: f.write(content)

    # 2. strcmp.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strcmp.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("strcmp_has_nul(va)", "(raw strcmp_has_nul(va) == true)")
    with open(path, "w") as f: f.write(content)

    # 3. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("while (raw is_whitespace(p[i]))", "while (raw is_whitespace(p[i]) == true)")
    # Are there any other while loops with truthiness?
    # Let's fix truthiness in general for is_whitespace
    with open(path, "w") as f: f.write(content)

fix()
