with open("src/math/math.npk", "r") as f:
    lines = f.readlines()

# fix math.npk
new_math = []
skip = False
for i, line in enumerate(lines):
    if line.startswith("pub func:math_max_u64"):
        new_math.append("pub func:math_max_u64 = int64(int64:a, int64:b) {\n")
        new_math.append("    if ((a ^ b) < 0i64) {\n")
        new_math.append("        if (a < 0i64) { pass a; }\n")
        new_math.append("        pass b;\n")
        new_math.append("    }\n")
        new_math.append("    if (a > b) { pass a; }\n")
        new_math.append("    pass b;\n")
        new_math.append("};\n")
        skip = True
    elif line.startswith("// math_sign_i64"):
        skip = False
    
    if not skip:
        new_math.append(line)

with open("src/math/math.npk", "w") as f:
    f.writelines(new_math)

# fix fstate.npk
with open("src/io/bio/fstate.npk", "r") as f:
    lines = f.readlines()
lines[116] = lines[116].replace(") {", ")) {")
lines[123] = lines[123].replace(") {", ")) {")
with open("src/io/bio/fstate.npk", "w") as f:
    f.writelines(lines)

# fix exec.npk
with open("src/proc/exec.npk", "r") as f:
    content = f.read()

content = content.replace(
    "int64:r = sys!!(SYS_EXECVE, path, argv, envp, 0i64, 0i64, 0i64);\n    if (r.is_error) {\n        libn_errno_set(@cast_unchecked<int64>(r.error));\n        pass -1i64;\n    }",
    "Result<int64>:res_r = sys(SYS_EXECVE, path, argv, envp, 0i64, 0i64, 0i64);\n    if (res_r.is_error) {\n        libn_errno_set(@cast_unchecked<int64>(res_r.error));\n        pass -1i64;\n    }\n    int64:r = res_r.value;"
)
content = content.replace("\"PATH\" as int64", "@cast_unchecked<int64>(\"PATH\")")
content = content.replace("\"/usr/local/bin:/usr/bin:/bin\" as int64", "@cast_unchecked<int64>(\"/usr/local/bin:/usr/bin:/bin\")")

with open("src/proc/exec.npk", "w") as f:
    f.write(content)

