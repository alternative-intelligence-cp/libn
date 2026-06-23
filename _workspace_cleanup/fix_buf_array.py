import os

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('libn_ptr_to_int_u8(&one[0])', '&one[0] as int64')
    content = content.replace('libn_ptr_to_int_u8(&buf[0])', '&buf[0] as int64')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
