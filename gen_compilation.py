import os
import subprocess

out_path = '/home/randy/Workspace/META/LIBN/audits/a37/compilation.md'
src_dir = '/home/randy/Workspace/REPOS/libn/src'

os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w') as f:
    f.write("# Libn Compilation for Audit A37\n\n")
    for root, dirs, files in os.walk(src_dir):
        for file in sorted(files):
            if file.endswith('.npk'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, '/home/randy/Workspace/REPOS/libn')
                f.write(f"### File: {rel_path}\n\n```nitpick\n")
                with open(full_path, 'r') as src_file:
                    f.write(src_file.read())
                f.write("\n```\n\n")

    f.write("# Build Output\n\n```\n")
    result = subprocess.run(['npkc', 'src/all.npk'], cwd='/home/randy/Workspace/REPOS/libn', capture_output=True, text=True)
    f.write(result.stdout)
    f.write(result.stderr)
    f.write("\n```\n")
