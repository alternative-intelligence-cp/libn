import os

replacements = {
    "int64:old_ptr = old_buf != 0i64 ? @cast_unchecked<int64>(@cast_unchecked<int64->>(&old_act[0])) : 0i64;": "int64:old_ptr = 0i64;\n    if (old_buf != 0i64) { old_ptr = @cast_unchecked<int64>(@cast_unchecked<int64->>(&old_act[0])); }",
    "int64:old_p = old_ptr != 0i64 ? &old_val : 0i64;": "int64:old_p = 0i64;\n    if (old_ptr != 0i64) { old_p = &old_val; }",
    "int64:tid = pid_r.is_error ? 1i64 : pid_r.value;": "int64:tid = pid_r.value;\n    if (pid_r.is_error) { tid = 1i64; }",
    "int64:to_copy = buffered < remaining ? buffered : remaining;": "int64:to_copy = remaining;\n            if (buffered < remaining) { to_copy = buffered; }",
    "int64:to_copy = buf_space < remaining ? buf_space : remaining;": "int64:to_copy = remaining;\n        if (buf_space < remaining) { to_copy = buf_space; }",
    "int64:pid = pid_r.is_error ? 1i64 : pid_r.value;": "int64:pid = pid_r.value;\n    if (pid_r.is_error) { pid = 1i64; }",
    "int64:dst = buf != 0i64 ? buf : @cast_unchecked<int64>(@g_tmpnam_buf[0]);": "int64:dst = @cast_unchecked<int64>(@g_tmpnam_buf[0]);\n    if (buf != 0i64) { dst = buf; }",
    "int64:max = width > 0i64 ? width : 0x7FFFFFFFFFFFFFFFi64;": "int64:max = 0x7FFFFFFFFFFFFFFFi64;\n    if (width > 0i64) { max = width; }",
    "base = (spec == 105u8) ? 0i64 : 10i64;": "if (spec == 105u8) { base = 0i64; } else { base = 10i64; }",
    "int64:cap = size > 0i64 ? size : BUFSIZ;": "int64:cap = BUFSIZ;\n        if (size > 0i64) { cap = size; }",
    "f.buf_mode = (fd == 1i64) ? _IOLBF : _IOFBF;": "if (fd == 1i64) { f.buf_mode = _IOLBF; } else { f.buf_mode = _IOFBF; }",
    "oflags[0] = has_plus ? O_RDWR : O_RDONLY;": "if (has_plus) { oflags[0] = O_RDWR; } else { oflags[0] = O_RDONLY; }",
    "sv.len = len < 0i64 ? 0i64 : len;": "sv.len = len;\n    if (len < 0i64) { sv.len = 0i64; }",
    "int64:min_len = sa.len < sb.len ? sa.len : sb.len;": "int64:min_len = sb.len;\n    if (sa.len < sb.len) { min_len = sa.len; }",
    "int64:plen = prefix != 0i64 ? str_strlen(prefix) : 0i64;": "int64:plen = 0i64;\n        if (prefix != 0i64) { plen = str_strlen(prefix); }",
    "int64:xlen = suffix != 0i64 ? str_strlen(suffix) : 0i64;": "int64:xlen = 0i64;\n        if (suffix != 0i64) { xlen = str_strlen(suffix); }",
    "int64:n = s.len < buflen ? s.len : buflen;": "int64:n = buflen;\n    if (s.len < buflen) { n = s.len; }",
    "int64:n = s.len < max ? s.len : max;": "int64:n = max;\n    if (s.len < max) { n = s.len; }",
    "byte->:digits = @cast_unchecked<uint8->>(upper ? DIGITS_UPPER : DIGITS_LOWER);": "byte->:digits = @cast_unchecked<uint8->>(DIGITS_LOWER);\n    if (upper) { digits = @cast_unchecked<uint8->>(DIGITS_UPPER); }",
    "prefix[prefix_len + 1i64] = is_upper ? 88u8 : 120u8;": "if (is_upper) { prefix[prefix_len + 1i64] = 88u8; } else { prefix[prefix_len + 1i64] = 120u8; }",
    "int64:new_cap = s.cap > 0i64 ? s.cap : STRBUF_MIN_CAP;": "int64:new_cap = STRBUF_MIN_CAP;\n    if (s.cap > 0i64) { new_cap = s.cap; }",
    "int64:cap = init_cap > STRBUF_MIN_CAP ? init_cap : STRBUF_MIN_CAP;": "int64:cap = STRBUF_MIN_CAP;\n    if (init_cap > STRBUF_MIN_CAP) { cap = init_cap; }",
    "pass a == INT64_MIN ? 0i64 : INT64_MAX;": "if (a == INT64_MIN) { pass 0i64; } else { pass INT64_MAX; }"
}

import re

def replace_ternaries(path):
    with open(path, 'r') as f:
        code = f.read()
    orig = code
    for k, v in replacements.items():
        if k in code:
            code = code.replace(k, v)

    # Regex for multi-line ternary in strfmt.npk
    code = re.sub(
        r'byte->:digits\s*=\s*@cast_unchecked<uint8->>\(\s*upper\s*\?\s*DIGITS_UPPER\s*:\s*DIGITS_LOWER\s*\);',
        r'byte->:digits = @cast_unchecked<uint8->>(DIGITS_LOWER);\n    if (upper) { digits = @cast_unchecked<uint8->>(DIGITS_UPPER); }',
        code
    )

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed ternaries in {path}")

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            replace_ternaries(os.path.join(root, f))
