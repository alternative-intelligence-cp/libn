import os

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

text = text.replace('*StrBuf', 'StrBuf->')
text = text.replace('@left => int64', '@cast_unchecked<int64>(@left)')
text = text.replace('@right => int64', '@cast_unchecked<int64>(@right)')
text = text.replace('@tmp => int64', '@cast_unchecked<int64>(@tmp)')
text = text.replace('@bv => int64', '@cast_unchecked<int64>(@bv)')

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

