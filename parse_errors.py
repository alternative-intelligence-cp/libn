import re
from collections import Counter

with open("build_errors.txt", "r") as f:
    text = f.read()

# Strip ANSI escape codes
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean_text = ansi_escape.sub('', text)

errors = []
for line in clean_text.split("\n"):
    if "error: Line" in line:
        errors.append(line.split("error:")[1].strip())

c = Counter(errors)
print(f"Total Unique Errors: {len(c)}")
for k, v in c.most_common(20):
    print(f"{v:4} | {k}")
