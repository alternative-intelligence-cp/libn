import re
from collections import Counter

with open("compile_output_clean.txt", "r") as f:
    text = f.read()

errors = re.findall(r'error: Line \d+, Column \d+:\s+Undefined identifier: (.*?)(?=Did|\n|\Z)', text, re.DOTALL)
errors = [e.strip().strip("'") for e in errors]

counter = Counter(errors)

for k, v in counter.most_common(30):
    print(f"{v:4} : {k}")
