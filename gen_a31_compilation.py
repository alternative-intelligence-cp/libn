import os
import subprocess

src_dir = '/home/randy/Workspace/REPOS/libn/src'
out_path = '/home/randy/Workspace/META/LIBN/audits/a31/compilation.md'
npkc = '/home/randy/Workspace/REPOS/nitpick/build/npkc'

os.makedirs(os.path.dirname(out_path), exist_ok=True)

build_output_lines = []
total_errors = 0
for root, _, files in os.walk(src_dir):
    for file in sorted(files):
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            res = subprocess.run([npkc, '-c', path], capture_output=True, text=True)
            
            # Filter stdout/stderr
            out_lines = [line for line in res.stdout.splitlines() if not line.startswith('[DEBUG') and not line.startswith('PARSING CAST')]
            err_lines = [line for line in res.stderr.splitlines() if not line.startswith('[DEBUG') and not line.startswith('PARSING CAST')]
            
            if out_lines or err_lines:
                build_output_lines.append(f'--- Output for {os.path.relpath(path, src_dir)} ---')
                if out_lines: build_output_lines.extend(out_lines)
                if err_lines: build_output_lines.extend(err_lines)
            
            err_count = res.stdout.count('error:')
            total_errors += err_count

if not build_output_lines:
    build_output_lines.append('Build completed successfully with no errors or warnings.')

build_output_str = '\n'.join(build_output_lines)
build_output_str += f'\n\nTotal errors: {total_errors}'

with open(out_path, 'w') as out_f:
    out_f.write('# Build Output\n\n```text\n')
    out_f.write(build_output_str)
    out_f.write('\n```\n\n')
    
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

print(f'Done generating compilation.md with {total_errors} errors.')
