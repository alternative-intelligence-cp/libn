import os

with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
# Fix struct casts (need @)
code = code.replace('@cast_unchecked<FILE->>(g_stdin_file)', '@cast_unchecked<FILE->>(@g_stdin_file)')
code = code.replace('@cast_unchecked<FILE->>(g_stdout_file)', '@cast_unchecked<FILE->>(@g_stdout_file)')
code = code.replace('@cast_unchecked<FILE->>(g_stderr_file)', '@cast_unchecked<FILE->>(@g_stderr_file)')
code = code.replace('@cast_unchecked<int64>(g_stdin_file)', '@cast_unchecked<int64>(@g_stdin_file)')
code = code.replace('@cast_unchecked<int64>(g_stdout_file)', '@cast_unchecked<int64>(@g_stdout_file)')
code = code.replace('@cast_unchecked<int64>(g_stderr_file)', '@cast_unchecked<int64>(@g_stderr_file)')

# Remove invalid raw keywords in stdfiles.npk
code = code.replace('raw bio_alloc_buf(BUFSIZ)', 'bio_alloc_buf(BUFSIZ)')
code = code.replace('raw bio_ensure_std_init()', 'bio_ensure_std_init()')
code = code.replace('raw fflush', 'fflush')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
# Remove invalid raw keywords in file.npk
code = code.replace('raw bio_parse_mode', 'bio_parse_mode')
code = code.replace('raw bio_ensure_std_init', 'bio_ensure_std_init')
code = code.replace('raw bio_alloc_file', 'bio_alloc_file')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

with open('src/io/bio/fprintf.npk', 'r') as f:
    code = f.read()
code = code.replace('raw bio_ensure_std_init()', 'bio_ensure_std_init()')
with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(code)

with open('src/io/bio/fstr.npk', 'r') as f:
    code = f.read()
code = code.replace('raw fgetc(fp)', 'fgetc(fp)')
code = code.replace('raw fputc(', 'fputc(')
with open('src/io/bio/fstr.npk', 'w') as f:
    f.write(code)

with open('src/io/bio/fscanf.npk', 'r') as f:
    code = f.read()
code = code.replace('raw bio_scan_getc', 'bio_scan_getc')
with open('src/io/bio/fscanf.npk', 'w') as f:
    f.write(code)

with open('src/proc/exec.npk', 'r') as f:
    code = f.read()
code = code.replace('@cast_unchecked<int64>("PATH")', '@cast_unchecked<int64>(@path_env_name)')
code = code.replace('@cast_unchecked<int64>("/bin:/usr/bin")', '@cast_unchecked<int64>(@default_path)')
with open('src/proc/exec.npk', 'w') as f:
    f.write(code)
