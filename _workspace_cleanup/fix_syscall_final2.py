import re
with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

# Fix GETCWD
text = re.sub(r'sys\(GETCWD[^)]*\)', r'sys(GETCWD)', text)
# Fix MADVISE
text = re.sub(r'sys\(MADVISE[^)]*\)', r"sys!!(SYS_MADVISE, addr, length, advice, 0i64, 0i64, 0i64)", text)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)
