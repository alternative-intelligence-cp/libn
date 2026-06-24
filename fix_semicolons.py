import re

def add_semicolon(filepath, func_prefix):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the function blocks and make sure their closing brace has a semicolon.
    # The pattern matches `func:<prefix>... = ... { ... }` where } might not have a semicolon.
    # Because Nitpick code can have nested braces, a simple regex might be tricky if not careful,
    # but `strbuf_appendf*` and `asprintf*` are relatively simple and their last line is `}` or `};`.
    
    # Actually, a safer way is to find the function signature, then find the matching closing brace.
    # Let's write a robust brace matcher.
    
    def fix_brace(content, func_name):
        idx = content.find(f"pub func:{func_name}")
        if idx == -1:
            return content
        
        # Find the first '{' after idx
        start_brace = content.find('{', idx)
        if start_brace == -1:
            return content
            
        brace_count = 0
        in_string = False
        i = start_brace
        while i < len(content):
            char = content[i]
            if char == '"' and content[i-1] != '\\':
                in_string = not in_string
            
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found the closing brace
                        if i + 1 < len(content) and content[i+1] != ';':
                            content = content[:i+1] + ';' + content[i+1:]
                        break
            i += 1
        return content

    for i in range(10): # Covers 0-9
        content = fix_brace(content, f"{func_prefix}{i}")

    with open(filepath, 'w') as f:
        f.write(content)

add_semicolon('src/str/strbuf.npk', 'strbuf_appendf')
add_semicolon('src/io/bio/fprintf.npk', 'asprintf')
print("Semicolons fixed.")
