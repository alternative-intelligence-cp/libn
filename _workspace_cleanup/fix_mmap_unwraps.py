import os
import re

filepath = 'src/mem/mmap.npk'
with open(filepath, 'r') as f:
    code = f.read()

# Fix raw unwraps
code = code.replace('int64:total = page_align_up(ALLOC_HEADER_SIZE + n);', 'int64:total = raw page_align_up(ALLOC_HEADER_SIZE + n);')
code = code.replace('int64:new_total = page_align_up(ALLOC_HEADER_SIZE + n);', 'int64:new_total = raw page_align_up(ALLOC_HEADER_SIZE + n);')

with open(filepath, 'w') as f:
    f.write(code)

