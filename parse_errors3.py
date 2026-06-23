import subprocess

res = subprocess.run(['/home/randy/Workspace/REPOS/nitpick/build/npkc', '/home/randy/Workspace/REPOS/libn/src/proc/exit.npk'], capture_output=True, text=True)

errors = []
for line in res.stderr.split('\n'):
    if 'error:' in line and 'Line ' in line:
        errors.append(line.split('error: ')[-1])

# Just print the first 20 errors
for err in errors[:20]:
    print(err)

