import os
files = []
for root, _, fs in os.walk('src'):
    for f in sorted(fs):
        if f.endswith('.npk') and f != 'all.npk':
            rel = os.path.relpath(os.path.join(root, f), 'src')
            files.append(f'use "{rel}".*;')
            
with open('src/all.npk', 'w') as f:
    f.write('\n'.join(files) + '\n')
