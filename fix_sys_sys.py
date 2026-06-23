import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
    
    c = re.sub(r'\bsys\(\s*SYS_([A-Z0-9_]+)', r'sys(\1', c)
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Fixed sys(SYS_ to sys(")
