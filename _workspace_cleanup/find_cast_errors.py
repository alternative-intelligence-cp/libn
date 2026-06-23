import subprocess

out = subprocess.run(["npkc", "test_root.npk"], capture_output=True, text=True)
lines = out.stderr.splitlines()

for i, line in enumerate(lines):
    if "Cannot cast 'Result<int64>' to 'int64'" in line:
        print(f"Error at: {line}")
        # Print a few lines before to see if there's a file context
        for j in range(max(0, i-3), i):
            print(f"  {lines[j]}")
