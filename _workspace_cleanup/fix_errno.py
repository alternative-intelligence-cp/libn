import os
def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace errno_set with libn_errno_set
    # and ok_i64 with libn_ok_i64 if needed? Actually wait, ok_i64 is NOT libn_ok_i64.
    # What IS ok_i64? Let's check where ok_i64 is defined.
    # It might be in src/libn_result.npk?
    content = content.replace('errno_set(', 'libn_errno_set(')
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src/io/bio'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
