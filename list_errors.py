import re, os
with open('clean_errors.txt') as f:
    clean_lines = [l.strip() for l in f.readlines()]
for clean in clean_lines:
    if 'error:' not in clean: continue
    m = re.search(r'Line (\d+), Column \d+: (.*)', clean)
    if not m: continue
    line = int(m.group(1))
    msg = m.group(2)
    print(f"--- Line {line}: {msg}")
    for root, _, fnames in os.walk('src'):
        for fname in fnames:
            if fname.endswith('.npk'):
                filepath = os.path.join(root, fname)
                with open(filepath) as f2:
                    flines = f2.readlines()
                if line <= len(flines):
                    text = flines[line-1].strip()
                    # only print if it looks suspicious
                    if "Cannot silently unwrap Result" in msg:
                        m_var = re.search(r"into '([^']+)'", msg)
                        if m_var and m_var.group(1) in text and '=' in text:
                            print(f"{filepath}:{line} -> {text}")
                    elif "bool" in msg or "Logical" in msg or "compare" in msg:
                        if ('==' in text or '!=' in text or '&&' in text or '||' in text or '!' in text or '<' in text or '>' in text or 'if' in text or 'while' in text):
                            print(f"{filepath}:{line} -> {text}")
                    elif "Member access (.) requires struct" in msg:
                        if '.' in text:
                            print(f"{filepath}:{line} -> {text}")
                    elif "Argument" in msg:
                        print(f"{filepath}:{line} -> {text}")
