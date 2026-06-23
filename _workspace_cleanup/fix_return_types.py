import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # If the language auto-wraps all function returns into Result<T>,
    # then any function explicitly declared as returning Result<T> will become Result<Result<T>>.
    # We should strip Result<...> from function declarations globally!
    # Example: pub func:foo = Result<int64>(...) -> pub func:foo = int64(...)
    code = re.sub(r'func:([a-zA-Z0-9_]+)\s*=\s*Result<([^>]+)>\(', r'func:\1 = \2(', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
