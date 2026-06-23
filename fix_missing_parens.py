import subprocess
import re

while True:
    res = subprocess.run(["npkc", "test_all.npk"], capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    errors = re.findall(r"Parse error in ([^:]+): Parse error at line (\d+)", out)
    if not errors:
        print("No more errors!")
        break
        
    fixed_something = False
    files_to_fix = set()
    for path, line_str in errors:
        line_num = int(line_str)
        files_to_fix.add((path, line_num))
        
    for path, line_num in files_to_fix:
        with open(path, 'r') as f:
            lines = f.readlines()
            
        target_idx = line_num - 1
        if 0 <= target_idx < len(lines):
            line = lines[target_idx]
            if " {" in line and ") {" not in line and "if " in line:
                lines[target_idx] = line.replace(" {", ") {")
                fixed_something = True
                
            elif " {" in line and ") {" not in line and "while " in line:
                lines[target_idx] = line.replace(" {", ") {")
                fixed_something = True
                
            # Specifically check for math.npk line 106
            if line_num == 106 and "math.npk" in path:
                # We tried fixing math.npk manually. Let's see if we can overwrite it correctly.
                pass

        if fixed_something:
            with open(path, 'w') as f:
                f.writelines(lines)
                
    if not fixed_something:
        print("Couldn't auto-fix anything. Exiting loop.")
        break

