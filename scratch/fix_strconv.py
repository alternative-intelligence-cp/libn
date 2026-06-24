import re

with open('src/str/strconv.npk', 'r') as f:
    text = f.read()

def fix_func_s(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);'
    return re.sub(pattern, replacement, code)

def fix_func_s_base(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any, int64:\2) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);'
    return re.sub(pattern, replacement, code)

def fix_func_strtol(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64->:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any, any->:\2_any, int64:\3) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64->:\2 = @cast_unchecked<int64->>(\2_any);'
    return re.sub(pattern, replacement, code)

def fix_func_itoa(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:v, int64:buf, int64:buf_size\) \{'
    replacement = r'pub func:' + func_name + r' = int64(int64:v, any->:buf_any, int64:buf_size) {\n    int64:buf = @cast_unchecked<int64>(buf_any);'
    return re.sub(pattern, replacement, code)

def fix_func_itoa_hex(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:v, int64:buf, int64:buf_size, bool:include_prefix\) \{'
    replacement = r'pub func:' + func_name + r' = int64(int64:v, any->:buf_any, int64:buf_size, bool:include_prefix) {\n    int64:buf = @cast_unchecked<int64>(buf_any);'
    return re.sub(pattern, replacement, code)

text = fix_func_s('str_atoi', text)
text = fix_func_s('str_parse_i64', text)
text = fix_func_s('str_parse_u64', text)
text = fix_func_s_base('str_parse_i64_base', text)
text = fix_func_strtol('str_strtol', text)
text = fix_func_strtol('str_strtoul', text)
text = fix_func_itoa('str_itoa', text)
text = fix_func_itoa('str_utoa', text)
text = fix_func_itoa_hex('str_itoa_hex', text)

with open('src/str/strconv.npk', 'w') as f:
    f.write(text)

