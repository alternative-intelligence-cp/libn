import os
import re

allocators = ['mem_malloc', 'mem_calloc', 'mem_realloc', 'libn_slab_alloc', 'libn_slab_alloc_zero', 'libn_slab_realloc']

def fix_signatures(path):
    with open(path, 'r') as f:
        content = f.read()

    for alloc in allocators:
        content = content.replace(f'pub func:{alloc} = int64', f'pub func:{alloc} = Result<int64>')
        # Also fix forward declarations if any
        content = content.replace(f'func:{alloc} = int64', f'func:{alloc} = Result<int64>')

    # Fix error propagation: replace `if (r.is_error) { pass 0i64; } pass r.value;` with `pass r;`
    content = re.sub(r'if \(r\.is_error\) \{\s*pass 0i64;\s*\}\s*pass r\.value;', r'pass r;', content)
    content = re.sub(r'if \(new_r\.is_error\) \{\s*pass 0i64;\s*\}\s*pass new_r\.value;', r'pass new_r;', content)
    
    # Also replace `pass r.value;` with `pass r;` if there are leftovers
    content = content.replace('pass r.value;', 'pass r;')
    content = content.replace('return r.value;', 'return r;')
    content = content.replace('pass new_r.value;', 'pass new_r;')
    content = content.replace('return new_r.value;', 'return new_r;')
    
    with open(path, 'w') as f:
        f.write(content)

def add_raw_to_calls():
    for root, dirs, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
        for file in files:
            if not file.endswith('.npk'): continue
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = content
            for alloc in allocators:
                # Add raw if not present
                # (?<!raw\s)   -> not preceded by 'raw ' or 'raw\t'
                # (?<!func:)   -> not preceded by 'func:'
                # (?<!pub\s)   -> not preceded by 'pub ' (just in case)
                # (?<!Result<int64>\() -> not preceded by 'Result<int64>(' (in definitions)
                # We also want to skip 'pass mem_malloc' in bio_alloc_buf and explicitly change it to 'pass raw mem_malloc'
                pattern = r'(?<!raw )(?<!raw\t)(?<!func:)(?<!pub func:)\b' + alloc + r'\s*\('
                new_content = re.sub(pattern, 'raw ' + alloc + '(', new_content)
                
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)

fix_signatures('/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk')
fix_signatures('/home/randy/Workspace/REPOS/libn/src/mem/slab.npk')

# Run raw adder
add_raw_to_calls()


def remove_raw_inside_allocators():
    paths = ['/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk', '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk']
    for path in paths:
        with open(path, 'r') as f:
            content = f.read()
        for alloc in allocators:
            content = content.replace(f'raw {alloc}(', f'{alloc}(')
        with open(path, 'w') as f:
            f.write(content)

remove_raw_inside_allocators()
