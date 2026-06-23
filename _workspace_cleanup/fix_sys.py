import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace SYS_M... with M...
    content = re.sub(r'\bSYS_MMAP\b', 'MMAP', content)
    content = re.sub(r'\bSYS_MUNMAP\b', 'MUNMAP', content)
    content = re.sub(r'\bSYS_MPROTECT\b', 'MPROTECT', content)
    content = re.sub(r'\bSYS_MREMAP\b', 'MREMAP', content)
    content = re.sub(r'\bSYS_MADVISE\b', 'MADVISE', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
