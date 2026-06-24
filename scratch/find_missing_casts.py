import os
import re

funcs_expecting_any = {
    'str_strlen': [1],
    'str_strcmp': [1, 2],
    'str_strncmp': [1, 2],
    'str_strcasecmp': [1, 2],
    'str_strncasecmp': [1, 2],
    'str_casecmp_prefix': [1, 2],
    'str_parse_i64': [1],
    'str_parse_u64': [1],
    'mem_memcpy': [1, 2],
    'libn_write_all': [2],
    'io_write_n': [2],
    'slab_free': [2],
    'libn_slab_free': [1],
}

def check_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if '//' in line:
            line = line[:line.index('//')]
        for func, any_args in funcs_expecting_any.items():
            for m in re.finditer(r'\b' + func + r'\s*\(([^)]+)\)', line):
                args = m.group(1).split(',')
                for arg_idx in any_args:
                    arg_idx -= 1
                    if arg_idx < len(args):
                        arg = args[arg_idx].strip()
                        if not arg.startswith('@cast') and not arg.startswith('"') and not arg.endswith('i64') and not arg.endswith('u8'):
                            print(f"{path}:{idx+1}: {func} called with uncast arg {arg_idx+1}: {arg}")

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            check_file(os.path.join(root, file))

