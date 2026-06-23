import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('int64:flush_res = bio_flush_write_buf', 'Result<int64>:flush_res = bio_flush_write_buf')
    content = content.replace('if (flush_res < 0i64)', 'if (flush_res.is_error)')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
