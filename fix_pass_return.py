import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    content = re.sub(r'pass\s+execve\(', 'return execve(', content)
    content = re.sub(r'pass\s+execvp\(', 'return execvp(', content)
    content = re.sub(r'pass\s+execvpe\(', 'return execvpe(', content)
    content = re.sub(r'pass\s+libn_dup\(', 'return libn_dup(', content)
    content = re.sub(r'pass\s+libn_fcntl\(', 'return libn_fcntl(', content)
    content = re.sub(r'pass\s+slab_alloc\(', 'return slab_alloc(', content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
