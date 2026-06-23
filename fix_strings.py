import os

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Replace fixed string:var = "..." with fixed int64:var = @"..."
    import re
    content = re.sub(r'fixed string:([a-zA-Z0-9_]+)\s*=\s*"([^"]+)";', r'fixed int64:\1 = @"\2";', content)
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('/home/randy/Workspace/REPOS/libn/src/io/bio/strerror.npk')
fix_file('/home/randy/Workspace/REPOS/libn/src/io/bio/tmpfile.npk')

print("Fixed strings")
