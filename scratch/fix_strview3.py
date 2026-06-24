import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

# Replace libn_slab_alloc_zero -> slab_alloc_zero
text = text.replace('libn_slab_alloc_zero', 'slab_alloc_zero')

# Function definitions already fixed: strview_make, strview_from_str, strview_from_buf

# Let's fix missing any-> casts
# Look for sv.data passed to string/mem functions
# Since there are many, I'll just write a script to replace sv.data and other variables when passed.
# Actually, the error says:
# Line 187, Column 22: Argument 1 has type 'int64', but function expects 'any->'
# Let's just run a generic replace for known functions:
funcs1 = ['str_strlen', 'slab_alloc_zero', 'str_strlcpy', 'str_strlcat', 'str_strscpy', 'str_strscpy_pad']
funcs2 = ['str_strchr', 'str_strrchr', 'str_strstr', 'str_strcmp', 'str_strncmp', 'str_strcasecmp', 'str_strncasecmp']
funcs3 = ['mem_memcpy', 'mem_memcmp', 'mem_memchr', 'mem_memrchr', 'mem_memset', 'mem_bzero']

# Wait, `sv.data` is an int64.
for f in funcs1 + funcs2 + funcs3:
    # A bit dangerous to blindly replace, but let's cast arguments to any-> if they are not already casted and not string literals.
    pass

# Let's just fix the remaining manually via regex
def cast(arg):
    arg = arg.strip()
    if arg.startswith('@cast_unchecked<any->>'): return arg
    # don't cast numbers like 0i64 or literals
    if arg == '0i64': return '@cast_unchecked<any->>(0i64)'
    if arg.isdigit() or arg.endswith('i64'): return arg # might be size
    return f'@cast_unchecked<any->>({arg})'

# Actually, we can use regex to replace specific lines since there are 57 errors.
# Let's just use `sed` or Python to prepend `@cast_unchecked<any->>` to all arguments for string/mem functions.
text = re.sub(r'str_strncmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strncmp({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)
text = re.sub(r'str_strcmp\(([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strcmp({cast(m.group(1))}, {cast(m.group(2))})', text)
text = re.sub(r'str_strcasecmp\(([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strcasecmp({cast(m.group(1))}, {cast(m.group(2))})', text)
text = re.sub(r'str_strncasecmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strncasecmp({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)
text = re.sub(r'str_strchr\(([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strchr({cast(m.group(1))}, {m.group(2)})', text)
text = re.sub(r'str_strrchr\(([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strrchr({cast(m.group(1))}, {m.group(2)})', text)
text = re.sub(r'str_strstr\(([^,]+),\s*([^)]+)\)', 
              lambda m: f'str_strstr({cast(m.group(1))}, {cast(m.group(2))})', text)
text = re.sub(r'str_strlen\(([^)]+)\)', 
              lambda m: f'str_strlen({cast(m.group(1))})', text)
text = re.sub(r'mem_memcpy\(([^,]+),\s*([^,]+),\s*([^)]+)\)', 
              lambda m: f'mem_memcpy({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)
text = re.sub(r'mem_memcmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', 
              lambda m: f'mem_memcmp({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

