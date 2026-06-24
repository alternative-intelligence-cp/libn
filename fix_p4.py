import re

def fix_memutil():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/memutil.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'offset = offset + bad_char[@cast_unchecked<int64>(h[offset + nlen - 1i64])];',
        'offset = offset + @cast_unchecked<int64>(bad_char[@cast_unchecked<int64>(h[offset + nlen - 1i64])]);'
    )
    
    with open(path, 'w') as f:
        f.write(content)

def fix_stdfiles():
    path = '/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'sout->buf_mode = is (isatty(1i64) != 0i64) : _IOLBF : _IOFBF;',
        'sout->buf_mode = is (raw isatty(1i64) != 0i64) : _IOLBF : _IOFBF;'
    )
    content = content.replace(
        'sout->buf_mode = is (isatty(2i64) != 0i64)',
        'sout->buf_mode = is (raw isatty(2i64) != 0i64)'
    )
    
    with open(path, 'w') as f:
        f.write(content)

fix_memutil()
fix_stdfiles()
