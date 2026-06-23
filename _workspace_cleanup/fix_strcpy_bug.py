import os
filepath = 'src/str/strcpy.npk'
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    code = code.replace('pass dst + i;  // points to the NUL uint8 };', 'pass dst + i;\n};\n// points to the NUL uint8')
    with open(filepath, 'w') as f:
        f.write(code)
