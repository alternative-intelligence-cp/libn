import re
with open('src/io/bio/fprintf.npk', 'r') as f:
    text = f.read()

# For fprintf0..8
pattern_fprintf = r'int64:len = (str_snprintf\d\([^)]+\));'
replacement_fprintf = r'''Result<int64>:len_res = \1;
    if (len_res.is_error) { pass -1i64; }
    int64:len = len_res.value;'''
text = re.sub(pattern_fprintf, replacement_fprintf, text)

with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(text)
