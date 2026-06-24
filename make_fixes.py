import re
import os

def replace_in_file(filename, old, new):
    if not os.path.exists(filename): return
    with open(filename, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Fixed {filename}")

replace_in_file('src/str/strchr.npk', 
    'if (to_lower_ascii(h[i]) == first_lo) {', 
    'if (to_lower_ascii(raw h[i]) == first_lo) {')

replace_in_file('src/str/strchr.npk',
    'while (n[j] != 0u8 && h[i + j] != 0u8 &&',
    'while ((raw n[j]) != 0u8 && (raw h[i + j]) != 0u8 &&')

replace_in_file('src/str/strchr.npk',
    'to_lower_ascii(h[i + j]) == to_lower_ascii(n[j])) {',
    'to_lower_ascii(raw h[i + j]) == to_lower_ascii(raw n[j])) {')

replace_in_file('src/str/strchr.npk',
    'if (h[i] == first) {',
    'if ((raw h[i]) == first) {')

replace_in_file('src/str/strchr.npk',
    'while (n[j] != 0u8 && h[i + j] != 0u8 &&',
    'while ((raw n[j]) != 0u8 && (raw h[i + j]) != 0u8 &&') # Wait, I already did this. 

replace_in_file('src/str/strchr.npk',
    'h[i + j] == n[j]) {',
    '(raw h[i + j]) == (raw n[j])) {')

replace_in_file('src/str/strchr.npk',
    'pass (table[c >> 3u8] >> (c & 7u8)) & 1u8 != 0u8;',
    'pass ((table[c >> 3u8] >> (c & 7u8)) & 1u8) != 0u8;')

replace_in_file('src/str/strlen.npk',
    'while (!has_nul_byte(pw[wi])) {',
    'while (!(has_nul_byte(raw pw[wi]))) {')

