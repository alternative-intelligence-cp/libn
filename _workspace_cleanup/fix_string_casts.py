import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()

    # Find @cast_unchecked<int64>("...") and replace it with @cast_unchecked<int64>(@("..."[0]))
    # But wait, does Nitpick support indexing literals like "..."[0]?
    # Probably not. Let's just create variables for them where needed.
    
    # We can just manually fix the known occurrences since there are only 5.
    
    if "tmpfile.npk" in filepath:
        code = code.replace(
            'int64:fp = fdopen(fd, @cast_unchecked<int64>("w+b"));',
            'fixed string:mode_w_plus_b = "w+b";\n    int64:fp = fdopen(fd, @cast_unchecked<int64>(mode_w_plus_b));'
        )

    if "printf.npk" in filepath:
        code = code.replace(
            'Result<int64>:r2 = io_write_str(STDERR_FD, @cast_unchecked<int64>(": "));',
            'fixed string:colon_space = ": ";\n        Result<int64>:r2 = io_write_str(STDERR_FD, @cast_unchecked<int64>(colon_space));'
        )
        
    if "exec.npk" in filepath:
        code = code.replace(
            'int64:path_str = proc_getenv_from(envp, @cast_unchecked<int64>("PATH"));',
            'fixed string:path_env_name = "PATH";\n    int64:path_str = proc_getenv_from(envp, @cast_unchecked<int64>(path_env_name));'
        )
        code = code.replace(
            'path_str = @cast_unchecked<int64>("/usr/local/bin:/usr/bin:/bin");',
            'fixed string:default_path = "/usr/local/bin:/usr/bin:/bin";\n        path_str = @cast_unchecked<int64>(default_path);'
        )

    if "wait.npk" in filepath:
        code = code.replace(
            '//       execlp1(@cast_unchecked<int64>("ls"), @cast_unchecked<int64>("ls"));',
            '//       execlp1(ls, ls);'
        )

    if "strconv.npk" in filepath:
        old_code = """    if (v == INT64_MIN) {
        int64:s = raw str_strlen("-9223372036854775808");
        if (buf_size <= s) { pass 0i64; }
        drop str_strcpy(buf, @cast_unchecked<int64>(@"-9223372036854775808"[0]));
        pass s;
    }"""
        new_code = """    if (v == INT64_MIN) {
        fixed string:min_str = "-9223372036854775808";
        int64:min_ptr = @cast_unchecked<int64>(@min_str);
        int64:s = raw str_strlen(min_ptr);
        if (buf_size <= s) { pass 0i64; }
        drop str_strcpy(buf, min_ptr);
        pass s;
    }"""
        code = code.replace(old_code, new_code)

    with open(filepath, 'w') as f:
        f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_file(os.path.join(root, f))
