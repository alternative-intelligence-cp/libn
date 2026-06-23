import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'r') as f:
    content = f.read()

# Remove g_stdin_file, g_stdout_file, g_stderr_file
content = re.sub(r'int64\[16\]:g_stdin_file;', '', content)
content = re.sub(r'int64\[16\]:g_stdout_file;', '', content)
content = re.sub(r'int64\[16\]:g_stderr_file;', '', content)

# Replace the initialization logic
content = content.replace('int64->:_ptr_in = &g_stdin_file;\n    FILE->:sin = @cast_unchecked<FILE->>(_ptr_in);', 'int64:p_in = bio_alloc_file();\n    FILE->:sin = @cast_unchecked<FILE->>(p_in);')
content = content.replace('int64->:_ptr_out = &g_stdout_file;\n    FILE->:sout = @cast_unchecked<FILE->>(_ptr_out);', 'int64:p_out = bio_alloc_file();\n    FILE->:sout = @cast_unchecked<FILE->>(p_out);')
content = content.replace('int64->:_ptr_err = &g_stderr_file;\n    FILE->:serr = @cast_unchecked<FILE->>(_ptr_err);', 'int64:p_err = bio_alloc_file();\n    FILE->:serr = @cast_unchecked<FILE->>(p_err);')

content = content.replace('stdin_fp = @cast_unchecked<int64>(_ptr_in);', 'stdin_fp = p_in;')
content = content.replace('stdout_fp = @cast_unchecked<int64>(_ptr_out);', 'stdout_fp = p_out;')
content = content.replace('stderr_fp = @cast_unchecked<int64>(_ptr_err);', 'stderr_fp = p_err;')

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'w') as f:
    f.write(content)

