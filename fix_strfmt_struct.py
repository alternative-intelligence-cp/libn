import os
import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        content = fp.read()
        
    # struct declarations
    content = re.sub(r'\b(pub\s+)?struct\s+([A-Za-z0-9_]+)\s*\{', r'\1struct:\2 = {', content)
    
    # pointer types in params
    content = content.replace('*FmtState', 'FmtState->')
    content = content.replace('*FILE', 'FILE->')
    content = content.replace('*DIR', 'DIR->')
    
    # that weird ternary fix syntax error
    content = content.replace('if ((!((upper))) { digits = DIGITS_LOWER) as uint8->; }', 'if (!(upper)) { digits = @cast_unchecked<uint8->>(DIGITS_LOWER); }')
    
    with open(file, 'w') as fp:
        fp.write(content)

print("Fixed struct syntax.")
