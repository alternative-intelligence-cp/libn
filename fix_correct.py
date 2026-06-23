import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    # 1. Functions end with };
    text = re.sub(r'^\}$', r'};', text, flags=re.MULTILINE)

    # 2. `as type` to `@cast_unchecked<type>`
    lines = text.split('\n')
    for i in range(len(lines)):
        if lines[i].strip().startswith('//'): continue
        lines[i] = re.sub(r'\b([a-zA-Z0-9_\.]+(?:\[[^\]]+\])?)\s+as\s+([a-zA-Z0-9_\*]+)\b', r'@cast_unchecked<\2>(\1)', lines[i])
        lines[i] = re.sub(r'\(([^\)]+)\)\s+as\s+([a-zA-Z0-9_\*]+)\b', r'@cast_unchecked<\2>(\1)', lines[i])
    text = '\n'.join(lines)

    # 3. test_all.npk pass to exit
    if 'test_all.npk' in file:
        pass # Handle below

    with open(file, 'w') as f:
        f.write(text)

with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('pass 0i32;', 'exit 0i32;')
text = text.replace('pass 0i64;', 'exit 0i32;')
with open('test_all.npk', 'w') as f:
    f.write(text)

