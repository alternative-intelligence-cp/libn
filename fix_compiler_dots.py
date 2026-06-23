import os
import re

with open("no_ansi.txt", "r") as f:
    lines = f.readlines()

file_edits = {}

# Parse lines like:
# src/io/bio/fio.npk:99:7: error: Member access (.) requires struct, object, or union type, got '*FILE'. Use -> for pointer member access.
# Wait, no_ansi.txt has the raw error format:
# test_all.npk:0:0: error: Line 99, Column 7: Member access (.) requires struct...
# Oh, we don't have the file name! 

# Let's run npkc on the individual files to get the exact file names and line numbers.
# But wait, libn uses "test_all.npk" to compile everything. If I use npkc on "test_all.npk", the errors are reported against test_all.npk if the compiler doesn't track origins, or the mapping script tracks it.
