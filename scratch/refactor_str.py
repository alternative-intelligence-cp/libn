import os, re

ptr_args = ['s', 'src', 'dst', 'str', 'prefix', 'suffix', 'needle', 'haystack', 'fmt', 'min_str']
ptr_ret_funcs = ['str_strcpy', 'str_stpcpy', 'str_strncpy', 'str_stpncpy', 'str_strdup', 'str_strndup', 'str_strlcpy', 'str_strlcat', 'str_strscpy', 'str_strscpy_pad', 'str_strchr', 'str_strrchr', 'str_strchrnul', 'str_strtok_r', 'str_strstr']

def refactor_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'pub func:' in line or 'func:' in line:
            # Change return type if in ptr_ret_funcs
            for fn in ptr_ret_funcs:
                if f'func:{fn} = int64(' in line:
                    line = line.replace(f'func:{fn} = int64(', f'func:{fn} = any->(')
            
            # Change params
            for arg in ptr_args:
                line = re.sub(rf'\bint64:{arg}\b', f'any->:{arg}', line)
            
            lines[i] = line
        else:
            # Change NULL checks
            for arg in ptr_args:
                line = re.sub(rf'\b{arg} == 0i64\b', f'{arg} == NULL', line)
                line = re.sub(rf'\b{arg} != 0i64\b', f'{arg} != NULL', line)
            
            lines[i] = line
            
    content = '\n'.join(lines)
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src/str'):
    for file in files:
        if file.endswith('.npk'):
            refactor_file(os.path.join(root, file))
