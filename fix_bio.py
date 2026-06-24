import re
import os

for root, _, fs in os.walk('src'):
    for file in fs:
        if not file.endswith('.npk'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            c = f.read()
        
        c = c.replace('bio_parse_mode(', 'raw bio_parse_mode(')
        c = c.replace('bio_alloc_file(', 'raw bio_alloc_file(')
        c = c.replace('bio_alloc_buf(', 'raw bio_alloc_buf(')
        
        with open(path, 'w') as f:
            f.write(c)

