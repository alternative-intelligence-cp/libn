import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    text = re.sub(r'\*byte([^\[a-zA-Z0-9_])', r'*byte[]\1', text)
    text = re.sub(r'\*int64([^\[a-zA-Z0-9_])', r'*int64[]\1', text)

    with open(file, 'w') as f:
        f.write(text)

