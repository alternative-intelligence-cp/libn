import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    orig = text

    text = re.sub(r'^(\s*)\}$', r'\1};', text, flags=re.MULTILINE)
    text = re.sub(r'^\}$', r'};', text, flags=re.MULTILINE)

    # Use \b to prevent matching inside 'pass'
    text = re.sub(r'\b([a-zA-Z0-9_\.]+(?:\[[^\]]+\])?)\s+as\s+([a-zA-Z0-9_\*]+)\b', r'@cast_unchecked<\2>(\1)', text)
    text = re.sub(r'\(([^\)]+)\)\s+as\s+([a-zA-Z0-9_\*]+)\b', r'@cast_unchecked<\2>(\1)', text)

    text = text.replace('valueue', 'value')

    if orig != text:
        with open(file, 'w') as f:
            f.write(text)
        print(f"Fixed {file}")

