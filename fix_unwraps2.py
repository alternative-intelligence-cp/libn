import re

def fix_file(filename, replacements):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, regex, repl in replacements:
        idx = line_num - 1
        lines[idx] = re.sub(regex, repl, lines[idx])
        
    with open(filename, 'w') as f:
        f.writelines(lines)

fopen_reps = [
    (81, r'int64:buf = bio_alloc_buf\((.*)\);', r'Result<int64>:buf_res = bio_alloc_buf(\1);\n    if (buf_res.is_error) { pass 0i64; }\n    int64:buf = buf_res.value;'),
    (116, r'int64:parse_ok = bio_parse_mode\((.*)\);', r'Result<int64>:parse_res = bio_parse_mode(\1);\n    if (parse_res.is_error) {\n        drop(errno_set(EINVAL));\n        pass 0i64;\n    }\n    int64:parse_ok = parse_res.value;'),
    (134, r'int64:fp = fdopen\((.*)\);', r'Result<int64>:fp_res = fdopen(\1);\n    if (fp_res.is_error) { pass 0i64; }\n    int64:fp = fp_res.value;'),
    (178, r'int64:parse_ok = bio_parse_mode\((.*)\);', r'Result<int64>:parse_res = bio_parse_mode(\1);\n    if (parse_res.is_error) {\n        drop(errno_set(EINVAL));\n        pass 0i64;\n    }\n    int64:parse_ok = parse_res.value;'),
    (184, r'int64:fp = fdopen\((.*)\);', r'Result<int64>:fp_res = fdopen(\1);\n    if (fp_res.is_error) { pass 0i64; }\n    int64:fp = fp_res.value;'),
    (225, r'int64:parse_ok = bio_parse_mode\((.*)\);', r'Result<int64>:parse_res = bio_parse_mode(\1);\n    if (parse_res.is_error) {\n        drop(fclose(fp));\n        drop(errno_set(EINVAL));\n        pass 0i64;\n    }\n    int64:parse_ok = parse_res.value;'),
]

tmpfile_reps = [
    (119, r'int64:tmpl_len = str_strlen\((.*)\);', r'Result<int64>:tmpl_res = str_strlen(\1);\n    if (tmpl_res.is_error) { pass -1i64; }\n    int64:tmpl_len = tmpl_res.value;'),
    (143, r'int64:entropy = tmpfile_get_entropy\((.*)\);', r'Result<int64>:ent_res = tmpfile_get_entropy(\1);\n        if (ent_res.is_error) { pass -1i64; }\n        int64:entropy = ent_res.value;'),
    (183, r'int64:tmpl_len = str_strlen\((.*)\);', r'Result<int64>:tmpl_res = str_strlen(\1);\n    if (tmpl_res.is_error) { pass 0i64; }\n    int64:tmpl_len = tmpl_res.value;'),
    (202, r'int64:entropy = tmpfile_get_entropy\((.*)\);', r'Result<int64>:ent_res = tmpfile_get_entropy(\1);\n        if (ent_res.is_error) { pass 0i64; }\n        int64:entropy = ent_res.value;'),
    (242, r'int64:pfx_len = str_strlen\((.*)\);', r'Result<int64>:pfx_res = str_strlen(\1);\n    if (pfx_res.is_error) { pass 0i64; }\n    int64:pfx_len = pfx_res.value;'),
    (246, r'int64:fd = mkostemp\((.*)\);', r'Result<int64>:fd_res = mkostemp(\1);\n    if (fd_res.is_error) { pass 0i64; }\n    int64:fd = fd_res.value;'),
]

fix_file('src/io/bio/fopen.npk', fopen_reps)
fix_file('src/io/bio/tmpfile.npk', tmpfile_reps)
