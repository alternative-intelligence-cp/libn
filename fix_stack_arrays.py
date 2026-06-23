import re
import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Undo the previous broken fix
    content = content.replace('stack uint8[1]:one_buf;\n        uint8->:one = one_buf;', 'stack int64[1]:one;\n        one[0] = 0i64;')
    content = content.replace('stack uint8[1]:b_buf;\n        uint8->:b = b_buf;', 'stack int64[1]:b;\n        b[0] = 0i64;')
    content = content.replace('stack uint8[1]:one;', 'stack int64[1]:one;\n        one[0] = 0i64;')
    content = content.replace('stack uint8[1]:b;', 'stack int64[1]:b;\n        b[0] = 0i64;')

    # When reading out of 'one', we did 'uint8:c = raw one[0];' or similar. 
    # Or in fchar.npk: 'pass @cast_unchecked<int64>(one[0]);'
    # Actually, one[0] is an int64. We can cast it to int64 directly (it is already int64!).
    content = content.replace('@cast_unchecked<int64>(one[0])', 'one[0]')
    content = content.replace('raw one[0]', '@cast_unchecked<uint8>(one[0] & 0xFFi64)')
    content = content.replace('b[0] = b;', 'b[0] = @cast_unchecked<int64>(b);')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))

