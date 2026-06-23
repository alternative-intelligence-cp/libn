import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()
    
# Fix the double closing parenthesis
text = re.sub(r'func:bio_refill_read_buf = int64\(int64:fp\)\)', r'func:bio_refill_read_buf = int64(int64:fp) {', text)

# Fix ternary operators
text = text.replace('oflags[0] = has_plus ? O_RDWR : O_RDONLY;', 'if (has_plus) { oflags[0] = O_RDWR; } else { oflags[0] = O_RDONLY; }')
text = text.replace('oflags[0] = has_plus ? (O_RDWR | O_CREAT | O_TRUNC) : (O_WRONLY | O_CREAT | O_TRUNC);', 'if (has_plus) { oflags[0] = O_RDWR | O_CREAT | O_TRUNC; } else { oflags[0] = O_WRONLY | O_CREAT | O_TRUNC; }')
text = text.replace('oflags[0] = has_plus ? (O_RDWR | O_CREAT | O_APPEND) : (O_WRONLY | O_CREAT | O_APPEND);', 'if (has_plus) { oflags[0] = O_RDWR | O_CREAT | O_APPEND; } else { oflags[0] = O_WRONLY | O_CREAT | O_APPEND; }')
text = text.replace('oflags[0] = has_plus ? O_RDWR | O_CREAT | O_TRUNC : O_WRONLY | O_CREAT | O_TRUNC;', 'if (has_plus) { oflags[0] = O_RDWR | O_CREAT | O_TRUNC; } else { oflags[0] = O_WRONLY | O_CREAT | O_TRUNC; }')
text = text.replace('oflags[0] = has_plus ? O_RDWR | O_CREAT | O_APPEND : O_WRONLY | O_CREAT | O_APPEND;', 'if (has_plus) { oflags[0] = O_RDWR | O_CREAT | O_APPEND; } else { oflags[0] = O_WRONLY | O_CREAT | O_APPEND; }')

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)
