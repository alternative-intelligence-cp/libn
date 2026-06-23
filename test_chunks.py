import json

with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as fp:
    chunks = json.load(fp)

c = chunks['/home/randy/Workspace/REPOS/libn/src/str/strcmp.npk']
if '@"' in c:
    print("HAS FIXES!")
else:
    print("NO FIXES!")
