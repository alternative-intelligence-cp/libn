import re
import glob

def fix_dbc(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    # Replace fail ERR_BADARG with !!! 10i32; if it's a null pointer check.
    # We will just replace all fail ERR_BADARG inside the memory core files for null checks
    # e.g. if (dst == 0i64) { fail @cast_unchecked<tbb32>(ERR_BADARG); } -> if (dst == 0i64) { !!! 10i32; }
    
    # We can match `fail @cast_unchecked<tbb32>(ERR_BADARG);`
    content = re.sub(r'fail @cast_unchecked<tbb32>\(ERR_BADARG\);', '!!! 10i32;', content)

    with open(filepath, "w") as f:
        f.write(content)

for file in ["src/mem/memcpy.npk", "src/mem/memset.npk", "src/mem/slab.npk", "src/mem/mmap.npk"]:
    fix_dbc(file)

