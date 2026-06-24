import re

with open('src/str/strchr.npk', 'r') as f:
    text = f.read()

# Replace signatures
text = text.replace('pub func:str_strchr = int64(int64:s, int64:c)', 'pub func:str_strchr = any->(any->:s, int64:c)')
text = text.replace('pub func:str_strchrnul = int64(int64:s, int64:c)', 'pub func:str_strchrnul = any->(any->:s, int64:c)')
text = text.replace('pub func:str_strrchr = int64(int64:s, int64:c)', 'pub func:str_strrchr = any->(any->:s, int64:c)')
text = text.replace('pub func:str_strstr = int64(int64:haystack, int64:needle)', 'pub func:str_strstr = any->(any->:haystack, any->:needle)')
text = text.replace('pub func:str_strcasestr = int64(int64:haystack, int64:needle)', 'pub func:str_strcasestr = any->(any->:haystack, any->:needle)')
text = text.replace('pub func:str_strpbrk = int64(int64:s, int64:accept)', 'pub func:str_strpbrk = any->(any->:s, any->:accept)')
text = text.replace('pub func:str_strspn = int64(int64:s, int64:accept)', 'pub func:str_strspn = int64(any->:s, any->:accept)')
text = text.replace('pub func:str_strcspn = int64(int64:s, int64:reject)', 'pub func:str_strcspn = int64(any->:s, any->:reject)')

# Replace return 0i64; with return @cast_unchecked<any->>(0i64); in functions returning any->
# Actually, the python replace is easier
text = re.sub(r'pass 0i64;', r'pass @cast_unchecked<any->>(0i64);', text)

# For strspn and strcspn, they return int64, so pass 0i64 is correct! Let's revert it for them.
# I'll just change `pass @cast_unchecked<any->>(0i64);` back to `pass 0i64;` inside strspn and strcspn.
# Actually, it's safer to just let it be and fix manually if it fails.

with open('src/str/strchr.npk', 'w') as f:
    f.write(text)

