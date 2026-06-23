import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # Fix Result<int64> in function definitions to int64
    content = re.sub(r'(pub func:\w+\s*=\s*)Result<int64>(\([^)]*\)\s*\{)', r'\1int64\2', content)
    content = re.sub(r'(func:\w+\s*=\s*)Result<int64>(\([^)]*\)\s*\{)', r'\1int64\2', content)

    # Fix Result<NIL> to NIL
    content = re.sub(r'(pub func:\w+\s*=\s*)Result<NIL>(\([^)]*\)\s*\{)', r'\1NIL\2', content)
    content = re.sub(r'(func:\w+\s*=\s*)Result<NIL>(\([^)]*\)\s*\{)', r'\1NIL\2', content)

    # Fix if / while conditions missing parens
    # e.g., if err { -> if (err) {
    # Match `if X {` where X doesn't start with `(`
    content = re.sub(r'\bif\s+(?!\()([^\{]+?)\s*\{', r'if (\1) {', content)
    content = re.sub(r'\bwhile\s+(?!\()([^\{]+?)\s*\{', r'while (\1) {', content)
    # Fix `if (condition)  {` cases where trailing spaces cause issues (the regex above handles most)

    # Fix missing semicolons on functions and structs
    # Match `}` at the start of a line preceded by code, but we just replace all `^}$` with `};`
    # However, this might break `if` statements. So we only do it for functions/structs.
    # Actually, we can use a more intelligent approach: 
    # Just replace `^}$` with `};` EXCEPT if it's an if/while block? No, Nitpick requires `;` on functions, structs, traits. 
    # Let's just find `}` at the end of a block that was opened by a function or struct.
    # The simpler way: run `sed` or regex. In Nitpick v0.x, ALL declarations need `};` but `if`/`while` don't... Wait, Nitpick's parser specifically complains about `pub func: ... { ... }` missing `;`.
    # Let's replace `^}$` with `};` for now, then fix if/while? 
    # No, Nitpick requires `};` for EVERYTHING at the statement level except if/while.
    # Actually, the parse errors specifically say: "Functions end with '};'"
    lines = content.split('\n')
    inside_decl = False
    brace_depth = 0
    for i in range(len(lines)):
        line = lines[i]
        
        # Track braces
        if '{' in line:
            if brace_depth == 0 and ('func:' in line or 'struct ' in line):
                inside_decl = True
            brace_depth += line.count('{')
            
        if '}' in line:
            brace_depth -= line.count('}')
            if brace_depth == 0 and inside_decl:
                # Close of a declaration block
                if not ';' in line.split('}')[-1]:
                    lines[i] = line.replace('}', '};')
                inside_decl = False

    content = '\n'.join(lines)

    # Re-apply some formatting fixes for specific files
    if 'syscall.npk' in filepath:
        # Array declarations int64[] -> int64[1] etc.? 
        pass

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")

def main():
    repo_dir = "/home/randy/Workspace/REPOS/libn"
    for root, _, files in os.walk(repo_dir):
        if 'nitpick' in root: continue
        for file in files:
            if file.endswith(".npk"):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
