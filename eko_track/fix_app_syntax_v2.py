with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific syntax error
# The error is likely: admin = Admin(app, name='Eko Track Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3'
# It should be: admin = Admin(app, name='Eko Track Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3')

target = "admin = Admin(app, name='Eko Track Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3'"
replacement = "admin = Admin(app, name='Eko Track Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3')"

if target in content and replacement not in content:
    content = content.replace(target, replacement)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
