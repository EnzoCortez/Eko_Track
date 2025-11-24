import re

with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """    # Estimated cost to fix this issue
    estimated_cost = db.Column(db.Float, default=0.0)"""

replacement = """    # Estimated cost to fix this issue
    estimated_cost = db.Column(db.Float, default=0.0)
    
    # Budget allocated by Admin
    allocated_budget = db.Column(db.Float, default=0.0)"""

content = content.replace(target, replacement)

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)
