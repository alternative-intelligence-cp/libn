import re

with open('src/str/strchr.npk', 'r') as f:
    text = f.read()

def fix_func_any_any(func_name, code):
    # Match pub func:<func_name> = int64(int64:a, int64:b) {
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = any->(any->:\1_any, any->:\2_any) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64:\2 = @cast_unchecked<int64>(\2_any);'
    code = re.sub(pattern, replacement, code)
    return code

def fix_func_any_int(func_name, code):
    # Match pub func:<func_name> = int64(int64:s, int64:c) {
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = any->(any->:\1_any, int64:\2) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);'
    code = re.sub(pattern, replacement, code)
    return code

def fix_func_ret_int_any_any(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:([a-zA-Z0-9_]+),\s*int64:([a-zA-Z0-9_]+)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:\1_any, any->:\2_any) {\n    int64:\1 = @cast_unchecked<int64>(\1_any);\n    int64:\2 = @cast_unchecked<int64>(\2_any);'
    code = re.sub(pattern, replacement, code)
    return code

text = fix_func_any_int('str_strchr', text)
text = fix_func_any_int('str_strchrnul', text)
text = fix_func_any_int('str_strrchr', text)
text = fix_func_any_any('str_strstr', text)
text = fix_func_any_any('str_strcasestr', text)
text = fix_func_any_any('str_strpbrk', text)
text = fix_func_ret_int_any_any('str_strspn', text)
text = fix_func_ret_int_any_any('str_strcspn', text)

# Now, we need to cast the returns in functions that now return any->.
# Instead of doing it globally, let's just do it globally but exclude strspn/strcspn which are at the bottom.
# Actually, str_strspn starts at line ~280.
# Let's split the text before str_strspn.
idx = text.find('pub func:str_strspn')
part1 = text[:idx]
part2 = text[idx:]

part1 = part1.replace('pass 0i64;', 'pass @cast_unchecked<any->>(0i64);')
part1 = re.sub(r'pass ([a-zA-Z0-9_]+ \+ [a-zA-Z0-9_]+);', r'pass @cast_unchecked<any->>(\1);', part1)
part1 = re.sub(r'pass ([a-zA-Z0-9_]+);', r'pass @cast_unchecked<any->>(\1);', part1)

# fix the regex that messed up 'pass @cast_unchecked<any->>(0i64);' -> 'pass @cast_unchecked<any->>(@cast_unchecked<any->>(0i64));'
part1 = part1.replace('pass @cast_unchecked<any->>(@cast_unchecked<any->>(0i64));', 'pass @cast_unchecked<any->>(0i64);')

with open('src/str/strchr.npk', 'w') as f:
    f.write(part1 + part2)

