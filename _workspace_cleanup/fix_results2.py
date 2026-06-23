import os
import re

def rewrite(filepath, callback):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    new_content = callback(content)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

def fix_strview(c):
    # mem_malloc calls
    c = re.sub(r'Result<int64>:alloc_r = mem_malloc\((.*?)\);\n\s*if \(alloc_r\.is_error\) \{ fail @cast_unchecked<tbb8>\(ENOMEM\); \}\n\s*int64:buf = alloc_r\.value;', r'int64:buf = mem_malloc(\1);\n        if (buf == 0i64) { fail @cast_unchecked<tbb8>(ENOMEM); }', c)
    c = re.sub(r'Result<int64>:r = mem_malloc\((.*?)\);\n\s*if \(r\.is_error\) \{ pass 0i64; \}\n\s*if \(s\.len > 0i64\) \{\n\s*drop\(mem_memcpy\(r\.value, s\.ptr, s\.len\)\);\n\s*\}\n\s*\(@cast_unchecked<uint8->>\(r\.value\)\)\[s\.len\] = 0u8;\n\s*pass r\.value;', r'int64:r_ptr = mem_malloc(\1);\n    if (r_ptr == 0i64) { pass 0i64; }\n    if (s.len > 0i64) {\n        drop(mem_memcpy(r_ptr, s.ptr, s.len));\n    }\n    (@cast_unchecked<uint8->>(r_ptr))[s.len] = 0u8;\n    pass r_ptr;', c)

    # str_parse_i64 / u64 calls
    c = c.replace('Result<int64>:r = str_parse_i64(buf);', 'int64:r = str_parse_i64(buf);')
    c = c.replace('Result<int64>:r = str_parse_u64(buf);', 'int64:r = str_parse_u64(buf);')
    return c
rewrite('src/str/strview.npk', fix_strview)

def fix_memcpy(c):
    # mem_malloc call
    c = re.sub(r'Result<int64>:r = mem_malloc\(n\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*Result<int64>:rc = mem_memcpy\(r\.value, src, n\);\n\s*if \(rc\.is_error\) \{\n\s*drop\(mem_free\(r\.value\)\);\n\s*fail rc\.error;\n\s*\}\n\s*pass r\.value;', r'int64:r_ptr = mem_malloc(n);\n    if (r_ptr == 0i64) { fail @cast_unchecked<tbb8>(12i64); }\n    Result<int64>:rc = mem_memcpy(r_ptr, src, n);\n    if (rc.is_error) {\n        drop(mem_free(r_ptr));\n        fail rc.error;\n    }\n    pass r_ptr;', c)
    return c
rewrite('src/mem/memcpy.npk', fix_memcpy)

def fix_strbuf(c):
    c = re.sub(r'Result<int64>:r = mem_realloc\(s\.ptr, new_cap\);\n\s*if \(r\.is_error\) \{ fail r\.error; \}\n\s*s\.ptr = r\.value;', r's.ptr = mem_realloc(s.ptr, new_cap);', c)
    
    c = re.sub(r'Result<int64>:sr = mem_malloc\(24i64\);\n\s*if \(sr\.is_error\) \{ pass 0i64; \}\n\s*StrBuf->:s = @cast_unchecked<StrBuf->>\(sr\.value\);\n\n\s*Result<int64>:br = mem_malloc\(cap\);\n\s*if \(br\.is_error\) \{\n\s*drop\(mem_free\(sr\.value\)\);\n\s*pass 0i64;\n\s*\}\n\s*s\.ptr = br\.value;', r'int64:sr_ptr = mem_malloc(24i64);\n    if (sr_ptr == 0i64) { pass 0i64; }\n    StrBuf->:s = @cast_unchecked<StrBuf->>(sr_ptr);\n\n    int64:br_ptr = mem_malloc(cap);\n    if (br_ptr == 0i64) {\n        drop(mem_free(sr_ptr));\n        pass 0i64;\n    }\n    s.ptr = br_ptr;', c)
    
    c = re.sub(r'Result<int64>:r = mem_malloc\(n \+ 1i64\);\n\s*if \(r\.is_error\) \{ pass 0i64; \}\n\s*int64:buf = r\.value;', r'int64:buf = mem_malloc(n + 1i64);\n    if (buf == 0i64) { pass 0i64; }', c)
    return c
rewrite('src/str/strbuf.npk', fix_strbuf)

def fix_fprintf(c):
    c = c.replace('int64:p = raw(mem_malloc(len + 1i64));', 'int64:p = mem_malloc(len + 1i64);')
    return c
rewrite('src/io/bio/fprintf.npk', fix_fprintf)
