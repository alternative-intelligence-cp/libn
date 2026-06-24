import re
import os

for root, _, fs in os.walk('src'):
    for file in fs:
        if not file.endswith('.npk'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            c = f.read()

        c = c.replace('!charset_test(', '(raw charset_test(')
        # Wait, if I replace `!charset_test(...)` with `(raw charset_test(...)`, I need to add ` == false)`!
        # Let's use regex!
        c = re.sub(r'!charset_test\(([^)]+)\)', r'(raw charset_test(\1) == false)', c)
        c = re.sub(r'charset_test\(', r'raw charset_test(', c)
        
        # fix the ones I broke: `raw raw charset_test`
        c = c.replace('raw raw charset_test', 'raw charset_test')
        
        c = re.sub(r'!has_nul_byte\(([^)]+)\)', r'(raw has_nul_byte(\1) == false)', c)
        c = re.sub(r'has_nul_byte\(', r'raw has_nul_byte(', c)
        c = c.replace('raw raw has_nul_byte', 'raw has_nul_byte')
        
        c = re.sub(r'!strcmp_has_nul\(([^)]+)\)', r'(raw strcmp_has_nul(\1) == false)', c)
        c = re.sub(r'strcmp_has_nul\(', r'raw strcmp_has_nul(', c)
        c = c.replace('raw raw strcmp_has_nul', 'raw strcmp_has_nul')
        
        with open(path, 'w') as f:
            f.write(c)

