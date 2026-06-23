import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        if line.strip() == '}':
            if i > 0 and lines[i-1].strip() == '':
                pass
            new_lines.append('};')
        else:
            new_lines.append(line)

    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))

fix_file("src/syscall/syscall.npk")
fix_file("src/mem/slab.npk")
