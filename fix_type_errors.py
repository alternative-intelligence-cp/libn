import re
import os

def read_errors(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def fix_errors():
    lines = read_errors("build_errors.txt")
    errors_by_file = {}
    
    current_error = None
    for line in lines:
        match = re.match(r"test_all\.npk:\d+:\d+: error: Line \d+, Column \d+:   Type check error in (.+):", line)
        if match:
            # wait, my npkc prints:
            # test_all.npk:0:0: error: Line X, Column Y: <msg>
            # But earlier it was Type check error in ... wait, let's see how `npkc` prints it in `build_errors.txt`.
            pass

