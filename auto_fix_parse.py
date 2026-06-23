import subprocess
import re

while True:
    res = subprocess.run(["npkc", "test_all.npk"], capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    errors = re.findall(r"Parse error in ([^:]+): Parse error at line (\d+)", out)
    if not errors:
        break
        
    fixed_something = False
    for path, line_str in errors:
        line_num = int(line_str)
        with open(path, 'r') as f:
            lines = f.readlines()
            
        target_idx = line_num - 1
        if 0 <= target_idx < len(lines):
            line = lines[target_idx]
            if " {" in line and ") {" not in line:
                lines[target_idx] = line.replace(" {", ") {")
                fixed_something = True
                
            elif " < " in line and "if" in line and "{" not in line:
                # math.npk line 100 might be broken across lines or have < missing {
                if "if (a < 0i64" in line:
                    lines[target_idx] = "    if (a < 0i64) {\n"
                    fixed_something = True
            
            # math.npk line 106, 108
            if line_num == 106 and "math.npk" in path:
                lines[target_idx] = "};\n"
                fixed_something = True
            if line_num == 108 and "math.npk" in path:
                lines[target_idx] = ""
                fixed_something = True

            with open(path, 'w') as f:
                f.writelines(lines)
                
    if not fixed_something:
        break
