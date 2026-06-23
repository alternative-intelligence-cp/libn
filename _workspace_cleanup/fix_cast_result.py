import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Fix @cast_unchecked<int64>(r) to @cast_unchecked<int64>(r.error)
    content = re.sub(r'int64:e = @cast_unchecked<int64>\((r|wr|r1|r2|res|res1|res2|r_in|r_out)\);', r'int64:e = @cast_unchecked<int64>(\1.error);', content)
    
    # Fix `fail r;` to `fail e;` where `e` was just defined.
    # Actually, we can just replace `fail r;` with `fail \1.error;` if \1 is r.
    # Let's just do:
    content = re.sub(r'fail (r|wr|r1|r2|res|res1|res2|r_in|r_out);', r'fail \1.error;', content)

    # Some `fail r.error;` might fail if r is NOT a result. But `fail` is usually on an error code or a Result's error field.
    # Let's see if this works.

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    if 'io' not in root: continue
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
