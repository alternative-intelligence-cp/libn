import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
        
    c = re.sub(r'int64:\s*([a-zA-Z0-9_]+)\s*=\s*sys\(', r'Result<int64>:\1 = sys(', c)
    c = re.sub(r'int32:\s*([a-zA-Z0-9_]+)\s*=\s*sys\(', r'Result<int32>:\1 = sys(', c)
    
    # Also I need to remove sys_safe and just replace all uses of sys_safe with sys directly?
    # No, wait, sys_safe was dynamically taking `nr`!
    # I can't do that. I have to replace sys_safe(SYS_XXX, ...) with sys(SYS_XXX, ...) everywhere!
    c = re.sub(r'sys_safe\s*\(\s*(SYS_[A-Z0-9_]+)', r'sys(\1', c)
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Fixed Result for sys().")
