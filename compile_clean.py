import os
import subprocess

src_dir = '/home/randy/Workspace/REPOS/libn/src'
npkc = '/home/randy/Workspace/REPOS/nitpick/build/npkc'

total_errors = 0
for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            res = subprocess.run([npkc, path], capture_output=True, text=True)
            err_count = res.stdout.count('error:')
            if err_count > 0:
                print(f"{path}: {err_count} errors")
                total_errors += err_count

print(f"Total errors: {total_errors}")
