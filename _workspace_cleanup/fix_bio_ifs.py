import glob
import re

for filepath in glob.glob('src/io/bio/*.npk'):
    with open(filepath, 'r') as f:
        text = f.read()
        
    text = re.sub(r'if ([^{]+) \{', r'if (\1) {', text)
    text = re.sub(r'while ([^{]+) \{', r'while (\1) {', text)
    
    # Fix double parens like if ((x)) { -> maybe fine
    
    with open(filepath, 'w') as f:
        f.write(text)
