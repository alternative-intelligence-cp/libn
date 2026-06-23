with open("src/io/bio/fscanf.npk", "r") as f:
    content = f.read()

content = content.replace("if (!(width > 0i64) { max = 0x7FFFFFFFFFFFFFFFi64; }", "if (!(width > 0i64)) { max = 0x7FFFFFFFFFFFFFFFi64; }")
content = content.replace("if (c != @cast_unchecked<int64>(ch) {", "if (c != @cast_unchecked<int64>(ch)) {")
content = content.replace("if (!((spec == 105u8) { base = 10i64; }", "if (!(spec == 105u8)) { base = 10i64; }")

old_consumed = """    int64:fi     = 0i64;    // format string index
    int64:ai     = 0i64;    // argument index
    int64:matched = 0i64;   // items successfully stored
    int64:consumed = 0i64;  // total bytes consumed from source
    bool:first   = true;    // for EOF-before-any-conversion detection"""

new_consumed = """    int64:fi     = 0i64;    // format string index
    int64:ai     = 0i64;    // argument index
    int64:matched = 0i64;   // items successfully stored
    stack int64[1]:consumed_arr; // total bytes consumed from source
    consumed_arr[0] = 0i64;
    bool:first   = true;    // for EOF-before-any-conversion detection"""

content = content.replace(old_consumed, new_consumed)

content = content.replace("consumed = consumed + 1i64;", "consumed_arr[0] = consumed_arr[0] + 1i64;")
content = content.replace("(@cast_unchecked<int64->>(out))[0] = consumed;", "(@cast_unchecked<int64->>(out))[0] = consumed_arr[0];")

content = content.replace("int64:r = bio_scan_str(src, width, out, &consumed);", "int64:r = bio_scan_str(src, width, out, @cast_unchecked<int64>(consumed_arr));")
content = content.replace("int64:r = bio_scan_int(src, base, width, out, &consumed);", "int64:r = bio_scan_int(src, base, width, out, @cast_unchecked<int64>(consumed_arr));")


with open("src/io/bio/fscanf.npk", "w") as f:
    f.write(content)
