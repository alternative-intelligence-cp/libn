import os
import subprocess
import re

npkc = '/home/randy/Workspace/REPOS/nitpick/build/npkc'
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

while True:
    errors = []
    
    # Run compiler on all files
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                path = os.path.join(root, file)
                res = subprocess.run([npkc, path], capture_output=True, text=True)
                clean_out = ansi_escape.sub('', res.stdout + res.stderr)
                
                # Parse errors
                for line in clean_out.splitlines():
                    # Format: "path:0:0: error: Line 123, Column 45: msg"
                    m = re.match(r'^([^:]+):0:0:\s*error:\s*Line (\d+),\s*Column\s*(\d+):\s*(.*)', line)
                    if m:
                        errors.append({
                            'file': m.group(1),
                            'line': int(m.group(2)),
                            'col': int(m.group(3)),
                            'msg': m.group(4)
                        })
                    else:
                        m2 = re.match(r'^([^:]+):(\d+):(\d+):\s*error:\s*(.*)', line)
                        if m2:
                            errors.append({
                                'file': m2.group(1),
                                'line': int(m2.group(2)),
                                'col': int(m2.group(3)),
                                'msg': m2.group(4)
                            })

    if not errors:
        print("No errors left!")
        break

    fixes = 0
    # Process errors
    files_to_fix = {}
    for err in errors:
        filepath = err['file']
        if filepath not in files_to_fix:
            with open(filepath, 'r') as f:
                files_to_fix[filepath] = f.read().splitlines()
        
        lines = files_to_fix[filepath]
        line_idx = err['line'] - 1
        
        if line_idx >= len(lines):
            continue

        msg = err['msg']
        
        if 'Expected \';\' after function declaration' in msg or 'Functions end with' in msg:
            if lines[line_idx].strip() == '}':
                lines[line_idx] = lines[line_idx].replace('}', '};')
                fixes += 1
            elif line_idx > 0 and lines[line_idx-1].strip() == '}':
                lines[line_idx-1] = lines[line_idx-1].replace('}', '};')
                fixes += 1
            elif line_idx > 1 and lines[line_idx-2].strip() == '}':
                lines[line_idx-2] = lines[line_idx-2].replace('}', '};')
                fixes += 1
            elif line_idx < len(lines) - 1 and lines[line_idx+1].strip() == '}':
                lines[line_idx+1] = lines[line_idx+1].replace('}', '};')
                fixes += 1
                
        elif 'Expected statement or block after if condition' in msg:
            pass
            
    if fixes == 0:
        print(f"No auto-fixes applied. {len(errors)} errors remain.")
        break
        
    for filepath, lines in files_to_fix.items():
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines) + '\n')
            
    print(f"Applied {fixes} fixes.")

