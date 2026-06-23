#!/bin/bash
find src -type f -name '*.npk' | while read f; do
    # Fix .err to .error
    sed -i 's/\.err/\.error/g' "$f"
    
    # Fix errno_set to libn_errno_set
    sed -i 's/\berrno_set\b/libn_errno_set/g' "$f"
    
    # Fix bio_ensure_std_init to drop bio_ensure_std_init
    # Only if it's not already drop or raw
    sed -i 's/^\s*bio_ensure_std_init();/    drop bio_ensure_std_init();/g' "$f"

    # Fix sys_safe to drop sys_safe if unused
    sed -i 's/^\s*sys_safe(/    drop sys_safe(/g' "$f"
done
