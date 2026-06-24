import re

with open("src/str/strfmt.npk", "r") as f:
    content = f.read()

render_uint_old = """func:render_uint = int64(int64:v, int64:base, int64:buf, bool:upper) {
    uint8->:b = @cast_unchecked<uint8->>(buf);
    uint8->:digits = @cast_unchecked<uint8->>(is (upper) : DIGITS_UPPER : DIGITS_LOWER);

    if (v == 0i64) {
        b[0] = 48u8;    // '0'
        pass 1i64;
    }

    stack uint8[66]:tmp;
    int64:ti = 0i64;
    int64:u = v;

      // Build digits in reverse
    while (u != 0i64) {
        int64:d = 0i64;
          // For base 2, 8, 16: use bitwise ops (exact for unsigned interpretation)
        if (base == 16i64) {
            d = u & 0xFi64;
            u = (u >> 4i64) & 0x0FFFFFFFFFFFFFFFi64;    // logical shift: mask off sign
        } else if (base == 8i64) {
            d = u & 7i64;
            u = (u >> 3i64) & 0x1FFFFFFFFFFFFFFFi64;
        } else if (base == 2i64) {
            d = u & 1i64;
            u = (u >> 1i64) & 0x7FFFFFFFFFFFFFFFi64;
        } else {
              // base 10: if top bit is set, do two-step to handle uint64 > INT64_MAX
            if (u < 0i64) {
                  // v > INT64_MAX: split into high/low halves
                  // u = high * 10000000000000000000 + low
                  // This handles values up to UINT64_MAX correctly
                  // Simple approximation for v0.3.7: use modular arithmetic
                  // For values in [INT64_MAX+1..UINT64_MAX] this is a known-hard problem
                  // without unsigned division. Defer to v0.40.x uint64 division.
                  // For now: render INT64_MAX @cast_unchecked<the>(("9223372036854775807")) max.
                pass str_itoa(9223372036854775807i64, buf, 66i64);
            }
            d = u % 10i64;
            u = u / 10i64;
        }
        tmp[ti] = digits[d];
        ti = ti + 1i64;
        if (u == 0i64) { break; }
    }"""

render_uint_new = """func:render_uint = int64(uint64:v, int64:base, int64:buf, bool:upper) {
    uint8->:b = @cast_unchecked<uint8->>(buf);
    uint8->:digits = @cast_unchecked<uint8->>(is (upper) : DIGITS_UPPER : DIGITS_LOWER);

    if (v == 0u64) {
        b[0] = 48u8;    // '0'
        pass 1i64;
    }

    stack uint8[66]:tmp;
    int64:ti = 0i64;
    uint64:u = v;
    uint64:ubase = @cast_unchecked<uint64>(base);

      // Build digits in reverse
    while (u != 0u64) {
        int64:d = 0i64;
        if (base == 16i64) {
            d = @cast_unchecked<int64>(u & 0xFu64);
            u = u >> 4u64;
        } else if (base == 8i64) {
            d = @cast_unchecked<int64>(u & 7u64);
            u = u >> 3u64;
        } else if (base == 2i64) {
            d = @cast_unchecked<int64>(u & 1u64);
            u = u >> 1u64;
        } else {
            d = @cast_unchecked<int64>(u % ubase);
            u = u / ubase;
        }
        tmp[ti] = digits[d];
        ti = ti + 1i64;
    }"""

content = content.replace(render_uint_old, render_uint_new)
content = content.replace("        nlen = raw render_uint(uval, num_base, @cast_unchecked<int64>(@nbuf[0]), is_upper);", "        nlen = raw render_uint(@cast_unchecked<uint64>(uval), num_base, @cast_unchecked<int64>(@nbuf[0]), is_upper);")

with open("src/str/strfmt.npk", "w") as f:
    f.write(content)

