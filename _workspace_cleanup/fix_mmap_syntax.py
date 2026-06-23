import re
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# Fix closing braces for functions
text = re.sub(r'^\}\n', '};\n', text, flags=re.MULTILINE)

# Fix if statements: if condition { -> if (condition) {
# Need to be careful. Let's just find specific instances:
text = re.sub(r'if length <= 0i64 \{', 'if (length <= 0i64) {', text)
text = re.sub(r'if n <= 0i64 \{', 'if (n <= 0i64) {', text)
text = re.sub(r'if r\.is_error \{', 'if (r.is_error) {', text)
text = re.sub(r'if !r\.is_error \{', 'if (!r.is_error) {', text)
text = re.sub(r'if ptr == 0i64 \{', 'if (ptr == 0i64) {', text)
text = re.sub(r'if new_size == 0i64 \{', 'if (new_size == 0i64) {', text)
text = re.sub(r'if new_r\.is_error \{', 'if (new_r.is_error) {', text)
text = re.sub(r'if !rr\.is_error \{', 'if (!rr.is_error) {', text)
text = re.sub(r'if size > 0i64 && n > \(9223372036854775807i64 / size\) \{', 'if (size > 0i64 && n > (9223372036854775807i64 / size)) {', text)
text = re.sub(r'if n <= 0i64 \|\| size <= 0i64 \{', 'if (n <= 0i64 || size <= 0i64) {', text)

# Fix pointers: *int64:hdr = map_start as *int64; -> int64->:hdr = @cast_unchecked<int64->>(map_start);
text = re.sub(r'\*int64:hdr = map_start as \*int64;', r'int64->:hdr = @cast_unchecked<int64->>(map_start);', text)
text = re.sub(r'\*int64:new_hdr = new_map as \*int64;', r'int64->:new_hdr = @cast_unchecked<int64->>(new_map);', text)
text = re.sub(r'\*int64:hdr = ptr as \*int64;', r'int64->:hdr = @cast_unchecked<int64->>(ptr);', text)
text = re.sub(r'\*byte:src = ptr as \*byte;', r'uint8->:src = @cast_unchecked<uint8->>(ptr);', text)
text = re.sub(r'\*byte:dst = new_ptr as \*byte;', r'uint8->:dst = @cast_unchecked<uint8->>(new_ptr);', text)

# Fix fail: fail ERR_BADARG as tbb8; -> fail ERR_BADARG;
text = re.sub(r'fail ERR_BADARG as tbb8;', 'fail ERR_BADARG;', text)
text = re.sub(r'fail ERR_OVERFLOW as tbb8;', 'fail ERR_OVERFLOW;', text)

# Fix r.err -> r.error
text = re.sub(r'r\.err;', 'r.error;', text)

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

