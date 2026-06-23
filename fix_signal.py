import re

path = '/home/randy/Workspace/REPOS/libn/src/proc/signal.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """    int64:old_p = is (old_ptr != 0i64) : @old_val : 0i64;"""
new = """    int64:old_p = is (old_ptr != 0i64) : @cast_unchecked<int64>(@old_val) : 0i64;"""
content = content.replace(orig, new)

with open(path, 'w') as f:
    f.write(content)
print("Fixed signal")
