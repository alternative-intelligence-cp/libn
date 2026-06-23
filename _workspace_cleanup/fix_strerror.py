import re

with open('src/io/bio/strerror.npk', 'r') as f:
    text = f.read()

# Replace `"..." as int64` with `@cast_unchecked<int64>(@"...")`
text = re.sub(r'"([^"]*)"\s+as\s+int64', r'@cast_unchecked<int64>(@"\1")', text)

with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(text)
