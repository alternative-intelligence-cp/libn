import os

with open('/home/randy/Workspace/META/LIBN/audits/a34/compilation.md', 'r') as f:
    content = f.read()

parts = content.split('\n# FILE: ')
for part in parts[1:]:
    lines = part.split('\n', 1)
    filepath = lines[0].strip()
    file_content = lines[1] if len(lines) > 1 else ""
    
    # Strip any trailing blank lines if needed, but keeping as is should be fine.
    # The file path usually starts with `src/`.
    
    full_path = os.path.join('/home/randy/Workspace/REPOS/libn', filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(file_content)
    print(f"Restored {filepath}")

