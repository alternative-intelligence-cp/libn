import os
import re

src_dir = '/home/randy/Workspace/REPOS/libn/src'

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            orig_content = content

            # Replace pointer types
            content = content.replace('uint8->', '*byte')
            content = content.replace('StrView->', '*StrView')
            content = content.replace('StrViewIter->', '*StrViewIter')
            content = content.replace('StrBuf->', '*StrBuf')

            # Replace casts:  expr => *byte  ->  @cast_unchecked<*byte>(expr)
            # We need a regex because `expr` can be `path`, `s->ptr`, `@table[0]`, `(s+i)`
            # We can find `=> *byte` and then manually fix the few occurrences, or use a smart regex.
            # But wait, did I use `=> uint8->`? Yes, which became `=> *byte`.
            # Let's replace `([a-zA-Z0-9_>\[\]@]+)\s*=>\s*\*([A-Za-z0-9_]+)`
            # Let's match typical expressions:
            content = re.sub(r'([a-zA-Z0-9_]+(?:->[a-zA-Z0-9_]+)?(?:\[[^\]]+\])?)\s*=>\s*\*([a-zA-Z0-9_]+)', r'@cast_unchecked<*\2>(\1)', content)
            
            # Special case for `@table[0] => *byte`
            content = re.sub(r'(@[a-zA-Z0-9_]+\[[^\]]+\])\s*=>\s*\*([a-zA-Z0-9_]+)', r'@cast_unchecked<*\2>(\1)', content)

            if content != orig_content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed {filepath}")
