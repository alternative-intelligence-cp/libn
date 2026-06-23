import os
import re

def fix_array_addrs(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace @ident[0] with @ident inside @cast_unchecked
    # Actually, we can just replace any @ident[0] that is immediately preceded by ( and followed by )
    # e.g. (@ident[0]) -> (@ident)
    # Even more robustly, replace @ident[0] with @ident everywhere except if it is on the left of an assignment?
    # Wait, the compiler says "only variables supported currently". So @ident[0] is NEVER supported anywhere!
    # So we can just replace @ident[0] with @ident globally!
    
    new_content = re.sub(r'@([a-zA-Z_]\w*)\[0\]', r'@\1', content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Fixed @[0] in {file_path}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            fix_array_addrs(os.path.join(root, file))
