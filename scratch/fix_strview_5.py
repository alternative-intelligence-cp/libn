import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

replacements = [
    (r'raw str_strlen\(prefix\)', r'raw str_strlen(@cast_unchecked<any->>(prefix))'),
    (r'raw str_strlen\(suffix\)', r'raw str_strlen(@cast_unchecked<any->>(suffix))'),
    (r'raw str_strlen\(needle\)', r'raw str_strlen(@cast_unchecked<any->>(needle))'),
]

for orig, new in replacements:
    text = re.sub(orig, new, text)

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

