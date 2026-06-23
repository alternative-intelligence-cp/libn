import os
import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        content = fp.read()
        
    content = re.sub(r'@cast_unchecked<uint8>\((.*?)\)->', r'@cast_unchecked<uint8->>(\1)', content)
    
    with open(file, 'w') as fp:
        fp.write(content)

print("Fixed -> casts.")
