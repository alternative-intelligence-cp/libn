import os
import subprocess

for root, _, files in os.walk('src/io/bio'):
    for file in files:
        if not file.endswith('.npk'): continue
        filepath = os.path.join(root, file)
        
        with open('test_dummy.npk', 'w') as f:
            f.write(f'use "{filepath}".*;\npub func:failsafe = int32(tbb32:err) {{ exit 1i32; }};\npub func:main = int32() {{ exit 0i32; }};\n')
        
        res = subprocess.run(['npkc', 'test_dummy.npk'], capture_output=True, text=True)
        if "Undefined identifier: 'r'" in res.stderr:
            print(f"File {filepath} has undefined 'r'")
            for line in res.stderr.splitlines():
                if "Undefined identifier: 'r'" in line:
                    print(line)
