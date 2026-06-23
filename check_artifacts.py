import json

path = '/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json'
with open(path, 'r') as f:
    chunks = json.load(f)

for c in chunks:
    if 'strchr.npk' in c['path']:
        lines = c['content'].split('\n')
        print("strchr.npk from all_chunks.json:")
        for i in range(50, 60):
            print(f"{i+1}: {lines[i]}")
        break
