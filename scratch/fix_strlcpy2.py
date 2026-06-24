with open('src/str/strlcpy.npk', 'r') as f:
    text = f.read()

text = text.replace('str_strlen(src)', 'str_strlen(src_any)')
text = text.replace('str_strlen(dst)', 'str_strlen(dst_any)')
text = text.replace('mem_memcpy(dst, src,', 'mem_memcpy(dst_any, src_any,')
text = text.replace('mem_memcpy(d, s,', 'mem_memcpy(@cast_unchecked<any->>(d), @cast_unchecked<any->>(s),')
text = text.replace('mem_memcpy(dst + dst_len, src,', 'mem_memcpy(@cast_unchecked<any->>(dst + dst_len), src_any,')

with open('src/str/strlcpy.npk', 'w') as f:
    f.write(text)
