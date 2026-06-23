import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # In fchar.npk: @cast_unchecked<int64>(one) -> @cast_unchecked<int64>(&one[0])
    content = content.replace('@cast_unchecked<int64>(one)', '@cast_unchecked<int64>(&one[0])')
    
    # In fprintf.npk: @cast_unchecked<int64>(buf) -> @cast_unchecked<int64>(&buf[0])
    content = content.replace('@cast_unchecked<int64>(buf)', '@cast_unchecked<int64>(&buf[0])')
    
    # We also have 5 fprintf_ptr_to_int_u8(buf) left.
    content = content.replace('fprintf_ptr_to_int_u8(buf)', '@cast_unchecked<int64>(&buf[0])')
    
    # In memcpy.npk: @cast_unchecked<int64>(src) and dst etc. Actually wait, those are probably int64 already?
    # Let's just do these for now.

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
