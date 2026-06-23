import re

path = '/home/randy/Workspace/REPOS/libn/src/proc/signal.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """    int64:tid = is (pid_r.is_error) : 1i64 : pid_r.value;"""
new = """    int64:tid = pid_r ?! 1i64;"""
content = content.replace(orig, new)

with open(path, 'w') as f:
    f.write(content)
print("Fixed signal tid")
