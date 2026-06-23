with open('/home/randy/Workspace/REPOS/libn/build_errors.txt', 'r') as f:
    errors = f.read()

import re
undefined = re.findall(r"Undefined identifier: '([^']+)'", errors)
from collections import Counter
for k, v in Counter(undefined).most_common(20):
    print(f"{v} {k}")
