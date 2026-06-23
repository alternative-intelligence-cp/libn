import os

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if 'fprintf_ptr_to_int_u8' in content:
        content = content.replace('fprintf_ptr_to_int_u8', 'libn_ptr_to_int_u8')
        with open(filepath, 'w') as f:
            f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
