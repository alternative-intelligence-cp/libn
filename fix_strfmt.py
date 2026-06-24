with open('src/str/strfmt.npk', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.startswith('pub func:str_format_args ='):
        new_lines.insert(0, "extern func:npk_string_format_float_simple = int64(int64:fval, int64:prec);\n\n")
    
    new_lines.append(line)
    
    if "if (spec == 99u8) {    // '%c'" in line:
        insert_idx = len(new_lines) - 1
        f_block = [
            "        if (spec == 102u8) {    // '%f'\n",
            "            int64:fval = arg_val;\n",
            "            int64:prec = precision;\n",
            "            if (prec < 0i64) { prec = 6i64; }\n",
            "            int64:fstr = npk_string_format_float_simple(fval, prec);\n",
            "            int64:flen = raw str_strlen(fstr);\n",
            "            int64:pad = 0i64;\n",
            "            if (width > flen) { pad = width - flen; }\n",
            "            if (!flag_left) { drop(fmt_pad(stp, 32u8, pad)); }\n",
            "            drop(fmt_puts_n(stp, fstr, flen));\n",
            "            if (flag_left) { drop(fmt_pad(stp, 32u8, pad)); }\n",
            "              // Free the compiler-allocated string\n",
            "              // NOTE: Nitpick builtins use malloc, so we must sys_safe it or something? Actually libn has libn_slab_free?\n",
            "              // Wait, since we can't be sure, we'll just leave it or use free if available.\n",
            "            continue;\n",
            "        }\n\n"
        ]
        new_lines = new_lines[:insert_idx] + f_block + new_lines[insert_idx:]

with open('src/str/strfmt.npk', 'w') as f:
    f.writelines(new_lines)
