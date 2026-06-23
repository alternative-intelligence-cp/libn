import re

with open('src/mem/memutil.npk', 'r') as f:
    text = f.read()

# Replace `(expr) as *int64` with `@cast_unchecked<int64->>(expr)`
text = re.sub(r'\(([^)]+)\)\s+as\s+\*int64', r'@cast_unchecked<int64->>(\1)', text)

# Replace `pa[i] as int64` with `@cast_unchecked<int64>(pa[i])`
text = re.sub(r'pa\[i\]\s+as\s+int64', r'@cast_unchecked<int64>(pa[i])', text)
text = re.sub(r'pb\[i\]\s+as\s+int64', r'@cast_unchecked<int64>(pb[i])', text)

# Replace `c as uint8` with `@cast_unchecked<uint8>(c)`
text = re.sub(r'c\s+as\s+uint8', r'@cast_unchecked<uint8>(c)', text)

# Replace `first as int64` with `@cast_unchecked<int64>(first)`
text = re.sub(r'first\s+as\s+int64', r'@cast_unchecked<int64>(first)', text)

with open('src/mem/memutil.npk', 'w') as f:
    f.write(text)
