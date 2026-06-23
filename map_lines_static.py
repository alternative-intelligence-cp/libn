import re
import os

def build_map():
    with open("test_all.npk") as f:
        lines = f.readlines()
        
    uses = []
    for l in lines:
        m = re.search(r'use "([^"]+)"', l)
        if m:
            uses.append(m.group(1))

    # wait, how does Nitpick count lines? 
    # the main file is parsed first? 
    # yes, test_all.npk has 15 lines. 
    # Does it count lines inside `use` starting from 1 again? 
    # Wait, the error message said "test_all.npk:0:0: error: Line 643"
    # Wait, the scanner's line counter is global.
    pass
