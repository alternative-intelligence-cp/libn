with open("src/mem/slab.npk", "r") as f:
    content = f.read()

content = content.replace("hdr_byte[0] = i as byte;", "hdr_byte[0] = @cast_unchecked<byte>(i);")
content = content.replace("fail ENOMEM as tbb8;", "fail ENOMEM;")
content = content.replace("*int64:next_ptr = user_ptr as *int64;", "int64->:next_ptr = @cast_unchecked<int64->>(user_ptr);")
content = content.replace("*byte:hdr = slot_start as *byte;", "byte->:hdr = @cast_unchecked<byte->>(slot_start);")
content = content.replace("int64:cls = hdr[0] as int64;", "int64:cls = @cast_unchecked<int64>(hdr[0]);")

with open("src/mem/slab.npk", "w") as f:
    f.write(content)
