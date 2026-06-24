with open('src/str/strlen.npk', 'r') as f:
    text = f.read()

# Fix str_strnlen signature
text = text.replace("pub func:str_strnlen = int64(int64:s, int64:max_len)", "pub func:str_strnlen = int64(any->:s, int64:max_len)")

# Inside str_strnlen
text = text.replace("int64:p = s;", "int64:p = @cast_unchecked<int64>(s);")

# Wait, does it use `s + i`? Yes! Let's check str_strnlen.
# It probably does `while (((p + i) & 7i64) != 0i64)`
# Wait, I already fixed str_strlen, so the variables might be different in str_strnlen.
