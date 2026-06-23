with open('src/str/strchr.npk', 'r') as f:
    text = f.read()

text = text.replace('int64->', 'int64@')
text = text.replace('uint8->', 'uint8@')
text = text.replace('int64@ >', 'int64@')
text = text.replace('uint8@ >', 'uint8@')
text = text.replace('int64@>', 'int64@')
text = text.replace('uint8@>', 'uint8@')

with open('src/str/strchr.npk', 'w') as f:
    f.write(text)
