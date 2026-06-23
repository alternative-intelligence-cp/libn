import os, glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    text = text.replace('int64->', '*int64')
    text = text.replace('uint8->', '*uint8')
    text = text.replace('FILE->', '*FILE')
    text = text.replace('tbb8->', '*tbb8')
    text = text.replace('*int64 >', '*int64')
    text = text.replace('*uint8 >', '*uint8')
    
    with open(file, 'w') as f:
        f.write(text)
