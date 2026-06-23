import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'r') as f:
    content = f.read()

# We need to change @cast_unchecked<FILE->>(g_stdout_file) to use an intermediate pointer
content = content.replace(
    'FILE->:sout = @cast_unchecked<FILE->>(g_stdout_file);',
    'int64->:_ptr_out = g_stdout_file;\n    FILE->:sout = @cast_unchecked<FILE->>(_ptr_out);'
)
content = content.replace(
    'FILE->:serr = @cast_unchecked<FILE->>(g_stderr_file);',
    'int64->:_ptr_err = g_stderr_file;\n    FILE->:serr = @cast_unchecked<FILE->>(_ptr_err);'
)
content = content.replace(
    'FILE->:sin = @cast_unchecked<FILE->>(g_stdin_file);',
    'int64->:_ptr_in = g_stdin_file;\n    FILE->:sin = @cast_unchecked<FILE->>(_ptr_in);'
)

# And for stdout_fp = @cast_unchecked<int64>(g_stdout_file)
content = content.replace(
    'stdout_fp = @cast_unchecked<int64>(g_stdout_file);',
    'stdout_fp = @cast_unchecked<int64>(_ptr_out);'
)
content = content.replace(
    'stderr_fp = @cast_unchecked<int64>(g_stderr_file);',
    'stderr_fp = @cast_unchecked<int64>(_ptr_err);'
)
content = content.replace(
    'stdin_fp = @cast_unchecked<int64>(g_stdin_file);',
    'stdin_fp = @cast_unchecked<int64>(_ptr_in);'
)

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'w') as f:
    f.write(content)

