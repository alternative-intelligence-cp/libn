import os
import re

def fix_fscanf():
    path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fscanf.npk'
    with open(path, 'r') as f:
        content = f.read()

    # Replace missing parens in if conditions
    content = content.replace('if c != 32i64 && c != 9i64 && c != 10i64 &&\n           c != 13i64 && c != 12i64 && c != 11i64 {',
                              'if (c != 32i64 && c != 9i64 && c != 10i64 &&\n           c != 13i64 && c != 12i64 && c != 11i64) {')
    content = content.replace('} else if c == 43i64 && chars < max {', '} else if (c == 43i64 && chars < max) {')
    content = content.replace('} else if base == 16i64 {', '} else if (base == 16i64) {')
    content = content.replace('} else if c >= 97i64 && c <= 102i64 {', '} else if (c >= 97i64 && c <= 102i64) {')
    content = content.replace('if c == 32i64 || c == 9i64 || c == 10i64 ||\n           c == 13i64 || c == 12i64 || c == 11i64 {',
                              'if (c == 32i64 || c == 9i64 || c == 10i64 ||\n           c == 13i64 || c == 12i64 || c == 11i64) {')
    
    # Missing parens elsewhere
    content = content.replace('if f[fi] == 108u8 || f[fi] == 104u8 || f[fi] == 122u8 ||\n           f[fi] == 106u8 || f[fi] == 116u8 {',
                              'if (f[fi] == 108u8 || f[fi] == 104u8 || f[fi] == 122u8 ||\n           f[fi] == 106u8 || f[fi] == 116u8) {')
    content = content.replace('} else if !suppress {', '} else if (!suppress) {')
    content = content.replace('} else if spec == 117u8 {', '} else if (spec == 117u8) {')
    content = content.replace('} else if spec == 111u8 {', '} else if (spec == 111u8) {')
    content = content.replace('} else if spec == 120u8 || spec == 88u8 {', '} else if (spec == 120u8 || spec == 88u8) {')

    with open(path, 'w') as f:
        f.write(content)


def fix_math():
    path = '/home/randy/Workspace/REPOS/libn/src/math/math.npk'
    with open(path, 'r') as f:
        content = f.read()

    # fix ternary
    content = content.replace('is (pass a == INT64_MIN) : 0i64 : INT64_MAX;', 'pass is (a == INT64_MIN) : 0i64 : INT64_MAX;')
    
    # fix limit keyword
    content = content.replace('int64:limit = INT64_MAX / abs_b;', 'int64:max_val = INT64_MAX / abs_b;')
    content = content.replace('if (abs_a > limit) {', 'if (abs_a > max_val) {')

    with open(path, 'w') as f:
        f.write(content)

fix_fscanf()
fix_math()
print("Fixed fscanf and math")
