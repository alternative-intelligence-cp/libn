import re

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """is (oflags[0] = has_plus) : O_RDWR : O_RDONLY;"""
new = """if (has_plus) {
            oflags[0] = O_RDWR;
        } else {
            oflags[0] = O_RDONLY;
        }"""
content = content.replace(orig, new)

with open(path, 'w') as f:
    f.write(content)
print("Fixed ternary")
