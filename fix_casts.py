import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Fix string literals cast
    # e.g., "PATH" as int64 -> @cast_unchecked<int64>("PATH")
    content = re.sub(r'("[^"]*")\s+as\s+([a-zA-Z0-9_]+(?:->)?)', r'@cast_unchecked<\2>(\1)', content)

    # Fix pointer cast
    # e.g., &@cast_unchecked<int64>(argv[0]) -> @cast_unchecked<int64>(&argv[0])
    content = re.sub(r'&@cast_unchecked<([^>]+)>\(([^)]+)\)', r'@cast_unchecked<\1>(&\2)', content)

    with open(path, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

