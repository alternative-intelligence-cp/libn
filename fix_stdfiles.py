import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'r') as f:
    content = f.read()

# Fix puts -> sout
content = content.replace('puts->', 'sout->')

# Fix FILE to int64[16]
content = content.replace('FILE:g_stdout_file;', 'int64[16]:g_stdout_file;')
content = content.replace('FILE:g_stderr_file;', 'int64[16]:g_stderr_file;')
content = content.replace('FILE:g_stdin_file;', 'int64[16]:g_stdin_file;')

# Fix serr.fd -> serr->fd
content = content.replace('serr.', 'serr->')

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'w') as f:
    f.write(content)

