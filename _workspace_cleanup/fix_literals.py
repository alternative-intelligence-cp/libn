import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()

    # Change byte[]:var or uint8[]:var = "string" to string:var = "string"
    code = re.sub(r'(?:uint8|byte)\[\]:([a-zA-Z0-9_]+)\s*=\s*("[^"]+");', r'string:\1 = \2;', code)

    with open(filepath, 'w') as f:
        f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_file(os.path.join(root, f))
