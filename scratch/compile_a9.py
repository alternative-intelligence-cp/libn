import os
import glob

# Ensure directory exists
os.makedirs('/home/randy/Workspace/META/LIBN/audits/a9', exist_ok=True)

out_file = '/home/randy/Workspace/META/LIBN/audits/a9/compilation.md'
with open(out_file, 'w') as f_out:
    f_out.write('# libn A9 Source Compilation\n\n')
    
    # Get all .npk files recursively
    files = glob.glob('/home/randy/Workspace/REPOS/libn/src/**/*.npk', recursive=True)
    # Sort files for consistency
    files.sort()
    
    for filepath in files:
        rel_path = os.path.relpath(filepath, '/home/randy/Workspace/REPOS/libn/')
        f_out.write(f'## `{rel_path}`\n\n')
        f_out.write('```nitpick\n')
        with open(filepath, 'r') as f_in:
            f_out.write(f_in.read())
        if not f_out.tell() or not open(filepath, 'r').read().endswith('\n'):
            f_out.write('\n')
        f_out.write('```\n\n')

print("A9 Compilation successful.")
