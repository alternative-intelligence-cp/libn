import re
import os

for root, _, fs in os.walk('src'):
    for file in fs:
        if not file.endswith('.npk'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            c = f.read()
        
        # Avoid replacing definitions: `func:str_strlen = ...`
        # Also avoid already raw calls: `raw str_strlen(`
        # So we only replace when it's preceded by space, =, or (, and not preceded by raw
        c = re.sub(r'(?<!raw )(?<!func:)str_strlen\(', r'raw str_strlen(', c)
        
        with open(path, 'w') as f:
            f.write(c)

