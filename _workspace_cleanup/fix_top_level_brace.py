import os

def fix_file(filepath):
    with open(filepath, "r") as f:
        lines = f.read().split('\n')
    
    for i in range(len(lines)):
        if lines[i] == '}':
            lines[i] = '};'
            
    with open(filepath, "w") as f:
        f.write('\n'.join(lines))

fix_file("src/syscall/syscall.npk")
fix_file("src/mem/slab.npk")
