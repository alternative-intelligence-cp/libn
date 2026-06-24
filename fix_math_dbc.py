import re

with open('src/math/math.npk', 'r') as f:
    content = f.read()

# We need to find `math_div_ceil_i64`, `math_div_floor_i64`, `math_mod_pos_i64`
# and add `requires b != 0i64` before the `{`

for func_name in ["math_div_ceil_i64", "math_div_floor_i64", "math_mod_pos_i64"]:
    # The signature looks like: pub func:math_div_ceil_i64 = int64(int64:a, int64:b) {
    pattern = rf"(pub func:{func_name} = int64\(int64:a, int64:b\)) {{"
    content = re.sub(pattern, r"\1 requires b != 0i64 {", content)

with open('src/math/math.npk', 'w') as f:
    f.write(content)

print("Updated math.npk")
