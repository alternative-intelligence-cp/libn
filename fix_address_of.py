import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    text = re.sub(r'&([a-zA-Z_])', r'@\1', text)

    with open(file, 'w') as f:
        f.write(text)

