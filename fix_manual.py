import re
import os

with open('src/str/strchr.npk', 'r') as f:
    c = f.read()
c = c.replace('if (to_lower_ascii(h[i]) == first_lo)', 'if (raw to_lower_ascii(h[i]) == first_lo)')
c = c.replace('to_lower_ascii(h[i + j]) == to_lower_ascii(n[j])', 'raw to_lower_ascii(h[i + j]) == raw to_lower_ascii(n[j])')
c = c.replace('(table[c >> 3u8] >> (c & 7u8)) & 1u8 != 0u8', '((table[c >> 3u8] >> (c & 7u8)) & 1u8) != 0u8')
c = c.replace('if (charset_test(', 'if (raw charset_test(')
c = c.replace('while (charset_test(', 'while (raw charset_test(')
with open('src/str/strchr.npk', 'w') as f:
    f.write(c)

with open('src/str/strcmp.npk', 'r') as f:
    c = f.read()
c = c.replace('to_lower_ascii(pa[i]) != to_lower_ascii(pb[i])', 'raw to_lower_ascii(pa[i]) != raw to_lower_ascii(pb[i])')
with open('src/str/strcmp.npk', 'w') as f:
    f.write(c)

