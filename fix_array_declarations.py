import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    # Match: optional 'stack ', then type, colon, name, brackets, semicolon.
    # Group 1: 'stack ' or 'pub ' or None
    # Group 2: type (e.g. byte, int64, Result)
    # Group 3: name
    # Group 4: size
    text = re.sub(r'\b(stack\s+|pub\s+)?([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_]+)\s*\[([^\]]+)\]\s*;', r'\1\2[\4]:\3;', text)

    with open(file, 'w') as f:
        f.write(text)

