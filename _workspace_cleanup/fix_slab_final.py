with open("src/mem/slab.npk", "r") as f:
    content = f.read()

content = content.replace("if i ==", "if (i ==")
content = content.replace("{ pass", ") { pass")
content = content.replace("else if (i ==", "else if (i ==")  # Wait, the replace of "{ pass" might affect other things.
# It's better to just write a simple regex or string replace.
