import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
        
    c = c.replace('*int64', 'int64->')
    c = re.sub(r'\blimit\b', 'limit_val', c)
    c = re.sub(r'\braw\s+', '', c)
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Fixed final issues.")
