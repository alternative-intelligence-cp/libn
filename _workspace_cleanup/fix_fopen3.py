import re

with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

# Fix ternary operators
text = re.sub(r'f\.buf_mode = \(fd == 1i64\) \? _IOLBF : _IOFBF;', '''if (fd == 1i64) {
        f.buf_mode = _IOLBF;
    } else {
        f.buf_mode = _IOFBF;
    }''', text)

text = re.sub(r'f\.buf_mode = \(\(open_flags & O_ACCMODE\) == O_WRONLY \|\| \(open_flags & O_ACCMODE\) == O_RDWR\) \? _IOFBF : _IOLBF;', '''if ((open_flags & O_ACCMODE) == O_WRONLY || (open_flags & O_ACCMODE) == O_RDWR) {
        f.buf_mode = _IOFBF;
    } else {
        f.buf_mode = _IOLBF;
    }''', text)

# Fix as casts
text = re.sub(r'fail ([a-zA-Z0-9_]+) as tbb8;', r'fail @cast_unchecked<tbb8>(\1);', text)
text = re.sub(r'r\.err as int64', r'@cast_unchecked<int64>(r.err)', text)

# Fix duplicated drops
text = text.replace('drop libn_drop libn_errno_set', 'drop libn_errno_set')
text = text.replace('drop drop libn_errno_set', 'drop libn_errno_set')

# Fix missed parentheses
text = text.replace('if buf_owned {', 'if (buf_owned) {')

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

