with open('src/str/strconv.npk', 'r') as f:
    content = f.read()

target = """    int64:digit_start = i;
    int64:result = 0i64;
    bool:overflow = false;

    while (true) {
        int64:dv = raw digit_val(p[i], base);
        if (dv < 0i64) { break; }
          // Unsigned overflow: result > (UINT64_MAX - dv) / base
          // In two's complement int64: UINT64_MAX = -1 (all bits set)
          // We detect overflow by checking if (result * base + dv) would exceed UINT64_MAX.
          // Using: result > (UINT64_MAX - dv) / base
          // Since UINT64_MAX = (int64)−1 @cast_unchecked<unsigned>(but), use bit tricks:
          // Safe: if result > (-1i64 / @cast_unchecked<uint>(base) - dv / @cast_unchecked<uint>(base)) overflow
          // This is subtle. Simple approach: compare directly.
          // result * base + dv > UINT64_MAX
          // ↔ result > (UINT64_MAX - dv) / base
          // In Nitpick int64 arithmetic, UINT64_MAX = -1i64 treated unsigned.
          // We use: raw unsigned compare. For now, use signed approximation:
        if (result < 0i64) {
              // result already has top bit set → any more makes it overflow
            overflow = true;
            break;
        }
          // result ≤ INT64_MAX here
          // Overflow if result > (INT64_MAX - dv) / base (conservative)
        if (result > (INT64_MAX - dv) / base) {
            overflow = true;
            break;
        }
        result = result * base + dv;
        i = i + 1i64;
    }"""

replacement = """    int64:digit_start = i;
    uint64:result = 0u64;
    bool:overflow = false;
    uint64:ubase = @cast_unchecked<uint64>(base);
    uint64:umax = @cast_unchecked<uint64>(-1i64);

    while (true) {
        int64:dv = raw digit_val(p[i], base);
        if (dv < 0i64) { break; }
        uint64:udv = @cast_unchecked<uint64>(dv);

        if (result > (umax - udv) / ubase) {
            overflow = true;
            break;
        }
        result = result * ubase + udv;
        i = i + 1i64;
    }"""

if target in content:
    content = content.replace(target, replacement)
    
    # Also fix the return value type from u64 to int64 by casting
    content = content.replace("pass is (negate) : 0i64 - result : result;", "pass is (negate) : 0i64 - @cast_unchecked<int64>(result) : @cast_unchecked<int64>(result);")
    
    with open('src/str/strconv.npk', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Target not found.")
