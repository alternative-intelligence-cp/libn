import os

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The files contain: `Result<int64>:r = drop bio_flush_write_buf(fp);`
    # We want to remove `drop `
    content = content.replace('= drop bio_flush_write_buf', '= bio_flush_write_buf')
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src/io/bio'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
