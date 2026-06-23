import re

def fix_file(path):
    with open(path, 'r') as f:
        text = f.read()

    # 1. Struct syntax
    text = text.replace('pub struct FILE {', 'pub struct:FILE = {')
    
    # 2. Add semicolons to top-level closing braces
    text = re.sub(r'^}$', '};', text, flags=re.MULTILINE)
    
    # 3. Add parens to if/while without them
    def add_parens(t):
        lines = t.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            m = re.match(r'^(\s*(?:if|while|else if)\s*)([^{]+)(\s*\{\s*)$', line)
            if m:
                cond = m.group(2).strip()
                if not (cond.startswith('(') and cond.endswith(')')):
                    lines[i] = f"{m.group(1)}({cond}){m.group(3)}"
            m2 = re.match(r'^(\s*\}\s*else if\s*)([^{]+)(\s*\{\s*)$', line)
            if m2:
                cond = m2.group(2).strip()
                if not (cond.startswith('(') and cond.endswith(')')):
                    lines[i] = f"{m2.group(1)}({cond}){m2.group(3)}"
        return '\n'.join(lines)
    text = add_parens(text)

    # 4. Void to NIL
    if 'file.npk' in path:
        text = text.replace('void(int64:fp)', 'NIL(int64:fp)')
        text = text.replace('void(int64:buf, int64:size)', 'NIL(int64:buf, int64:size)')
        text = text.replace('pub func:bio_parse_mode = int64(int64:mode_str, int64->:fmode, int64->:oflags) {', 'pub func:bio_parse_mode = int64(int64:mode_str) {')

    # 5. Fix type casting
    text = text.replace('fp as *FILE', '@cast_unchecked<FILE->>(fp)')
    text = text.replace('f.buf as *byte', '@cast_unchecked<uint8->>(f.buf)')
    text = text.replace('p as *FILE', '@cast_unchecked<FILE->>(p)')
    text = text.replace('m as *byte', '@cast_unchecked<uint8->>(m)')
    text = re.sub(r'r\.err as int64', r'@cast_unchecked<int64>(r.error)', text)
    text = re.sub(r'fail ([a-zA-Z0-9_]+) as tbb8;', r'fail @cast_unchecked<tbb8>(\1);', text)

    # 6. Result Unwrapping / Drops
    text = text.replace('errno_set', 'drop libn_errno_set')
    text = text.replace('drop drop ', 'drop ')
    if 'fopen.npk' in path:
        text = text.replace('int64:fp = bio_alloc_file();', 'int64:fp = raw bio_alloc_file();')
        text = text.replace('bio_free_file(fp);', 'drop bio_free_file(fp);')
        text = text.replace('bio_flush_write_buf(fp);', 'drop bio_flush_write_buf(fp);')
        text = text.replace('bio_free_buf(f.buf, f.buf_size);', 'drop bio_free_buf(f.buf, f.buf_size);')
        text = text.replace('fclose(fp);', 'drop fclose(fp);')

    # 7. bio_parse_mode fix for file.npk
    if 'file.npk' in path:
        def repl_parse(m):
            return '''    int64:fmode = 0i64;
    int64:oflags = 0i64;

    if (m[0] == 0u8) { pass -1i64; }  // empty string

    uint8:first = m[0];
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

    pass (oflags << 32i64) | fmode;'''
        text = re.sub(r'    fmode\[0\] = 0i64;.*?pass 0i64;', repl_parse, text, flags=re.DOTALL)

    # 8. bio_parse_mode fix for fopen.npk
    if 'fopen.npk' in path:
        def repl_parse_fopen(m):
            return '''    int64:parse_res = raw bio_parse_mode(mode);
    if (parse_res < 0i64) {
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:open_flags = parse_res >> 32i64;
    int64:file_mode = parse_res & 0xFFFFFFFFi64;'''
        text = re.sub(r'    stack int64:file_mode_out\[1\];.*?if \(parse_ok != 0i64\) \{\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \};?', repl_parse_fopen, text, flags=re.DOTALL)
        text = re.sub(r'    stack int64:file_mode_out\[1\];.*?if parse_ok != 0i64 \{\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \};?', repl_parse_fopen, text, flags=re.DOTALL)
        
        def repl_parse2_fopen(m):
            return '''    int64:parse_res = raw bio_parse_mode(mode);
    if (parse_res < 0i64) {
        drop fclose(fp);
        drop libn_errno_set(EINVAL);
        pass 0i64;
    }
    int64:open_flags = parse_res >> 32i64;
    int64:file_mode = parse_res & 0xFFFFFFFFi64;'''
        text = re.sub(r'    stack int64:file_mode_out\[1\];.*?if \(parse_ok != 0i64\) \{\n        fclose\(fp\);\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \};?', repl_parse2_fopen, text, flags=re.DOTALL)
        text = re.sub(r'    stack int64:file_mode_out\[1\];.*?if parse_ok != 0i64 \{\n        fclose\(fp\);\n        drop libn_errno_set\(EINVAL\);\n        pass 0i64;\n    \};?', repl_parse2_fopen, text, flags=re.DOTALL)
        
        text = text.replace('int64:file_mode  = file_mode_out[0];\n    int64:open_flags = open_flags_out[0];\n', '')
        text = text.replace('int64:file_mode = file_mode_out[0];\n    int64:open_flags = open_flags_out[0];\n', '')

    # Fix pointers
    text = text.replace('*FILE:f', 'FILE->:f')
    text = text.replace('*FILE:fp', 'FILE->:fp')
    text = text.replace('*byte:', 'uint8->:')
    text = text.replace('byte:first', 'uint8:first')

    # Fix ternary in fopen
    if 'fopen.npk' in path:
        text = re.sub(r'f\.buf_mode = \(fd == 1i64\) \? _IOLBF : _IOFBF;', '''if (fd == 1i64) {
        f.buf_mode = _IOLBF;
    } else {
        f.buf_mode = _IOFBF;
    }''', text)

        text = re.sub(r'f\.buf_mode = \(\(open_flags & O_ACCMODE\) == O_WRONLY \|\| \(open_flags & O_ACCMODE\) == O_RDWR\) \? _IOFBF : _IOLBF;', '''if ((open_flags & O_ACCMODE) == O_WRONLY || (open_flags & O_ACCMODE) == O_RDWR) {
        f.buf_mode = _IOFBF;
    } else {
        f.buf_mode = _IOLBF;
    }''', text)

    with open(path, 'w') as f:
        f.write(text)

fix_file('src/io/bio/file.npk')
fix_file('src/io/bio/fopen.npk')

