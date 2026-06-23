import re

with open('src/math/math.npk', 'r') as f:
    c = f.read()

# Replace math_abs_i64
c = re.sub(r'pub func:math_abs_i64 = int64\(int64:v\) \{\s*pass\(\(v == INT64_MIN\) \? INT64_MAX : \(\(v < 0i64\) \? 0i64 - v : v\)\);\s*\};',
           'pub func:math_abs_i64 = int64(int64:v) { if (v == INT64_MIN) { pass(INT64_MAX); } if (v < 0i64) { pass(0i64 - v); } pass(v); };', c)

# Replace math_min_i64
c = re.sub(r'pub func:math_min_i64 = int64\(int64:a, int64:b\) \{\s*pass\(\(a < b\) \? a : b\);\s*\};',
           'pub func:math_min_i64 = int64(int64:a, int64:b) { if (a < b) { pass(a); } pass(b); };', c)

# Replace math_max_i64
c = re.sub(r'pub func:math_max_i64 = int64\(int64:a, int64:b\) \{\s*pass\(\(a > b\) \? a : b\);\s*\};',
           'pub func:math_max_i64 = int64(int64:a, int64:b) { if (a > b) { pass(a); } pass(b); };', c)

# Replace math_min_u64
c = re.sub(r'pub func:math_min_u64 = int64\(int64:a, int64:b\) \{.*?\};',
           'pub func:math_min_u64 = int64(int64:a, int64:b) { if ((a ^ b) < 0i64) { if (a < 0i64) { pass(b); } pass(a); } if (a < b) { pass(a); } pass(b); };', c, flags=re.DOTALL)

# Replace math_max_u64
c = re.sub(r'pub func:math_max_u64 = int64\(int64:a, int64:b\) \{.*?\};',
           'pub func:math_max_u64 = int64(int64:a, int64:b) { if ((a ^ b) < 0i64) { if (a < 0i64) { pass(a); } pass(b); } if (a > b) { pass(a); } pass(b); };', c, flags=re.DOTALL)

# Replace math_clamp_i64
c = re.sub(r'pub func:math_clamp_i64 = int64\(int64:v, int64:lo, int64:hi\) \{.*?\};',
           'pub func:math_clamp_i64 = int64(int64:v, int64:lo, int64:hi) { if (v < lo) { pass(lo); } if (v > hi) { pass(hi); } pass(v); };', c, flags=re.DOTALL)

# Replace math_sign_i64
c = re.sub(r'pub func:math_sign_i64 = int64\(int64:v\) \{.*?\};',
           'pub func:math_sign_i64 = int64(int64:v) { if (v < 0i64) { pass(-1i64); } if (v > 0i64) { pass(1i64); } pass(0i64); };', c, flags=re.DOTALL)

# Replace in math_div_round_i64
c = c.replace('int64:abs_r = (r < 0i64) ? 0i64 - r : r;', 'int64:abs_r = r; if (r < 0i64) { abs_r = 0i64 - r; }')
c = c.replace('int64:abs_b = (b < 0i64) ? 0i64 - b : b;', 'int64:abs_b = b; if (b < 0i64) { abs_b = 0i64 - b; }')

with open('src/math/math.npk', 'w') as f:
    f.write(c)

with open('src/str/strcpy.npk', 'r') as f:
    c2 = f.read()
c2 = c2.replace('(r.@cast_unchecked<uint8->>(val))[actual_len] = 0u8;', '(@cast_unchecked<uint8->>(r.val))[actual_len] = 0u8;')
with open('src/str/strcpy.npk', 'w') as f:
    f.write(c2)

