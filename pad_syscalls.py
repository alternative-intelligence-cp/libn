import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
    
    def repl(m):
        nr = m.group(1)
        args_str = m.group(2).strip()
        if args_str.startswith(','):
            args_str = args_str[1:].strip()
        
        if not args_str:
            args = []
        else:
            args = [a.strip() for a in args_str.split(',')]
            
        while len(args) < 6:
            args.append('0i64')
            
        return f'sys({nr}, {", ".join(args)})'
    
    c = re.sub(r'\b(?:sys_safe[0-6]?|sys_full[0-6]?|sys_raw[0-6]?|sys[0-6])\s*\(\s*(SYS_[A-Z0-9_]+)(.*?)\)', repl, c)
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Padded syscalls.")
