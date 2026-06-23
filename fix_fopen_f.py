import re

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """    f->next_global = g_open_files;
    g_open_files = fp;"""
new = """    FILE->:f = @cast_unchecked<FILE->>(fp);
    f->next_global = g_open_files;
    g_open_files = fp;"""

content = content.replace(orig, new)

with open(path, 'w') as f:
    f.write(content)

print("Fixed fopen")
