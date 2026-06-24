import re

with open("src/io/bio/strerror.npk", "r") as f:
    content = f.read()

# We need to extract the errno values and strings
matches = re.findall(r'\{\s*(\d+)i64,\s*@cast_unchecked<int64>\((@"[^"]+")\)\s*\},', content)
table = ['0i64'] * 135

for code_str, msg in matches:
    code = int(code_str)
    if code <= 134:
        table[code] = f'@cast_unchecked<int64>({msg})'

table_str = "fixed int64[135]:errno_table = [\n    " + ",\n    ".join(table) + "\n];\n"

content = re.sub(r'fixed ErrEntry\[\]:errno_table = \[.*?\];', table_str, content, flags=re.DOTALL)

# Refactor strerror to use O(1)
new_strerror = """pub func:strerror = int64(int64:errnum) {
    if (errnum >= 0i64 && errnum <= 134i64) {
        int64:msg = errno_table[errnum];
        if (msg != 0i64) {
            pass msg;
        }
    }
    uint8->:dst = @cast_unchecked<uint8->>(@g_strerror_unknown_buf[0]);
    fixed int64:prefix = @cast_unchecked<int64>(@"Unknown error ");
    int64:prefix_len = raw str_strlen(@cast_unchecked<int64>(prefix));
    drop(mem_memcpy(@cast_unchecked<int64>(@dst[0]), @cast_unchecked<int64>(prefix), prefix_len));
    stack uint8[24]:num;
    int64:num_len = raw str_itoa(errnum, @cast_unchecked<int64>(@num[0]), 24i64);
    drop(mem_memcpy(@cast_unchecked<int64>(@dst[prefix_len]), @cast_unchecked<int64>(@num[0]), num_len + 1i64));
    pass @cast_unchecked<int64>(@g_strerror_unknown_buf[0]);
};"""

content = re.sub(r'pub func:strerror = int64\(int64:errnum\) \{.*?\n\};', new_strerror, content, flags=re.DOTALL)

# Refactor strerror_r
new_strerror_r = """pub func:strerror_r = int64(int64:errnum, int64:buf, int64:buflen) {
    if (buf == 0i64 || buflen <= 0i64) {
        pass EINVAL;
    }

    int64:msg = 0i64;
    if (errnum >= 0i64 && errnum <= 134i64) {
        msg = errno_table[errnum];
    }
    
    if (msg != 0i64) {
        int64:msg_len = raw str_strlen(msg);
        if (msg_len + 1i64 > buflen) {
            drop(mem_memcpy(buf, msg, buflen - 1i64));
            (@cast_unchecked<uint8->>(buf))[buflen - 1i64] = 0u8;
            pass ERANGE;
        }
        drop(mem_memcpy(buf, msg, msg_len + 1i64));
        pass 0i64;
    }

    // Unknown error rendering securely into caller buffer
    fixed int64:prefix = @cast_unchecked<int64>(@"Unknown error ");
    int64:prefix_len = raw str_strlen(@cast_unchecked<int64>(prefix));
    
    stack uint8[24]:num;
    int64:num_len = raw str_itoa(errnum, @cast_unchecked<int64>(@num[0]), 24i64);
    
    int64:total_len = prefix_len + num_len;
    if (total_len + 1i64 > buflen) {
        // Truncation required for unknown error
        int64:copy1 = prefix_len;
        if (copy1 > buflen - 1i64) { copy1 = buflen - 1i64; }
        drop(mem_memcpy(buf, @cast_unchecked<int64>(prefix), copy1));
        
        int64:copy2 = buflen - 1i64 - copy1;
        if (copy2 > 0i64) {
            drop(mem_memcpy(buf + copy1, @cast_unchecked<int64>(@num[0]), copy2));
        }
        (@cast_unchecked<uint8->>(buf))[buflen - 1i64] = 0u8;
        pass ERANGE;
    }
    
    drop(mem_memcpy(buf, @cast_unchecked<int64>(prefix), prefix_len));
    drop(mem_memcpy(buf + prefix_len, @cast_unchecked<int64>(@num[0]), num_len + 1i64));
    pass EINVAL;
};"""

content = re.sub(r'pub func:strerror_r = int64\(int64:errnum, int64:buf, int64:buflen\) \{.*?\n\};', new_strerror_r, content, flags=re.DOTALL)

# Refactor perror to use strerror_r
new_perror = """pub func:perror = NIL(int64:prefix) {
    drop(bio_ensure_std_init());

    if (prefix != 0i64 && (@cast_unchecked<uint8->>(prefix))[0] != 0u8) {
        drop(fputs(prefix, stderr_fp));
        drop(fputc(58i64, stderr_fp));     // ':'
        drop(fputc(32i64, stderr_fp));     // ' '
    }

    stack uint8[256]:msg_buf;
    int64:errnum = @cast_unchecked<int64>(libn_errno);
    drop(strerror_r(errnum, @cast_unchecked<int64>(@msg_buf[0]), 256i64));
    
    drop(fputs(@cast_unchecked<int64>(@msg_buf[0]), stderr_fp));
    drop(fputc(10i64, stderr_fp));     // '\\n'
    drop(fflush(stderr_fp));
};"""

content = re.sub(r'pub func:perror = NIL\(int64:prefix\) \{.*?\n\};', new_perror, content, flags=re.DOTALL)

with open("src/io/bio/strerror.npk", "w") as f:
    f.write(content)

