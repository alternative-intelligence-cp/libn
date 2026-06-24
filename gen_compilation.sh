#!/bin/bash
OUT="/home/randy/Workspace/META/LIBN/audits/a36/compilation.md"
mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"
cd /home/randy/Workspace/REPOS/libn
for f in $(find src -name '*.npk' | sort); do
    echo "================================================================================" >> "$OUT"
    echo "FILE: $f" >> "$OUT"
    echo "================================================================================" >> "$OUT"
    echo '```nitpick' >> "$OUT"
    cat "$f" >> "$OUT"
    echo '```' >> "$OUT"
    echo "" >> "$OUT"
done

echo "================================================================================" >> "$OUT"
echo "BUILD OUTPUT" >> "$OUT"
echo "================================================================================" >> "$OUT"
echo '```' >> "$OUT"
/home/randy/Workspace/REPOS/nitpick/build/npkc src/all.npk >> "$OUT" 2>&1
echo '```' >> "$OUT"
