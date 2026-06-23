import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
        
    # void to NIL
    c = re.sub(r'\bvoid\b', 'NIL', c)
    
    # sys_write -> sys(SYS_WRITE, ...)
    # Wait, if it is sys_write(fd, buf, size), I should replace it with sys(SYS_WRITE, fd, buf, size, 0, 0, 0)
    c = re.sub(r'sys_write\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'sys(SYS_WRITE, \1, \2, \3, 0i64, 0i64, 0i64)', c)
    c = re.sub(r'sys_read\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'sys(SYS_READ, \1, \2, \3, 0i64, 0i64, 0i64)', c)
    
    # "Result<int64>:r = sys(..." -> "int64:r = sys(..."
    # Actually wait! sys() returns Result<int64>? No, it returns int64 and sets errno, or whatever.
    # What does sys() return in v0.12? It just returns the raw int64!
    # And Result<int64> is no longer a type!
    # My `fix_results.py` removed Result<int64> in function definitions, but DID IT remove it in variable declarations?
    c = re.sub(r'Result<int64>:\s*([a-zA-Z0-9_]+)\s*=\s*', r'int64:\1 = ', c)
    c = re.sub(r'Result<int32>:\s*([a-zA-Z0-9_]+)\s*=\s*', r'int32:\1 = ', c)
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Fixed void and sys_write/read.")
