#!/bin/bash
git checkout src/

python3 apply_all_fixes.py
python3 fix_pick.py
python3 fix_memset.py
python3 fix_remaining_syntax.py
python3 fix_address_of.py
python3 fix_all_as.py
python3 fix_ternary.py
python3 fix_struct_close.py
python3 fix_top_level_braces.py
python3 fix_arrays.py

# Fix specific paren bugs
sed -i 's/if (prot & PROT_EXEC) != 0i64) {/if ((prot \& PROT_EXEC) != 0i64) {/g' src/syscall/syscall.npk
sed -i 's/if (prot & PROT_EXEC) != 0i64) {/if ((prot \& PROT_EXEC) != 0i64) {/g' src/mem/mmap.npk
sed -i 's/if (raw has_zero_byte(v) {/if (raw has_zero_byte(v)) {/g' src/mem/memutil.npk
sed -i 's/if (size > 0i64 && n > (9223372036854775807i64 \/ size) {/if (size > 0i64 \&\& n > (9223372036854775807i64 \/ size)) {/g' src/mem/mmap.npk

# Fix slab comment parser bug where 'is' is parsed as a keyword
sed -i 's/is above/is_above/g; s/for inline/for_inline/g' src/mem/slab.npk

# Fix memset 'as byte'
sed -i 's/(p32 >> ((i \& 3i64) \* 8i64)) as byte;/@cast_unchecked<uint8>((p32 >> ((i \& 3i64) \* 8i64)));/g' src/mem/memset.npk

# Fix multi-line else if in strconv.npk
perl -0777 -pi -e 's/\} else if base == 16i64 \&\& p\[i\] == 48u8 \&\&\n\s+\(p\[i \+ 1i64\] == 120u8 \|\| p\[i \+ 1i64\] == 88u8\) \{/\} else if \(base == 16i64 \&\& p\[i\] == 48u8 \&\&\n              \(p\[i \+ 1i64\] == 120u8 \|\| p\[i \+ 1i64\] == 88u8\)\) \{/g' src/str/strconv.npk

# Added script to fix pointer comparisons (int64-> vs int64)
python3 fix_ptr_cmp.py
# Added script to fix bitwise operator precedence in strcmp
python3 fix_strcmp.py
# Added scripts to fix string literal types and casts
python3 fix_literals.py
python3 fix_string_casts.py
python3 fix_missing_imports.py
python3 fix_errno_names.py
python3 fix_strcpy_end.py
python3 fix_missing_funcs.py
python3 fix_strerror_unwraps.py
python3 fix_trailing_comma.py
python3 fix_errno_return.py
python3 fix_sys_full_impl.py
python3 fix_mmap_unwraps.py

python3 fix_fscanf.py
python3 fix_byte.py
python3 fix_results.py
python3 fix_return_types.py
python3 fix_err_to_error.py
python3 fix_unused.py
python3 fix_void.py
python3 fix_strcpy_bug.py

python3 fix_libn_remnants.py

/home/randy/Workspace/REPOS/nitpick/build/npkc -c test_root.npk
