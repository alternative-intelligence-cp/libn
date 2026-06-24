import os
import re

def fix_comments_in_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    changed = False
    for i in range(len(lines)):
        line = lines[i]
        comment_idx = line.find('//')
        if comment_idx != -1:
            # We only fix things after the comment
            pre_comment = line[:comment_idx]
            comment = line[comment_idx:]
            
            # Pattern: @cast_unchecked<X>(Y) -> X Y (or maybe just X depending on if Y is punctuation)
            # Actually, let's just replace @cast_unchecked<([^>]+)>\(([^)]+)\) with \1 \2
            # Wait, if X="an" and Y="but", it becomes "an but"?
            # Let's look at examples: @cast_unchecked<an>(character) -> an character? Or maybe the original was an(character)?
            # What if we just remove the @cast_unchecked<X> and the parentheses around Y?
            # So @cast_unchecked<X>(Y) -> X Y
            # Or if it's @cast_unchecked<X> just remove it?
            
            # Let's replace @cast_unchecked<([^>]+)>\(([^)]+)\) with \1 \2 for now
            new_comment = re.sub(r'@cast_unchecked<([^>]+)>\(([^)]+)\)', r'\1 \2', comment)
            
            # Also just @cast_unchecked<([^>]+)> without parens?
            # e.g. @cast_unchecked<int64> in comments. Sometimes it's a real code reference.
            # But wait, if X is an, a, the, we should remove them?
            
            if new_comment != comment:
                lines[i] = pre_comment + new_comment
                changed = True

    if changed:
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print(f"Fixed {filepath}")

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_comments_in_file(os.path.join(root, f))
