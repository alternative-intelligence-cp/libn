import os
import re

filepath = 'src/io/bio/strerror.npk'
with open(filepath, 'r') as f:
    code = f.read()

# Fix msg = strerror(errnum)
code = code.replace(
    'int64:msg = strerror(errnum);',
    'int64:msg = raw strerror(errnum);'
)

# Fix libn_errno_get
code = code.replace(
    'int64:msg = strerror(@cast_unchecked<int64>(libn_errno));',
    'int64:msg = raw strerror(libn_errno_get());'
)

with open(filepath, 'w') as f:
    f.write(code)

