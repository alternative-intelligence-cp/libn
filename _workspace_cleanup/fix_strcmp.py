import os
import re

filepath = 'src/str/strcmp.npk'
with open(filepath, 'r') as f:
    code = f.read()

code = code.replace(
    'while (((a + i) | (b + i)) & 7i64 != 0i64) {',
    'while ((((a + i) | (b + i)) & 7i64) != 0i64) {'
)

# And fix line 86: if (a[i] != b[i]) { -> if ((@cast_unchecked<uint8->>(a))[i] != (@cast_unchecked<uint8->>(b))[i]) {
code = code.replace(
    'if (a[i] != b[i]) {',
    'if ((@cast_unchecked<uint8->>(a))[i] != (@cast_unchecked<uint8->>(b))[i]) {'
)

# What about line 91: pass @cast_unchecked<int64>(a[i]) - @cast_unchecked<int64>(b[i]);
code = code.replace(
    'pass @cast_unchecked<int64>(a[i]) - @cast_unchecked<int64>(b[i]);',
    'pass @cast_unchecked<int64>((@cast_unchecked<uint8->>(a))[i]) - @cast_unchecked<int64>((@cast_unchecked<uint8->>(b))[i]);'
)

with open(filepath, 'w') as f:
    f.write(code)

