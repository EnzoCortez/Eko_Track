import re

with open('admin_config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add imports
if "from flask import request, flash" not in content:
    content = content.replace("from sqlalchemy import func", "from sqlalchemy import func\n        from flask import request, flash")

# 2. Add POST handling
target_post = """        # 1. Criticality Matrix Data"""
replacement_post = """        # Handle Budget Assignment POST
        if request.method == 'POST':
            try:
                report_id = request.form.get('report_id')
                allocated_amount = float(request.form.get('allocated_amount', 0))
                
                report = Report.query.get(report_id)
                if report:
                    report.allocated_budget = allocated_amount
                    db.session.commit()
                    flash(f'Presupuesto asignado a reporte {report.title}: ${allocated_amount}', 'success')
                else:
                    flash('Reporte no encontrado.', 'error')
            except ValueError:
                flash('Valor de presupuesto inválido.', 'error')
            except Exception as e:
                flash(f'Error al asignar presupuesto: {str(e)}', 'error')

        # 1. Criticality Matrix Data"""

content = content.replace(target_post, replacement_post)

# 3. Update Budget Suggestions Logic
target_logic = """                budget_suggestions.append({
                    'category': cat_data['category'],
                    'score': cat_data['score'], # Category-level score
                    'cost': r.estimated_cost,
                    'funded': funded
                })"""

replacement_logic = """                # Use allocated budget if set, otherwise estimated cost
                cost_to_use = r.allocated_budget if r.allocated_budget > 0 else r.estimated_cost
                
                if current_spend + cost_to_use <= total_budget:
                    current_spend += cost_to_use
                    funded = True
                
                budget_suggestions.append({
                    'id': r.id,
                    'title': r.title,
                    'category': cat_data['category'],
                    'score': cat_data['score'], # Category-level score
                    'cost': r.estimated_cost,
                    'allocated': r.allocated_budget,
                    'funded': funded
                })"""

# We need to be careful with indentation and exact matching. 
# The previous logic block is:
#                 funded = False
#                 if current_spend + r.estimated_cost <= total_budget:
#                     current_spend += r.estimated_cost
#                     funded = True
#                 
#                 budget_suggestions.append({
#                     'category': cat_data['category'],
#                     'score': cat_data['score'], # Category-level score
#                     'cost': r.estimated_cost,
#                     'funded': funded
#                 })

# Let's replace the whole inner loop block to be safe
target_loop = """            for r in cat_reports:
                funded = False
                if current_spend + r.estimated_cost <= total_budget:
                    current_spend += r.estimated_cost
                    funded = True
                
                budget_suggestions.append({
                    'category': cat_data['category'],
                    'score': cat_data['score'], # Category-level score
                    'cost': r.estimated_cost,
                    'funded': funded
                })"""

replacement_loop = """            for r in cat_reports:
                funded = False
                # Use allocated budget if set, otherwise estimated cost
                cost_to_use = r.allocated_budget if r.allocated_budget > 0 else r.estimated_cost
                
                if current_spend + cost_to_use <= total_budget:
                    current_spend += cost_to_use
                    funded = True
                
                budget_suggestions.append({
                    'id': r.id,
                    'title': r.title,
                    'category': cat_data['category'],
                    'score': cat_data['score'], # Category-level score
                    'cost': r.estimated_cost,
                    'allocated': r.allocated_budget,
                    'funded': funded
                })"""

content = content.replace(target_loop, replacement_loop)

# 4. Update @expose decorator
content = content.replace("@expose('/')", "@expose('/', methods=('GET', 'POST'))")

with open('admin_config.py', 'w', encoding='utf-8') as f:
    f.write(content)
