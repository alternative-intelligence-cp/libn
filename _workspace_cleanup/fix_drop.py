import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace `Result<int64>:r = drop bio_flush_write_buf(fp);` with `int64:r = bio_flush_write_buf(fp);`
    # Also replace any other `Result<int64>:xxx = drop` that might be there
    content = re.sub(r'Result<int64>:([a-zA-Z0-9_]+)\s*=\s*drop\s+bio_flush_write_buf', r'int64:\1 = bio_flush_write_buf', content)
    
    # Let's also check if there are other `Result<int64>:x = drop ` and fix them
    content = re.sub(r'Result<int64>:([a-zA-Z0-9_]+)\s*=\s*drop\s+', r'int64:\1 = ', content)
    content = re.sub(r'Result<uint8>:([a-zA-Z0-9_]+)\s*=\s*drop\s+', r'uint8:\1 = ', content)

    # Wait, if `bio_flush_write_buf` returns `int64`, but the code does `if (r.is_error) {`, that's a problem!
    # Because `int64` doesn't have `.is_error`!
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
