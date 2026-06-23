import re

def fix_file(path):
    with open(path, 'r') as f:
        text = f.read()

    # Make functions public
    text = text.replace('\nfunc:bio_alloc_file', '\npub func:bio_alloc_file')
    text = text.replace('\nfunc:bio_free_file', '\npub func:bio_free_file')
    text = text.replace('\nfunc:bio_alloc_buf', '\npub func:bio_alloc_buf')
    text = text.replace('\nfunc:bio_free_buf', '\npub func:bio_free_buf')
    text = text.replace('\nfunc:bio_flush_write_buf', '\npub func:bio_flush_write_buf')

    # Remove fail cast
    text = re.sub(r'fail @cast_unchecked<tbb8>\(([A-Za-z0-9_]+)\);', r'fail \1;', text)

    # In file.npk, bio_parse_mode: change byte-> back to uint8->
    if 'file.npk' in path:
        text = text.replace('byte->:m = @cast_unchecked<byte->>(mode_str);', 'uint8->:m = @cast_unchecked<uint8->>(mode_str);')
        text = text.replace('byte:first = m[0];', 'uint8:first = m[0];')
        # Also fix line 365 uint8/byte mismatch:
        # Wait, I don't know what line 365 is! Let's check it below.

    with open(path, 'w') as f:
        f.write(text)

fix_file('src/io/bio/file.npk')
fix_file('src/io/bio/fopen.npk')

