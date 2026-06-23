import re

with open('/home/randy/Workspace/REPOS/libn/src/proc/exit.npk', 'r') as f:
    content = f.read()

# Fix raw _atexit_handlers
content = content.replace('int64:fn = raw _atexit_handlers[i];', 'int64:fn = _atexit_handlers[i];')
content = content.replace('int64:fn = raw _atqexit_handlers[i];', 'int64:fn = _atqexit_handlers[i];')

# Fix unused Results
content = content.replace('_exit(code);', 'drop _exit(code);')
content = content.replace('_exit(134i64);', 'drop _exit(134i64);')
content = content.replace('_proc_run_atexit();', 'drop _proc_run_atexit();')
content = content.replace('bio_flush_all();', 'drop bio_flush_all();')
content = content.replace('_proc_run_atqexit();', 'drop _proc_run_atqexit();')

with open('/home/randy/Workspace/REPOS/libn/src/proc/exit.npk', 'w') as f:
    f.write(content)

