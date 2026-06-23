import os
import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        content = fp.read()
        
    # Replace &@cast_unchecked<TYPE>(var[0]) with @cast_unchecked<TYPE>(var)
    content = re.sub(r'&@cast_unchecked<([a-zA-Z0-9_\*\[\]\->]+)>\(([a-zA-Z0-9_]+)\[0\]\)', r'@cast_unchecked<\1>(\2)', content)
    # Any remaining &@cast_unchecked<TYPE>(var) -> @cast_unchecked<TYPE>(var)
    content = re.sub(r'&@cast_unchecked', r'@cast_unchecked', content)
    
    # Also fix arrays: `type:var[size]` -> `type[size]:var`
    # if it didn't work from `fix_array_declarations.py` because `stack byte:b[1];`
    content = re.sub(r'\b(stack\s+|pub\s+)?([a-zA-Z0-9_\->]+)\s*:\s*([a-zA-Z0-9_]+)\s*\[([^\]]+)\]\s*;', r'\1\2[\4]:\3;', content)
    
    with open(file, 'w') as fp:
        fp.write(content)

print("Fixed array & and declarations.")
