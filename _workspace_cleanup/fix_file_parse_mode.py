import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

def repl_parse(m):
    return '''pub func:bio_parse_mode = int64(int64:mode_str) {
    byte->:m = @cast_unchecked<byte->>(mode_str);

    int64:fmode = 0i64;
    int64:oflags = 0i64;

    if (m[0] == 0u8) { pass -1i64; }  // empty string

    byte:first = m[0];
    bool:has_plus = false;
    bool:has_b    = false;
    int64:i = 1i64;

    // Scan for '+' and 'b' modifiers
    while (m[i] != 0u8) {
        if (m[i] == 43u8) { has_plus = true; }   // '+'
        if (m[i] == 98u8) { has_b    = true; }   // 'b'
        i = i + 1i64;
    }

    if (has_b) {
        fmode = fmode | FILE_MODE_BINARY;
    }
    if (has_plus) {
        fmode = fmode | FILE_MODE_UPDATE;
    }

    if (first == 114u8) {  // 'r'
        fmode  = fmode | FILE_MODE_READ;
        if (has_plus) {
            oflags = O_RDWR;
            fmode = fmode | FILE_MODE_WRITE;
        } else {
            oflags = O_RDONLY;
        }
    } else if (first == 119u8) {  // 'w'
        fmode  = fmode | FILE_MODE_WRITE;
        if (has_plus) {
            oflags = O_RDWR | O_CREAT | O_TRUNC;
            fmode = fmode | FILE_MODE_READ;
        } else {
            oflags = O_WRONLY | O_CREAT | O_TRUNC;
        }
    } else if (first == 97u8) {  // 'a'
        fmode  = fmode | FILE_MODE_WRITE | FILE_MODE_APPEND;
        if (has_plus) {
            oflags = O_RDWR | O_CREAT | O_APPEND;
            fmode = fmode | FILE_MODE_READ;
        } else {
            oflags = O_WRONLY | O_CREAT | O_APPEND;
        }
    } else {
        pass -1i64;  // unrecognized mode
    }

    pass (oflags << 32i64) | fmode;
};'''

text = re.sub(r'func:bio_parse_mode = int64\(.*?\).*?^};', repl_parse, text, flags=re.DOTALL|re.MULTILINE)

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

