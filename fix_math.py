import re

with open('src/math/math.npk', 'r') as f:
    content = f.read()

# Fix math_rol
content = content.replace("pass (v << n) | (v >> (64i64 - n));", "pass (v << n) | ((v >> (64i64 - n)) & ((1i64 << n) - 1i64));")

# Fix math_ror
content = content.replace("pass (v >> n) | (v << (64i64 - n));", "pass ((v >> n) & ((1i64 << (64i64 - n)) - 1i64)) | (v << (64i64 - n));")

# Fix math_sat_add_i64
sat_add_i64_old = """pub func:math_sat_add_i64 = int64(int64:a, int64:b) {
    int64:r = a + b;
      // Overflow if both operands have same sign and result has different sign
      // (a > 0 && b > 0 && r < 0) → overflow up → clamp to INT64_MAX
      // (a < 0 && b < 0 && r > 0) → underflow  → clamp to INT64_MIN
    if (a > 0i64 && b > 0i64 && r < 0i64) { pass INT64_MAX; }
    if (a < 0i64 && b < 0i64 && r > 0i64) { pass INT64_MIN; }
    pass r;
};"""

sat_add_i64_new = """pub func:math_sat_add_i64 = int64(int64:a, int64:b) {
    if (b > 0i64 && a > INT64_MAX - b) { pass INT64_MAX; }
    if (b < 0i64 && a < INT64_MIN - b) { pass INT64_MIN; }
    pass a + b;
};"""
content = content.replace(sat_add_i64_old, sat_add_i64_new)

# Fix math_sat_add_u64
sat_add_u64_old = """pub func:math_sat_add_u64 = int64(int64:a, int64:b) {
    int64:r = a + b;
    if (r < a) { pass -1i64; }
    pass r;
};"""

sat_add_u64_new = """pub func:math_sat_add_u64 = int64(int64:a, int64:b) {
    if (a > -1i64 - b) { pass -1i64; }
    pass a + b;
};"""
content = content.replace(sat_add_u64_old, sat_add_u64_new)

with open('src/math/math.npk', 'w') as f:
    f.write(content)
