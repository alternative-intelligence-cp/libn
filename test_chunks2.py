import json
path = '/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json'
with open(path, 'r') as f:
    chunks = json.load(f)
k = '/home/randy/Workspace/REPOS/libn/src/fs/path.npk'
print(chunks[k][0].keys())
print(chunks[k][0]['target'])
print("---")
print(chunks[k][0]['replacement'])
