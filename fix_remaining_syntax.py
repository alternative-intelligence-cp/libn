import glob, re

for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        s = f.read()

    # Fix )) { -> ) { globally
    s = s.replace(')) {', ') {')
    s = s.replace('};;', '};')
    
    # Fix while n > 0i64 { -> while (n > 0i64) {
    s = re.sub(r'while\s+([^{]*?)\s*\{', r'while (\1) {', s)
    s = re.sub(r'while\s+\(\((.*?)\)\)\s*\{', r'while (\1) {', s)

    with open(filepath, 'w') as f:
        f.write(s)
