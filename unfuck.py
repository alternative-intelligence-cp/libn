import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    orig = content

    # Fix the corrupted type declarations
    content = re.sub(r'(func|int64|bool|byte|uint8|uint8->|FILE->|Result<int64>|void)\) \? ', r'\1:', content)
    
    # Fix the weird spaces introduced around colons
    content = re.sub(r'(int64|bool|byte|uint8|uint8->|FILE->|void) : ', r'\1:', content)

    # Fix corrupted comments and strings (due to bad replace of " is " with " (")
    content = content.replace('(the path (longer', 'the path is longer')
    content = content.replace('If b (absolute', 'If b is absolute')
    content = content.replace('If a (empty', 'If a is empty')
    content = content.replace('a ("/"', 'a == "/"')
    content = content.replace('// Examples) ? ', '// Examples:')
    content = content.replace('// Returns) ? ', '// Returns:')
    content = content.replace('// Note) ? ', '// Note:')
    content = content.replace('// Rules) ? ', '// Rules:')
    content = content.replace('// Functions) ? ', '// Functions:')

    # Fix bad casts generated from `=> pass` match arms
    content = re.sub(r'@cast_unchecked<pass>\((.*?)\)\s*', r'\1 => pass ', content)
    
    # Fix extra parentheses added to `=> pass (8i64)`
    content = re.sub(r'=> pass \((.*?)\);', r'=> pass \1;', content)

    if orig != content:
        with open(path, 'w') as f:
            f.write(content)
        print("Fixed", path)

def main():
    src_dir = '/home/randy/Workspace/REPOS/libn/src'
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.npk'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
