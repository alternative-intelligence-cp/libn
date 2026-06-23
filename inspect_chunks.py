import json

path = '/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json'
with open(path, 'r') as f:
    chunks = json.load(f)

if isinstance(chunks, dict):
    print("It's a dict!")
    for k in list(chunks.keys())[:5]:
        print(k)
        if isinstance(chunks[k], str):
            print(f"Value is string of length {len(chunks[k])}")
        else:
            print(f"Value is {type(chunks[k])}")
elif isinstance(chunks, list):
    print("It's a list!")
    print(type(chunks[0]))
