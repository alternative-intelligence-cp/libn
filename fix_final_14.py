import os, glob

# Fix strbuf.npk
with open('src/str/strbuf.npk', 'r') as f:
    text = f.read()
text = text.replace('*StrBuf', 'StrBuf->')
text = text.replace('.val', '.value')
with open('src/str/strbuf.npk', 'w') as f:
    f.write(text)

# Fix strview.npk
with open('src/str/strview.npk', 'r') as f:
    text = f.read()
text = text.replace('@@cast_unchecked<int64>(left)', '@left => int64')
text = text.replace('@@cast_unchecked<int64>(right)', '@right => int64')
text = text.replace('@@cast_unchecked<int64>(tmp)', '@tmp => int64')
text = text.replace('@@cast_unchecked<int64>(bv)', '@bv => int64')
text = text.replace('.val', '.value')
# In strview: Cannot cast 'uint8@' to 'int64'
# @tmp[0] => int64 is correct, wait, what was line 621?
# It was `@tmp[0] => int64` but parsed as `uint8@` to `int64`? In v0.12, maybe `int64(@tmp[0])`? No, `@cast_unchecked<int64>(@tmp[0])` or something?
# Let's just fix .value and left/right first.
with open('src/str/strview.npk', 'w') as f:
    f.write(text)

# Fix Result.value in all files
for file in glob.glob('src/**/*.npk', recursive=True):
    if file not in ['src/str/strbuf.npk', 'src/str/strview.npk']:
        with open(file, 'r') as f:
            text = f.read()
        if '.val' in text:
            text = text.replace('.val', '.value')
            with open(file, 'w') as f:
                f.write(text)

