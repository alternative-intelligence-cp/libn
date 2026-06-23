import re
import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Convert array to decayed pointer
    content = content.replace('stack int64[1]:one;\n        one[0] = 0i64;', 'stack int64[1]:one_arr;\n        int64->:one = one_arr;\n        one[0] = 0i64;')
    content = content.replace('stack int64[1]:b;\n        b[0] = 0i64;', 'stack int64[1]:b_arr;\n        int64->:b = b_arr;\n        b[0] = 0i64;')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))

