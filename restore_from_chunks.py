import json
import os

with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as f:
    chunks = json.load(f)

for path, content in chunks.items():
    print(f"Restoring {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write('\n'.join(content))

print("Restored from all_chunks.json!")
