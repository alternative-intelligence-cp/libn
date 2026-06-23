import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Find @cast_unchecked<int64>("something") and replace with @cast_unchecked<int64>(@"something")
    # Make sure to handle escaping inside the string correctly, or just use a simple regex since it's only simple strings.
    new_content = re.sub(r'@cast_unchecked<int64>\("([^"]+)"\)', r'@cast_unchecked<int64>(@"\1")', content)

    if new_content != content:
        with open(path, 'w') as f:
            f.write(new_content)
        print(f"Fixed {path}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            fix_file(os.path.join(root, file))
