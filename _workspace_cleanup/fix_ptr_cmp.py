import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()

    # str_strtol and str_strtoul
    code = re.sub(r'if \((endptr) (!=|==) 0i64\)', r'if (@cast_unchecked<int64>(\1) \2 0i64)', code)
    # str_strtok_r
    code = re.sub(r'if \((saveptr) (!=|==) 0i64\)', r'if (@cast_unchecked<int64>(\1) \2 0i64)', code)
    # str_strsep
    code = re.sub(r'if \((stringp) (!=|==) 0i64', r'if (@cast_unchecked<int64>(\1) \2 0i64', code)

    with open(filepath, 'w') as f:
        f.write(code)

fix_file('src/str/strconv.npk')
fix_file('src/str/strtok.npk')
