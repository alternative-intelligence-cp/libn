import re

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/tmpfile.npk'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('pub fixed int64:TMP_DIR = @"/tmp/";', 'pub fixed int64:TMP_DIR = @cast_unchecked<int64>(@"/tmp/");')
content = content.replace('pub fixed int64:TMP_PREFIX = @"npk_";', 'pub fixed int64:TMP_PREFIX = @cast_unchecked<int64>(@"npk_");')
content = content.replace('fixed int64:pfx = @"/tmp/npk_XXXXXX";', 'fixed int64:pfx = @cast_unchecked<int64>(@"/tmp/npk_XXXXXX");')
content = content.replace('fixed int64:pfx = @"/tmp/npk_";', 'fixed int64:pfx = @cast_unchecked<int64>(@"/tmp/npk_");')

with open(path, 'w') as f:
    f.write(content)

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/strerror.npk'
with open(path, 'r') as f:
    content = f.read()
content = content.replace('fixed int64:prefix = @"Unknown error ";', 'fixed int64:prefix = @cast_unchecked<int64>(@"Unknown error ");')
with open(path, 'w') as f:
    f.write(content)

print("Fixed strings")
