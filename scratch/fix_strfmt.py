import re
with open('src/str/strfmt.npk', 'r') as f:
    text = f.read()

# Fix FmtState accesses
text = text.replace('st->buf', 'st.buf')
text = text.replace('st->size', 'st.size')
text = text.replace('st->pos', 'st.pos')

# Fix str_snprintf signatures
def fix_func(func_name, code):
    pattern = r'pub func:' + func_name + r' = int64\(int64:buf, int64:buf_size, int64:fmt(.*?)\) \{'
    replacement = r'pub func:' + func_name + r' = int64(any->:buf_any, int64:buf_size, any->:fmt_any\1) {\n    int64:buf = @cast_unchecked<int64>(buf_any);\n    int64:fmt = @cast_unchecked<int64>(fmt_any);'
    return re.sub(pattern, replacement, code, flags=re.DOTALL)

text = fix_func('str_snprintf0', text)
text = fix_func('str_snprintf1', text)
text = fix_func('str_snprintf2', text)
text = fix_func('str_snprintf3', text)
text = fix_func('str_snprintf4', text)
text = fix_func('str_snprintf5', text)
text = fix_func('str_snprintf6', text)
text = fix_func('str_snprintf7', text)
text = fix_func('str_snprintf8', text)

# Fix str_format_args signature
pattern = r'pub func:str_format_args = int64\(int64:buf, int64:buf_size, int64:fmt,\s*int64->:args, int64:nargs\) \{'
replacement = r'pub func:str_format_args = int64(any->:buf_any, int64:buf_size, any->:fmt_any, any->:args_any, int64:nargs) {\n    int64:buf = @cast_unchecked<int64>(buf_any);\n    int64:fmt = @cast_unchecked<int64>(fmt_any);\n    int64->:args = @cast_unchecked<int64->>(args_any);'
text = re.sub(pattern, replacement, text, flags=re.DOTALL)

# Fix str_format_args calls to pass pointers instead of ints
text = re.sub(r'str_format_args\(buf, buf_size, fmt, @cast_unchecked<int64->>\(0i64\),', r'str_format_args(buf_any, buf_size, fmt_any, @cast_unchecked<any->>(0i64),', text)
text = re.sub(r'str_format_args\(buf, buf_size, fmt, @cast_unchecked<int64->>\(@a\),', r'str_format_args(buf_any, buf_size, fmt_any, @cast_unchecked<any->>(@a),', text)

# Fix old untyped array arg pass
text = re.sub(r'str_format_args\(buf, buf_size, fmt, 0i64,', r'str_format_args(buf_any, buf_size, fmt_any, @cast_unchecked<any->>(0i64),', text)
text = re.sub(r'str_format_args\(buf, buf_size, fmt, @a,', r'str_format_args(buf_any, buf_size, fmt_any, @cast_unchecked<any->>(@a),', text)

# Fix str_strlen calls
text = text.replace('raw str_strlen(sptr)', 'raw str_strlen(@cast_unchecked<any->>(sptr))')

with open('src/str/strfmt.npk', 'w') as f:
    f.write(text)

