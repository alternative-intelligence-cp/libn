import os
import re

src_dir = "src"

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    orig = content

    # 1. Replace pointer member access (.) with (->) for known pointer variables.
    # This is tricky because we don't have a semantic parser.
    # But we know common ones: s.ptr, s.len, r.is_error, r.value, r.err, sa.len, sb.len, etc.
    # Actually, r is Result<int64> (struct), not a pointer, so r.is_error is correct!
    # "got '*StrView'. Use -> for pointer member access."
    # So StrView pointers: sv, s, p, o, n, x, a, b, sa, sb, lo, ro, to, cur, tok, left, right, it, tmp
    # Let's just blindly replace `.ptr` with `->ptr` and `.len` with `->len` if preceded by a letter/variable,
    # UNLESS it's a known non-pointer struct. Are there any StrView structs that are by-value?
    # `stack StrView:tmp;` creates an object! `tmp.len` is correct.
    # But wait, `test_all.npk` error on `line 509` (which is in strview.npk line 509):
    # `lo.ptr = s.ptr;` Here `lo` and `s` are pointers!
    # I can use regex to replace `([a-zA-Z_0-9]+)\.(ptr|len|code|msg)` -> `\1->\2`
    # EXCEPT for stack variables: tmp, left, right, bv, cur, tok, line, etc.
    
    # 2. "void return type only allowed in extern blocks."
    # func:foo = void(...) { -> func:foo = NIL(...) {
    content = re.sub(r'=\s*void\s*\(', r'= NIL(', content)

    # 3. "Cannot silently unwrap Result<...>"
    # "Declare as Result<int64> and check .is_error"
    
    if content != orig:
        with open(path, 'w') as f:
            f.write(content)

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
