import os
import re

for root, _, files in os.walk('src'):
    for f in files:
        if not f.endswith('.npk'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r') as fp:
            content = fp.read()
            
        # Global replace of known pointer variables dot access
        content = re.sub(r'\b(sv|sb|iter|fp|f|file)\.(len|capacity|end_idx|pos|fd|flags|state|err|error|eof|buf|data|ptr)\b', r'\1->\2', content)
        
        # also 'errno_set' to 'libn_errno_set'
        content = re.sub(r'\berrno_set\(', r'libn_errno_set(', content)
        
        # also Result.err to Result.error
        content = re.sub(r'\.err\b', r'.error', content)
        
        # also fix 'raw raw' if any accidentally got created
        content = re.sub(r'\braw\s+raw\b', r'raw', content)
        
        with open(path, 'w') as fp:
            fp.write(content)

print("Global replace done.")
