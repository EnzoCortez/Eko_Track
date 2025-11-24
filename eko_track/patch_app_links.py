import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if "from flask_admin.menu import MenuLink" not in content:
    content = content.replace("# Admin Setup", "# Admin Setup\nfrom flask_admin.menu import MenuLink")

# Add links
target = "admin.add_view(MunicipalitySettingsView(MunicipalitySettings, db.session))"
replacement = """admin.add_view(MunicipalitySettingsView(MunicipalitySettings, db.session))

# Add Navigation Links
admin.add_link(MenuLink(name='Main Menu', category='', url='/'))
admin.add_link(MenuLink(name='Logout', category='', url='/logout'))"""

content = content.replace(target, replacement)

# Update Admin init to use bootstrap3
content = content.replace("index_view=MyAdminIndexView())", "index_view=MyAdminIndexView(), template_mode='bootstrap3'")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
