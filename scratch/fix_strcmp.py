import re

with open('src/str/strcmp.npk', 'r') as f:
    text = f.read()

def fix_func_any_any(func_name, code):
    # Match pub func:<func_name> = int64(int64:a, int64:b) {
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any, any->:\2_any) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64:\2 = @cast_unchecked<int64>(\2_any);'
    code = re.sub(pattern, replacement, code)
    return code

def fix_func_any_any_int(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any, any->:\2_any, int64:\3) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64:\2 = @cast_unchecked<int64>(\2_any);'
    code = re.sub(pattern, replacement, code)
    return code

def fix_func_bool_any_any(func_name, code):
    pattern = r'pub func:' + func_name + r' = bool\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = bool(any->:\1_any, any->:\2_any) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64:\2 = @cast_unchecked<int64>(\2_any);'
    code = re.sub(pattern, replacement, code)
    return code

text = fix_func_any_any('str_strcmp', text)
text = fix_func_any_any_int('str_strncmp', text)
text = fix_func_bool_any_any('str_strcmp_prefix', text)
text = fix_func_any_any('str_strcasecmp', text)
text = fix_func_any_any_int('str_strncasecmp', text)
text = fix_func_bool_any_any('str_casecmp_prefix', text)

with open('src/str/strcmp.npk', 'w') as f:
    f.write(text)

