import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'r') as f:
    content = f.read()

content = content.replace('int64->:_ptr_in = g_stdin_file;', 'int64->:_ptr_in = &g_stdin_file;')
content = content.replace('int64->:_ptr_out = g_stdout_file;', 'int64->:_ptr_out = &g_stdout_file;')
content = content.replace('int64->:_ptr_err = g_stderr_file;', 'int64->:_ptr_err = &g_stderr_file;')

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'w') as f:
    f.write(content)

