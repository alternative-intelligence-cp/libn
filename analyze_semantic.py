import re
from collections import defaultdict

with open('no_ansi.txt', 'r') as f:
    text = f.read()

errors = re.findall(r'test_all\.npk:0:0: error: Line (\d+), Column (\d+): (.+)', text)

by_file = defaultdict(list)
by_type = defaultdict(int)

# Since we don't have file names in semantic errors, we have to look up test_all.npk to see where the line is?
# Wait! "Line 233, Column 9:" means line 233 of test_all.npk!
# Because the compiler compiles test_all.npk which includes ALL libn files as ONE big file during parsing (or rather, the error locations might be mapped poorly?)
# Actually, the compiler output says `test_all.npk:0:0: error: Line 233...`
# Wait, did it report the line number inside `test_all.npk`?
# NO, the error is inside `test_all.npk` itself or in the imported files!
# Wait, `test_all.npk` only has 650 lines!
# But libn has thousands of lines!
# Does the compiler report ALL errors as being in `test_all.npk`?!
# Let's check test_all.npk line 233.
