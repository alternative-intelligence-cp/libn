import sys
import re

def fix_tmpfile():
    with open('/home/randy/Workspace/REPOS/libn/src/io/bio/tmpfile.npk', 'r') as f:
        content = f.read()
    
    content = content.replace("int64:tmpl_len = str_strlen", "int64:tmpl_len = raw str_strlen")
    content = content.replace("int64:pfx_len = str_strlen", "int64:pfx_len = raw str_strlen")
    content = content.replace("int64:fp = fdopen", "int64:fp = raw fdopen")
    
    with open('/home/randy/Workspace/REPOS/libn/src/io/bio/tmpfile.npk', 'w') as f:
        f.write(content)

def fix_fprintf():
    with open('/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk', 'r') as f:
        content = f.read()
    
    content = re.sub(r'int64:len = str_snprintf', r'int64:len = raw str_snprintf', content)
    
    with open('/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk', 'w') as f:
        f.write(content)

fix_tmpfile()
fix_fprintf()
