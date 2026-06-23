import re

with open('src/str/strfmt.npk', 'r') as f:
    c = f.read()

# Fix literal string pointers
c = c.replace('&"0123456789abcdef"[0] as int64', '@cast_unchecked<int64>(@"0123456789abcdef"[0])')
c = c.replace('&"0123456789ABCDEF"[0] as int64', '@cast_unchecked<int64>(@"0123456789ABCDEF"[0])')
c = c.replace('&"(null)"[0] as int64', '@cast_unchecked<int64>(@"(null)"[0])')

# Fix struct pointer
c = c.replace('*FmtState:stp = &st;', 'FmtState->:stp = @cast_unchecked<FmtState->>(st);')

# Fix array pointers &a[0]
c = re.sub(r'&a\[0\]', r'@cast_unchecked<int64>(a)', c)

with open('src/str/strfmt.npk', 'w') as f:
    f.write(c)

print("Fixed strfmt ampersands.")
