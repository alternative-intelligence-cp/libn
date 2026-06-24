import os
import re

FUNCTIONS = {
    'mem_memcpy': [0, 1],
    'mem_mempcpy': [0, 1],
    'mem_memmove': [0, 1],
    'mem_memdup': [0],
    'str_strcpy': [0, 1],
    'str_strncpy': [0, 1],
    'str_strcmp': [0, 1],
    'str_strncmp': [0, 1],
    'str_strlen': [0],
    'str_strnlen': [0],
    'libn_read': [1],
    'libn_write': [1],
    'libn_open': [0],
    'libn_openat': [1],
    'libn_pread': [1],
    'libn_pwrite': [1],
    'libn_mmap': [0],
    'libn_mprotect': [0],
    'libn_mremap': [0, 4],
    'libn_statx': [1, 4],
    'libn_getcwd': [0],
    'libn_chdir': [0],
    'libn_write_all': [1],
    'str_snprintf0': [0, 2],
    'str_snprintf1': [0, 2],
    'str_snprintf2': [0, 2],
    'str_snprintf3': [0, 2],
    'str_snprintf4': [0, 2],
    'str_snprintf5': [0, 2],
    'str_snprintf6': [0, 2],
    'str_snprintf7': [0, 2],
    'str_snprintf8': [0, 2],
    'str_format_args': [0, 2, 3],
    'libn_slab_free': [0],
    'str_strlcpy': [0, 1],
    'str_strlcat': [0, 1],
    'str_strscpy': [0, 1],
    'str_strscpy_pad': [0, 1],
    'str_strlcpy_chk': [0, 1]
}

def split_args(args_str):
    args = []
    current = []
    paren_depth = 0
    angle_depth = 0
    for char in args_str:
        if char == '(': paren_depth += 1
        elif char == ')': paren_depth -= 1
        elif char == '<': angle_depth += 1
        elif char == '>': angle_depth -= 1
        elif char == ',' and paren_depth == 0 and angle_depth == 0:
            args.append(''.join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        args.append(''.join(current).strip())
    return args

for root, _, files in os.walk('src'):
    for file in files:
        if not file.endswith('.npk'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            for func, any_args in FUNCTIONS.items():
                pattern = r'\b' + re.escape(func) + r'\s*\('
                matches = list(re.finditer(pattern, line))
                for match in matches:
                    start_idx = match.end()
                    args_str = ''
                    paren_depth = 1
                    curr_idx = start_idx
                    while curr_idx < len(line):
                        if line[curr_idx] == '(': paren_depth += 1
                        elif line[curr_idx] == ')':
                            paren_depth -= 1
                            if paren_depth == 0: break
                        args_str += line[curr_idx]
                        curr_idx += 1
                    
                    if paren_depth == 0:
                        args = split_args(args_str)
                        for arg_idx in any_args:
                            if arg_idx < len(args):
                                arg = args[arg_idx]
                                if not arg.startswith('@cast_unchecked') and not arg.startswith('@"'):
                                    # It might be `dst_any` or `s_any`, etc.
                                    if not arg.endswith('_any'):
                                        print(f"{path}:{i+1}: {func} ARG {arg_idx}: {arg}")

