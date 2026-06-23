import os
import re

def fix():
    # 1. strfmt.npk fixes
    path = "/home/randy/Workspace/REPOS/libn/src/str/strfmt.npk"
    with open(path, "r") as f: content = f.read()
    
    # Replace @cast_unchecked<int64->>(a) with @cast_unchecked<int64->>(@a[0])
    content = content.replace("@cast_unchecked<int64->>(a)", "@cast_unchecked<int64->>(@a[0])")
    
    # Add missing str_snprintf5 and str_snprintf7
    if "str_snprintf5" not in content:
        snprintf5 = """
pub func:str_snprintf5 = int64(int64:buf, int64:buf_size, int64:fmt,
                                int64:a0, int64:a1, int64:a2,
                                int64:a3, int64:a4) {
    stack int64[5]:a;
    a[0]=a0; a[1]=a1; a[2]=a2; a[3]=a3; a[4]=a4;
    pass str_format_args(buf, buf_size, fmt, @cast_unchecked<int64->>(@a[0]), 5i64);
};
"""
        content = content.replace("// Six-arg version", snprintf5 + "\n// Six-arg version")

    if "str_snprintf7" not in content:
        snprintf7 = """
pub func:str_snprintf7 = int64(int64:buf, int64:buf_size, int64:fmt,
                                int64:a0, int64:a1, int64:a2, int64:a3,
                                int64:a4, int64:a5, int64:a6) {
    stack int64[7]:a;
    a[0]=a0; a[1]=a1; a[2]=a2; a[3]=a3;
    a[4]=a4; a[5]=a5; a[6]=a6;
    pass str_format_args(buf, buf_size, fmt, @cast_unchecked<int64->>(@a[0]), 7i64);
};
"""
        content = content.replace("// Eight-arg version", snprintf7 + "\n// Eight-arg version")

    with open(path, "w") as f: f.write(content)


    # 2. fprintf.npk fixes
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk"
    with open(path, "r") as f: content = f.read()
    
    # Add memutil import
    if "src/mem/memutil.npk" not in content:
        content = content.replace("use \"src/mem/slab.npk\".*;", "use \"src/mem/slab.npk\".*;\nuse \"src/mem/memutil.npk\".*;")
    
    # Fix len raw unwrapping
    content = content.replace("int64:len = str_snprintf", "int64:len = raw str_snprintf")
    content = content.replace("int64:r = fprintf", "int64:r = raw fprintf")
    content = content.replace("int64:r = printf", "int64:r = raw printf")
    content = content.replace("int64:r = eprintf", "int64:r = raw eprintf")
    
    with open(path, "w") as f: f.write(content)

fix()
