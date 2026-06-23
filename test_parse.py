import subprocess
out = subprocess.run(["/home/randy/Workspace/REPOS/nitpick/build/npkc", "src/all.npk"], capture_output=True, text=True).stderr
for i, line in enumerate(out.split('\n')):
    if "Line 214, Column 9" in line:
        print("FOUND Line 214")
        # print 5 lines before and after
        lines = out.split('\n')
        for j in range(max(0, i-5), min(len(lines), i+5)):
            print(lines[j])
