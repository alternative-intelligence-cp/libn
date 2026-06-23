import os
import re

# We will read all .npk files into a list of lines.
files_lines = {}
for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                files_lines[path] = f.readlines()

# Read the error lines
lines_to_find = [309, 326, 343, 362, 381]
for line_num in lines_to_find:
    print(f"--- Line {line_num} ---")
    for path, lines in files_lines.items():
        if len(lines) >= line_num:
            line_content = lines[line_num - 1].strip()
            # If the line looks like an assignment, print it
            if "=" in line_content and ("int64:" in line_content or line_content.startswith("r =")):
                print(f"{path}:{line_num}: {line_content}")

