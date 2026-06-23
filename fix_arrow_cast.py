import os, glob, re

for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        s = f.read()
        
    new_s = re.sub(r'(\w+)->@cast_unchecked<([^>]+)>\((\w+)\)', r'@cast_unchecked<\2>(\1->\3)', s)
    
    if s != new_s:
        with open(filepath, 'w') as f:
            f.write(new_s)
            print(f"Fixed {filepath}")
