import os
import re

def fix_raw_drop(code):
    # Fix 'drop function(args);' to 'drop(function(args));'
    # We look for 'drop ' followed by an identifier and an opening paren.
    # Then we need to find the matching closing paren, which is usually right before the semicolon.
    # Actually, a simple regex works if the statement ends with ;
    code = re.sub(r'\bdrop\s+([a-zA-Z0-9_]+)\((.*?)\);', r'drop(\1(\2));', code)
    
    # Fix 'raw function(args)' to 'raw(function(args))'
    # 'raw ' could be inside an assignment: int64:x = raw sys(...);
    code = re.sub(r'\braw\s+([a-zA-Z0-9_]+)\((.*?)\);', r'raw(\1(\2));', code)
    code = re.sub(r'\braw\s+([a-zA-Z0-9_]+)\((.*?)\)\s*,', r'raw(\1(\2)),', code) # If in an argument list
    
    return code

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                code = f.read()
            new_code = fix_raw_drop(code)
            if code != new_code:
                with open(path, 'w') as f:
                    f.write(new_code)
                print(f"Fixed {path}")
