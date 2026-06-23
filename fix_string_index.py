import os

def fix_file(path, var_name):
    with open(path, 'r') as f:
        content = f.read()
    
    # Replace @cast_unchecked<int64>(@var_name[0]) with @cast_unchecked<int64>(var_name)
    content = content.replace(f'@cast_unchecked<int64>(@{var_name}[0])', f'@cast_unchecked<int64>({var_name})')
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('/home/randy/Workspace/REPOS/libn/src/io/bio/strerror.npk', 'prefix')
fix_file('/home/randy/Workspace/REPOS/libn/src/io/bio/tmpfile.npk', 'pfx')

print("Fixed string indexing")
