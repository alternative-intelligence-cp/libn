import os

filepath = 'src/mem/memutil.npk'
with open(filepath, 'r') as f:
    code = f.read()

funcs = """
// has_zero_byte - Returns true if any byte in the 64-bit word is zero
func:has_zero_byte = bool(int64:v) {
    int64:mask = -9187201950435737472i64; // 0x8080808080808080
    int64:ones = 72340172838076673i64;    // 0x0101010101010101
    int64:x = (v - ones) & (!v) & mask;
    pass x != 0i64;
};

// replicate_byte - repeats a byte 8 times across an int64
func:replicate_byte = int64(uint8:c) {
    int64:v = @cast_unchecked<int64>(c);
    v = v | (v << 8i64);
    v = v | (v << 16i64);
    v = v | (v << 32i64);
    pass v;
};
"""

if "func:has_zero_byte" not in code:
    code += "\n" + funcs + "\n"

with open(filepath, 'w') as f:
    f.write(code)


