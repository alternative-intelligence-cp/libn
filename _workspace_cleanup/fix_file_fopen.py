import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

# Add pub to internal functions that fopen uses
text = text.replace('func:bio_alloc_file', 'pub func:bio_alloc_file')
text = text.replace('func:bio_free_file', 'pub func:bio_free_file')
text = text.replace('func:bio_alloc_buf', 'pub func:bio_alloc_buf')
text = text.replace('func:bio_free_buf', 'pub func:bio_free_buf')
text = text.replace('func:bio_flush_write_buf', 'pub func:bio_flush_write_buf')
text = text.replace('func:bio_parse_mode', 'pub func:bio_parse_mode')

# Change void to NIL for Nitpick
text = text.replace('void(int64:fp)', 'NIL(int64:fp)')
text = text.replace('void(int64:buf, int64:size)', 'NIL(int64:buf, int64:size)')

# Fix byte->uint8 cast inside bio_parse_mode
text = text.replace('byte:first = m[0];', 'uint8:first = m[0];')

# Rewrite bio_parse_mode correctly
def repl_parse_mode(m):
    body = m.group(1)
    body = body.replace('fmode[0]  = 0i64;', 'int64:fmode_val = 0i64;')
    body = body.replace('oflags[0] = 0i64;', 'int64:oflags_val = 0i64;')
    body = body.replace('fmode[0]', 'fmode_val')
    body = body.replace('oflags[0]', 'oflags_val')
    # find the end of the function and replace pass 0i64 with pass combined
    body = body.replace('pass 0i64;\n};', 'pass (oflags_val << 32i64) | fmode_val;\n};')
    return 'pub func:bio_parse_mode = int64(int64:mode_str) {\n' + body

text = re.sub(r'pub func:bio_parse_mode = int64\(int64:mode_str, int64->:fmode, int64->:oflags\) \{\n(.*?pass 0i64;\n\};)', repl_parse_mode, text, flags=re.DOTALL)

# Fix Result wrapper issue on slab_alloc_zero
text = text.replace('int64:p = slab_alloc_zero', 'int64:p = raw slab_alloc_zero')

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)


with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

# Fix errno_set to drop libn_errno_set
text = text.replace('errno_set', 'drop libn_errno_set')
text = text.replace('drop drop', 'drop')

# Fix bio_parse_mode calls
def repl_call(m):
    return '''    int64:parse_res = raw bio_parse_mode(mode);
    if (parse_res < 0i64) {
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:open_flags = parse_res >> 32i64;
    int64:file_mode = parse_res & 0xFFFFFFFFi64;'''

text = re.sub(r'    int64\[1\]:file_mode_out;\n    int64\[1\]:open_flags_out;\n    int64:parse_ok = bio_parse_mode\(mode, file_mode_out, open_flags_out\);\n    if \(parse_ok != 0i64\) \{\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \}\n\n    int64:file_mode  = file_mode_out\[0\];\n    int64:open_flags = open_flags_out\[0\];', repl_call, text)

# bio_alloc_file uses raw
text = text.replace('int64:fp = bio_alloc_file();', 'int64:fp = raw bio_alloc_file();')
# bio_free_file and others shouldn't need raw because they return NIL, but they MUST be wrapped in drop!
text = text.replace('bio_free_file(fp);', 'drop bio_free_file(fp);')
text = text.replace('bio_flush_write_buf(fp);', 'drop bio_flush_write_buf(fp);')
text = text.replace('bio_free_buf(f.buf, f.buf_size);', 'drop bio_free_buf(f.buf, f.buf_size);')

# Fix unused result from fclose
text = text.replace('fclose(fp);', 'drop fclose(fp);')

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

