import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
    
    c = c.replace(';;', ';')
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Fixed double semicolons.")
