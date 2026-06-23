import os
import re

for root, _, files in os.walk('src'):
    for f in files:
        if not f.endswith('.npk'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r') as fp:
            content = fp.read()
            
        content = re.sub(r'\)\.(len|capacity|end_idx|pos|fd|flags|state|err|error|eof|buf|data|ptr)\b', r')->\1', content)
        
        with open(path, 'w') as fp:
            fp.write(content)

print("Parentheses dots replaced.")
