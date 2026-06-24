with open('src/str/strconv.npk', 'r') as f:
    text = f.read()

# Fix str_strtol calls inside str_atoi, str_parse_i64, etc.
text = text.replace('str_strtol(s, @cast_unchecked<int64->>(0i64),', 'str_strtol(s_any, @cast_unchecked<any->>(0i64),')
text = text.replace('str_strtoul(s, @cast_unchecked<int64->>(0i64),', 'str_strtoul(s_any, @cast_unchecked<any->>(0i64),')
text = text.replace('str_strlen(min_str)', 'str_strlen(@cast_unchecked<any->>(min_str))')
text = text.replace('str_strlcpy(buf, min_str,', 'str_strlcpy(buf_any, @cast_unchecked<any->>(min_str),')

with open('src/str/strconv.npk', 'w') as f:
    f.write(text)

