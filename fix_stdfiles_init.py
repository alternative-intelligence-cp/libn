import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'r') as f:
    content = f.read()

# Replace main. with sin->
content = content.replace('main.', 'sin->')
# Replace main-> with sin-> (just in case)
content = content.replace('main->', 'sin->')

# And fix the if condition
content = content.replace('if (stdin_fp != 0i64)', 'if (p_in != 0i64)')
content = content.replace('if (stdout_fp != 0i64)', 'if (p_out != 0i64)')
content = content.replace('if (stderr_fp != 0i64)', 'if (p_err != 0i64)')

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk', 'w') as f:
    f.write(content)

