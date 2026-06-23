import os
import glob

src_dir = '/home/randy/Workspace/REPOS/libn/src'
out_path = '/home/randy/Workspace/META/LIBN/audits/a6/compilation.md'

os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w') as out_f:
    out_f.write('# Source Compilation\n\n')
    for root, _, files in os.walk(src_dir):
        for file in sorted(files):
            if file.endswith('.npk'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, '/home/randy/Workspace/REPOS/libn')
                out_f.write(f'## {rel_path}\n\n```nitpick\n')
                with open(full_path, 'r') as in_f:
                    out_f.write(in_f.read())
                out_f.write('\n```\n\n')
