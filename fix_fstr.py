import re

with open('src/io/bio/fstr.npk', 'r') as f:
    content = f.read()

content = content.replace(
'''            if (rr.is_error || rr.value == 0i64) {
                if (count == 0i64) { pass 0i64; }
                break;
            }''',
'''            if (rr.is_error) {
                if (count == 0i64) { pass 0i64; }
                break;
            }
            if (rr.value == 0i64) {
                if (count == 0i64) { pass 0i64; }
                break;
            }''')

with open('src/io/bio/fstr.npk', 'w') as f:
    f.write(content)
