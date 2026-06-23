import os

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # in fchar.npk
    content = content.replace('int64:one_ptr = &one[0] as int64;', 'int64:one_ptr = raw libn_ptr_to_int_u8(one);')
    # in printf.npk
    content = content.replace('&buf[0] as int64', 'raw libn_ptr_to_int_u8(buf)')
    # in fprintf.npk and everywhere else where buf_ptr is used
    content = content.replace('int64:buf_ptr = libn_ptr_to_int_u8(buf);', 'int64:buf_ptr = raw libn_ptr_to_int_u8(buf);')
    content = content.replace('libn_ptr_to_int_u8(one)', 'raw libn_ptr_to_int_u8(one)')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
