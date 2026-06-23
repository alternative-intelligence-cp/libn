import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    # 1. Fix struct
    text = re.sub(r'\b(pub\s+)?struct\s+([A-Za-z0-9_]+)\s*\{', r'\1struct:\2 = {', text)

    # 2. Fix &@cast_unchecked
    text = re.sub(r'&\s*@cast_unchecked<([A-Za-z0-9_\*]+)>\(([^\)]+)\)', r'@cast_unchecked<\1>(&\2)', text)

    # 3. test_all.npk might have missed something?
    # No, test_all.npk is outside src

    with open(file, 'w') as f:
        f.write(text)

