import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    text = text.replace('*int64[]', 'int64->')

    with open(file, 'w') as f:
        f.write(text)

