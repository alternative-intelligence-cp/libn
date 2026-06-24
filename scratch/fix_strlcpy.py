import re

with open('src/str/strlcpy.npk', 'r') as f:
    text = f.read()

def fix_func(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any, any->:\2_any, int64:\3) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64:\2 = @cast_unchecked<int64>(\2_any);'
    return re.sub(pattern, replacement, code)

text = fix_func('str_strlcpy', text)
text = fix_func('str_strlcat', text)
text = fix_func('str_strscpy', text)
text = fix_func('str_strscpy_pad', text)
text = fix_func('str_strlcpy_chk', text)

with open('src/str/strlcpy.npk', 'w') as f:
    f.write(text)

