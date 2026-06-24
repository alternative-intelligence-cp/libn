import sys

def replace_in_file(path, old, new):
    with open(path, 'r') as f: content = f.read()
    with open(path, 'w') as f: f.write(content.replace(old, new))

# 1. g_open_files
replace_in_file('src/io/bio/stdfiles.npk', 'pub int64:g_open_files = 0i64;\n', '')
with open('src/io/bio/file.npk', 'a') as f: f.write('\npub int64:g_open_files = 0i64;\n')

# 2. fopen and fio imports
# Nothing needed since I moved g_open_files to file.npk, which is ALREADY imported by fopen and fio!

# 3. open.npk
replace_in_file('src/io/open.npk', 'sys_safe(SYS_OPEN, path, safe_flags, mode);', 'sys_safe(SYS_OPEN, path, safe_flags, mode, 0i64, 0i64, 0i64);')

# 4. env.npk
env_old = '''    int64:cap = n + ENV_INITIAL_CAP;
    Result<int64>:r = mem_malloc((cap + 1i64) * 8i64);    // +1 for NULL terminator
    if (r.is_error) {'''
env_new = '''    int64:cap = n + ENV_INITIAL_CAP;
    Result<int64>:r = mem_malloc((cap + 1i64) * 8i64);    // +1 for NULL terminator
    Result<int64>:r2 = mem_malloc((cap + 1i64) * 8i64);
    if (r.is_error || r2.is_error) {
        if (!r.is_error) { drop mem_free(r.value); }'''
replace_in_file('src/proc/env.npk', env_old, env_new)

# 5. strerror.npk
replace_in_file('src/io/bio/strerror.npk', 'str_int64_to_dec(', 'str_itoa(')

# 6. bio_init_stream
fopen_old = 'func:bio_init_stream = Result<int64>(int64:fp, int64:fd, int64:file_mode, bool:is_static) {'
fopen_new = 'func:bio_init_stream = int64(int64:fp, int64:fd, int64:file_mode, bool:is_static) {'
replace_in_file('src/io/bio/fopen.npk', fopen_old, fopen_new)

print("Applied reverts.")
