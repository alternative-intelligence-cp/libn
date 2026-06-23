import os, glob

# Fix strfmt.npk missing semicolons
with open('src/str/strfmt.npk', 'r') as f:
    text = f.read()
text = text.replace('5i64));\n}\n', '5i64));\n};\n')
text = text.replace('7i64));\n}\n', '7i64));\n};\n')
with open('src/str/strfmt.npk', 'w') as f:
    f.write(text)

# Fix test_all.npk pass
with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('    pass;\n', '    exit 0i64;\n')
with open('test_all.npk', 'w') as f:
    f.write(text)

