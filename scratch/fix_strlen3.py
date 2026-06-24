with open('src/str/strlen.npk', 'r') as f:
    text = f.read()

# Fix str_strnlen
text = text.replace("pub func:str_strnlen = int64(int64:s, int64:max_len)", "pub func:str_strnlen = int64(any->:s, int64:max_len)")
text = text.replace("if (s == 0i64", "if (s == @cast_unchecked<any->>(0i64)")
text = text.replace("((s + i) & 7i64)", "((@cast_unchecked<int64>(s) + i) & 7i64)")
text = text.replace("((s + i));", "((@cast_unchecked<int64>(s) + i));")

# Fix str_strlen_safe
text = text.replace("pub func:str_strlen_safe = int64(int64:s, int64:max_len)", "pub func:str_strlen_safe = int64(any->:s, int64:max_len)")

with open('src/str/strlen.npk', 'w') as f:
    f.write(text)
