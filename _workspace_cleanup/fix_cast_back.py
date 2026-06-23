import os

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('@cast_unchecked<int64>(&one[0])', 'libn_ptr_to_int_u8(one)')
    content = content.replace('@cast_unchecked<int64>(&buf[0])', 'libn_ptr_to_int_u8(buf)')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
