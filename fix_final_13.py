with open('src/str/strview.npk', 'r') as f:
    text = f.read()

text = text.replace('*StrViewIter', 'StrViewIter->')
text = text.replace('*StrView', 'StrView->')

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

