import re

path_file = "/home/randy/Workspace/REPOS/libn/src/fs/path.npk"
with open(path_file, 'r') as f:
    content = f.read()

# Fix `is add_slash`
content = content.replace("(is add_slash : 1i64 : 0i64)", "(is (add_slash) ? 1i64 : 0i64)")
content = content.replace("(is add_slash :", "(is (add_slash) :")

# Replace `end` -> `end_pos` but only as a standalone word (variable)
content = re.sub(r'\bend\b', 'end_pos', content)

with open(path_file, 'w') as f:
    f.write(content)
print("path.npk fixed")
