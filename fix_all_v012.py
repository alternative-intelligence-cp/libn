import glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    # 1. Functions end with };
    text = re.sub(r'^\}$', r'};', text, flags=re.MULTILINE)

    lines = text.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        
        # Strip comments for checking
        code_part = line
        comment_idx = line.find('//')
        if comment_idx != -1:
            code_part = line[:comment_idx]
            comment_part = line[comment_idx:]
        else:
            comment_part = ""

        # 2. `as type` to `@cast_unchecked<type>` ONLY in code part
        code_part = re.sub(r'\b([a-zA-Z0-9_\.]+(?:\[[^\]]+\])?)\s+as\s+([a-zA-Z0-9_\*]+)\b', r'@cast_unchecked<\2>(\1)', code_part)
        code_part = re.sub(r'\(([^\)]+)\)\s+as\s+([a-zA-Z0-9_\*]+)\b', r'@cast_unchecked<\2>(\1)', code_part)

        # 3. Add parens to if/while
        # We need to match `if cond {` even if there's stuff after `{`
        m_if = re.match(r'^(\s*)(\}?\s*else\s+)?if\s+(.+?)\s*\{(.*)$', code_part)
        if m_if:
            prefix = m_if.group(1) or ""
            else_part = m_if.group(2) or ""
            cond = m_if.group(3).strip()
            rest = m_if.group(4) or ""
            if not (cond.startswith('(') and cond.endswith(')') and cond.count('(') == cond.count(')')):
                cond = f"({cond})"
            code_part = f"{prefix}{else_part}if {cond} {{{rest}"

        m_while = re.match(r'^(\s*)while\s+(.+?)\s*\{(.*)$', code_part)
        if m_while:
            prefix = m_while.group(1) or ""
            cond = m_while.group(2).strip()
            rest = m_while.group(3) or ""
            if not (cond.startswith('(') and cond.endswith(')') and cond.count('(') == cond.count(')')):
                cond = f"({cond})"
            code_part = f"{prefix}while {cond} {{{rest}"

        lines[i] = code_part + comment_part

    text = '\n'.join(lines)

    # 4. Keyword replacement
    # 'end' is a keyword! Replace variable 'end' with 'end_idx'
    # We must be careful to only match standalone 'end'
    text = re.sub(r'\bend\b', 'end_idx', text)

    # test_all.npk pass to exit
    if 'test_all.npk' in file:
        pass # Handle below

    with open(file, 'w') as f:
        f.write(text)

with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('pass 0i32;', 'exit 0i32;')
text = text.replace('pass 0i64;', 'exit 0i32;')
with open('test_all.npk', 'w') as f:
    f.write(text)

