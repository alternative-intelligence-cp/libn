with open("src/io/bio/strerror.npk", "r") as f:
    content = f.read()

import re
content = re.sub(r'pass "([^"]+)" as int64;', r'pass @cast_unchecked<int64>("\1");', content)

with open("src/io/bio/strerror.npk", "w") as f:
    f.write(content)
