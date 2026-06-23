import json
with open('scratch/all_chunks.json', 'r') as f:
    chunks = json.load(f)
for c in chunks:
    if c['path'].endswith('strchr.npk'):
        lines = c['content'].split('\n')
        for i, line in enumerate(lines[50:65]):
            print(f"{i+51}: {line}")
        break
