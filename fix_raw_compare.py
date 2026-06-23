import re

env_path = '/home/randy/Workspace/REPOS/libn/src/proc/env.npk'
with open(env_path, 'r') as f:
    env_content = f.read()

env_content = env_content.replace('getenv(name) != 0i64', 'raw getenv(name) != 0i64')

with open(env_path, 'w') as f:
    f.write(env_content)

strview_path = '/home/randy/Workspace/REPOS/libn/src/str/strview.npk'
with open(strview_path, 'r') as f:
    strview_content = f.read()

strview_content = strview_content.replace('strview_find_str(sv, needle) >= 0i64', 'raw strview_find_str(sv, needle) >= 0i64')
strview_content = strview_content.replace('strview_find(sv, needle) >= 0i64', 'raw strview_find(sv, needle) >= 0i64')

with open(strview_path, 'w') as f:
    f.write(strview_content)

print("Fixed comparisons")
