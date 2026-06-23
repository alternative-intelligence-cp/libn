import re
import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # In fchar.npk, read.npk, write.npk:
    content = content.replace('stack uint8[1]:one;', 'stack uint8[1]:one_buf;\n        uint8->:one = one_buf;')
    content = content.replace('stack uint8[1]:b;', 'stack uint8[1]:b_buf;\n        uint8->:b = b_buf;')
    
    # And fix read.npk corrupted blocks
    content = content.replace('if (fd->is_error) {', 'if (r.is_error) {')
    content = content.replace('if (fd->value == 0i64) {', 'if (r.value == 0i64) {')
    content = content.replace('if (b->is_error) {', 'if (r.is_error) {')
    content = content.replace('if (b->value == 0i64) {', 'if (r.value == 0i64) {')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))

