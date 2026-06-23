import os
import re

filepath = 'src/syscall/errno.npk'
with open(filepath, 'r') as f:
    code = f.read()

# Replace uint8-> or *uint8 or *byte with string
code = re.sub(r'pub func:err_str = (\*uint8|uint8->|uint8@|\*byte)\(int64:e\) \{', r'pub func:err_str = string(int64:e) {', code)

with open(filepath, 'w') as f:
    f.write(code)
