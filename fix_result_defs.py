import os
import re

for root, _, fs in os.walk('src'):
    for file in fs:
        if not file.endswith('.npk'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            c = f.read()

        # Fix `func:foo = Result<T>(...)` to `func:foo = T(...)`
        c = re.sub(r'(func:[a-zA-Z0-9_]+) = Result<([a-zA-Z0-9_<>]+)>\(', r'\1 = \2(', c)

        with open(path, 'w') as f:
            f.write(c)

