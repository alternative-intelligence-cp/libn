import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

# Add missing imports
if 'use "../syscall/syscall.npk".*;' not in text:
    text = text.replace('use "../syscall/errno.npk".*;\n', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/slab.npk".*;\nuse "../str/strchr.npk".*;\nuse "../str/strcmp.npk".*;\n')

# There are many functions with `int64:data` representing string pointer.
# Let's fix `strview_make`
text = re.sub(
    r'pub func:strview_make = strview_t\(int64:data, int64:len\) \{',
    r'pub func:strview_make = strview_t(any->:data_any, int64:len) {\n    int64:data = @cast_unchecked<int64>(data_any);',
    text
)
# `strview_from_str`
text = re.sub(
    r'pub func:strview_from_str = strview_t\(int64:data\) \{',
    r'pub func:strview_from_str = strview_t(any->:data_any) {\n    int64:data = @cast_unchecked<int64>(data_any);',
    text
)
# `strview_from_buf`
text = re.sub(
    r'pub func:strview_from_buf = strview_t\(int64:buf\) \{',
    r'pub func:strview_from_buf = strview_t(any->:buf_any) {\n    int64:buf = @cast_unchecked<int64>(buf_any);',
    text
)

# And now fix all calls to functions that expect `any->`
# mem_memcpy(..., ..., ...)
text = re.sub(r'mem_memcpy\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_memcpy(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)

# str_strlen(data)
text = re.sub(r'str_strlen\(([^)]+)\)', r'str_strlen(@cast_unchecked<any->>(\1))', text)

# str_strchr, str_strrchr, str_strstr
text = re.sub(r'str_strchr\(([^,]+),\s*([^)]+)\)', r'str_strchr(@cast_unchecked<any->>(\1), \2)', text)
text = re.sub(r'str_strrchr\(([^,]+),\s*([^)]+)\)', r'str_strrchr(@cast_unchecked<any->>(\1), \2)', text)
text = re.sub(r'str_strstr\(([^,]+),\s*([^)]+)\)', r'str_strstr(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2))', text)

# str_strcmp, str_strncmp, str_strcasecmp, str_strncasecmp
text = re.sub(r'str_strcmp\(([^,]+),\s*([^)]+)\)', r'str_strcmp(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2))', text)
text = re.sub(r'str_strncmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'str_strncmp(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)
text = re.sub(r'str_strcasecmp\(([^,]+),\s*([^)]+)\)', r'str_strcasecmp(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2))', text)
text = re.sub(r'str_strncasecmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'str_strncasecmp(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)

# libn_write_all
text = re.sub(r'libn_write_all\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'libn_write_all(\1, @cast_unchecked<any->>(\2), \3)', text)

# str_strtol, str_strtoul
text = re.sub(r'str_strtol\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'str_strtol(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)
text = re.sub(r'str_strtoul\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'str_strtoul(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

