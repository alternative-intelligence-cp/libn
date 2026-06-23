import os
def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('libn_libn_errno_set(', 'libn_errno_set(')
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src/io/bio'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
