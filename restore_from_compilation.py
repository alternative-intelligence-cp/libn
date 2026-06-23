import re, os

md_path = '/home/randy/Workspace/META/LIBN/audits/a18/compilation.md'
with open(md_path, 'r') as f:
    text = f.read()

pattern = r'## ([^\n]+)\n+```npk\n(.*?)\n```'
matches = re.finditer(pattern, text, re.DOTALL)

for match in matches:
    filepath = match.group(1).strip()
    code = match.group(2)
    
    full_path = os.path.join('/home/randy/Workspace/REPOS/libn/src', filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(code + '\n')
    print(f"Restored {filepath}")

