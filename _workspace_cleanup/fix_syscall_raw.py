import os
import re

file_path = '/home/randy/Workspace/REPOS/libn/src/syscall/syscall.npk'
with open(file_path, 'r') as f:
    content = f.read()

# Revert pass raw ret; to pass ret;
content = re.sub(r'pass raw ret;', r'pass ret;', content)

# Revert int64:ret = raw(sys!!(...)); to int64:ret = sys!!(...);
content = re.sub(r'int64:ret = raw\(sys!!\((.*?)\)\);', r'int64:ret = sys!!(\1);', content)
content = re.sub(r'int64:ret = raw\(sys!!!\((.*?)\)\);', r'int64:ret = sys!!!(\1);', content)

with open(file_path, 'w') as f:
    f.write(content)
print("Fixed syscall.npk")
