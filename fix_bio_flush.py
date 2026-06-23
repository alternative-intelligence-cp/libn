import re
import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace('int64:r = bio_flush_write_buf(fp);', 'int64:r = raw bio_flush_write_buf(fp);')
    content = content.replace('int64:r = bio_refill_read_buf(fp);', 'int64:r = raw bio_refill_read_buf(fp);')
    content = content.replace('pass bio_flush_write_buf(fp);', 'pass raw bio_flush_write_buf(fp);')
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))

