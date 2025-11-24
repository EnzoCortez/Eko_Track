with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = ", template_mode='bootstrap3')"
replacement = ")"

content = content.replace(target, replacement)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
