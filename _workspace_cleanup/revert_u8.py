import os
import re

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            content = re.sub(r'@cast_unchecked<uint8>\(@cast_unchecked<uint8>\(([0-9a-fA-FxX]+)u8\)\)', r'\1u8', content)
            content = re.sub(r'@cast_unchecked<uint8>\(([0-9a-fA-FxX]+)u8\)', r'\1u8', content)

            with open(filepath, 'w') as f:
                f.write(content)
