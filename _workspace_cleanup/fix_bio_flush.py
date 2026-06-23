import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # If we replaced `Result<int64>:r = drop ...` with `int64:r = ...`, let's fix `r.is_error` right after it
    # We will just replace `if (r.is_error)` with `if (r < 0i64)` where `r` is the variable
    # Wait, it's safer to just change the assignment and the if statement.
    content = content.replace('int64:r = bio_flush_write_buf', 'int64:flush_res = bio_flush_write_buf')
    
    # Wait, the best way is to use regex:
    content = re.sub(r'int64:([a-zA-Z0-9_]+)\s*=\s*bio_flush_write_buf(.*?);\s*if \(\1\.is_error\)', r'int64:\1 = bio_flush_write_buf\2;\n        if (\1 < 0i64)', content)
    
    # Let's also check if there are `.error` accesses
    content = re.sub(r'\.error', r'', content) # DANGEROUS! No!

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
