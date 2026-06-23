import os

def fix_memset(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Remove volatile
    code = code.replace("volatile p[i]", "p[i]")

    # Fix as uint8
    code = code.replace("pb[i] = (p32 >> ((i & 3i64) * 8i64)) as uint8;", "pb[i] = @cast_unchecked<uint8>((p32 >> ((i & 3i64) * 8i64)));")

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

fix_memset('src/mem/memset.npk')
