with open('src/str/strlcpy.npk', 'r') as f:
    text = f.read()

text = text.replace('str_strnlen(dst, dst_size)', 'str_strnlen(dst_any, dst_size)')
text = text.replace('str_strscpy(dst, src, dst_size)', 'str_strscpy(dst_any, src_any, dst_size)')
text = text.replace('str_strlcpy(dst, src, dst_size)', 'str_strlcpy(dst_any, src_any, dst_size)')

with open('src/str/strlcpy.npk', 'w') as f:
    f.write(text)

