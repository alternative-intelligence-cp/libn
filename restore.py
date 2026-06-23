import json
import os

with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as fp:
    chunks = json.load(fp)

# The keys are something like: '39_errno.npk' or 'src/syscall/errno.npk'?
# Let's see what keys it has!
print(list(chunks.keys())[:5])
