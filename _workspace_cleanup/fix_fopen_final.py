import re

with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

def repl_parse_fclose(m):
    return '''    int64:parse_res = raw bio_parse_mode(mode);
    if (parse_res < 0i64) {
        drop fclose(fp);
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:open_flags = parse_res >> 32i64;
    int64:file_mode = parse_res & 0xFFFFFFFFi64;'''

text = re.sub(r'    stack int64:file_mode_out\[1\];\n    stack int64:open_flags_out\[1\];\n    int64:parse_ok = bio_parse_mode\(mode, &file_mode_out\[0\] as int64, &open_flags_out\[0\] as int64\);\n    if \(parse_ok != 0i64\)\{\n        drop fclose\(fp\);\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \}', repl_parse_fclose, text)

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

