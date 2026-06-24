import re
import os

for root, _, fs in os.walk('src'):
    for file in fs:
        if not file.endswith('.npk'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            c = f.read()

        c = re.sub(r'(?<!raw )(?<!func:)str_strnlen\(', r'raw str_strnlen(', c)
        c = re.sub(r'(?<!raw )(?<!func:)to_lower_ascii\(', r'raw to_lower_ascii(', c)
        
        with open(path, 'w') as f:
            f.write(c)
