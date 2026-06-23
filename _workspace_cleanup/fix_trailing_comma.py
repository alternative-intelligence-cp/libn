import os

filepath = 'src/io/bio/strerror.npk'
with open(filepath, 'r') as f:
    code = f.read()

# Replace trailing comma
code = code.replace('{ -1i64,  0i64 },   // sentinel\n];', '{ -1i64,  0i64 }   // sentinel\n];')

with open(filepath, 'w') as f:
    f.write(code)
