import re
with open("src/mem/slab.npk", "r") as f:
    content = f.read()

content = content.replace("fail ERR_BADARG as tbb8;", "fail ERR_BADARG;")
content = content.replace("if r.is_error {", "if (r.is_error) {")
content = content.replace("if rr.is_error {", "if (rr.is_error) {")
content = content.replace("if slot_full > PAGE_SIZE {", "if (slot_full > PAGE_SIZE) {")
content = content.replace("while j < slots {", "while (j < slots) {")
content = content.replace("if j == 0i64 {", "if (j == 0i64) {")
content = content.replace("if prev_next_ptr != 0i64 {", "if (prev_next_ptr != 0i64) {")
content = content.replace("if n <= 0i64 {", "if (n <= 0i64) {")
content = content.replace("if cls >= SLAB_CLASS_COUNT {", "if (cls >= SLAB_CLASS_COUNT) {")
content = content.replace("if head == 0i64 {", "if (head == 0i64) {")

content = content.replace("*byte:hdr_byte = slot_start as *byte;", "byte->:hdr_byte = @cast_unchecked<byte->>(slot_start);")
content = content.replace("*int64:next_ptr = next_ptr_addr as *int64;", "int64->:next_ptr = @cast_unchecked<int64->>(next_ptr_addr);")
content = content.replace("*int64:prev = prev_next_ptr as *int64;", "int64->:prev = @cast_unchecked<int64->>(prev_next_ptr);")

# More casts
content = content.replace("*byte:hdr = ptr_val as *byte;", "byte->:hdr = @cast_unchecked<byte->>(ptr_val);")
content = content.replace("*int64:next_ptr = next_ptr_addr as *int64;", "int64->:next_ptr = @cast_unchecked<int64->>(next_ptr_addr);")

content = content.replace("fail r.err;", "fail r.error;")
content = content.replace("fail rr.err;", "fail rr.error;")

# pass r; -> if (r.is_error) { fail r.error; } pass r.value;
content = content.replace("Result<int64>:r = mem_malloc(n);\n        pass r;", "Result<int64>:r = mem_malloc(n);\n        if (r.is_error) { fail r.error; }\n        pass r.value;")

with open("src/mem/slab.npk", "w") as f:
    f.write(content)
