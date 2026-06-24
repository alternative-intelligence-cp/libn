import re

def fix_file(filename, replacements):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, old_str, new_str in replacements:
        idx = line_num - 1
        lines[idx] = lines[idx].replace(old_str, new_str)
        
    with open(filename, 'w') as f:
        f.writelines(lines)

fopen_reps = [
    (81, "int64:buf = bio_alloc_buf(", "Result<int64>:buf_res = bio_alloc_buf(\n        if (buf_res.is_error) { pass 0i64; }\n        int64:buf = buf_res.value; //"),
    (116, "int64:parse_ok = bio_parse_mode(", "Result<int64>:parse_res = bio_parse_mode(\n    if (parse_res.is_error) { pass 0i64; }\n    int64:parse_ok = parse_res.value; //"),
    (134, "int64:fp = fdopen(", "Result<int64>:fp_res = fdopen(\n    if (fp_res.is_error) { pass 0i64; }\n    int64:fp = fp_res.value; //"),
    (178, "int64:parse_ok = bio_parse_mode(", "Result<int64>:parse_res = bio_parse_mode(\n    if (parse_res.is_error) { pass 0i64; }\n    int64:parse_ok = parse_res.value; //"),
    (184, "int64:fp = fdopen(", "Result<int64>:fp_res = fdopen(\n    if (fp_res.is_error) { pass 0i64; }\n    int64:fp = fp_res.value; //"),
    (225, "int64:parse_ok = bio_parse_mode(", "Result<int64>:parse_res = bio_parse_mode(\n    if (parse_res.is_error) { pass 0i64; }\n    int64:parse_ok = parse_res.value; //"),
]

tmpfile_reps = [
    (119, "int64:tmpl_len = str_strlen(", "Result<int64>:tmpl_res = str_strlen(\n    if (tmpl_res.is_error) { pass -1i64; }\n    int64:tmpl_len = tmpl_res.value; //"),
    (143, "int64:entropy = tmpfile_get_entropy(", "Result<int64>:ent_res = tmpfile_get_entropy(\n        if (ent_res.is_error) { pass -1i64; }\n        int64:entropy = ent_res.value; //"),
    (183, "int64:tmpl_len = str_strlen(", "Result<int64>:tmpl_res = str_strlen(\n    if (tmpl_res.is_error) { pass 0i64; }\n    int64:tmpl_len = tmpl_res.value; //"),
    (202, "int64:entropy = tmpfile_get_entropy(", "Result<int64>:ent_res = tmpfile_get_entropy(\n        if (ent_res.is_error) { pass 0i64; }\n        int64:entropy = ent_res.value; //"),
    (242, "int64:pfx_len = str_strlen(", "Result<int64>:pfx_res = str_strlen(\n    if (pfx_res.is_error) { pass 0i64; }\n    int64:pfx_len = pfx_res.value; //"),
    (246, "int64:fd = mkostemp(", "Result<int64>:fd_res = mkostemp(\n    if (fd_res.is_error) { pass 0i64; }\n    int64:fd = fd_res.value; //"),
]

fix_file('src/io/bio/fopen.npk', fopen_reps)
fix_file('src/io/bio/tmpfile.npk', tmpfile_reps)
