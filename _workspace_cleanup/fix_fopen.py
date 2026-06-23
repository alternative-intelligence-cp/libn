import re

with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

# Replace all old casting syntax with @cast_unchecked
text = text.replace('fp as *FILE', '@cast_unchecked<FILE->>(fp)')
text = text.replace('f.buf as *byte', '@cast_unchecked<uint8->>(f.buf)')

# Replace errno_set with drop libn_errno_set
text = text.replace('errno_set', 'drop libn_errno_set')
text = text.replace('drop drop', 'drop')

# Replace bio_parse_mode
def repl_parse(m):
    return '''    int64:parse_res = raw bio_parse_mode(mode);
    if parse_res < 0i64 {
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:file_mode = parse_res & 0xFFFFFFFFi64;
    int64:open_flags = parse_res >> 32i64;'''

text = re.sub(r'    stack int64:file_mode_out\[1\];\n    stack int64:open_flags_out\[1\];\n    int64:parse_ok = bio_parse_mode\(mode, &file_mode_out\[0\] as int64, &open_flags_out\[0\] as int64\);\n    if parse_ok != 0i64 \{\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \}', repl_parse, text)

def repl_parse2(m):
    return '''    int64:parse_res = raw bio_parse_mode(mode);
    if parse_res < 0i64 {
        drop fclose(fp);
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:file_mode = parse_res & 0xFFFFFFFFi64;
    int64:open_flags = parse_res >> 32i64;'''

text = re.sub(r'    stack int64:file_mode_out\[1\];\n    stack int64:open_flags_out\[1\];\n    int64:parse_ok = bio_parse_mode\(mode, &file_mode_out\[0\] as int64, &open_flags_out\[0\] as int64\);\n    if parse_ok != 0i64 \{\n        fclose\(fp\);\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \}', repl_parse2, text)

# Remove unused variable extractions
text = text.replace('int64:file_mode  = file_mode_out[0];\n    int64:open_flags = open_flags_out[0];\n', '\n')

# Fix bio_alloc_file and bio_free_file
text = text.replace('int64:fp = bio_alloc_file();', 'int64:fp = raw bio_alloc_file();')
text = text.replace('bio_free_file(fp);', 'drop bio_free_file(fp);')
text = text.replace('bio_flush_write_buf(fp);', 'drop bio_flush_write_buf(fp);')
text = text.replace('bio_free_buf(f.buf, f.buf_size);', 'drop bio_free_buf(f.buf, f.buf_size);')
text = text.replace('fclose(fp);', 'drop fclose(fp);')

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

