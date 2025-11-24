import re

with open('admin_config.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = r"""class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))"""

replacement = r"""class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('login'))
            
        from models import Report, ReportCategory, MunicipalitySettings, db
        from sqlalchemy import func

        # 1. Criticality Matrix Data
        # Query: Category Name, Criticality, Count
        results = db.session.query(
            ReportCategory.name, 
            Report.criticality, 
            func.count(Report.id)
        ).join(Report).filter(Report.status == 'Pendiente').group_by(ReportCategory.name, Report.criticality).all()
        
        # Process into structure for template
        matrix_data = {}
        for cat_name, crit, count in results:
            if cat_name not in matrix_data:
                matrix_data[cat_name] = {'category': cat_name, 'high': 0, 'medium': 0, 'low': 0, 'total': 0}
            
            if crit == 'Alto': matrix_data[cat_name]['high'] = count
            elif crit == 'Medio': matrix_data[cat_name]['medium'] = count
            elif crit == 'Bajo': matrix_data[cat_name]['low'] = count
            matrix_data[cat_name]['total'] += count
            
        matrix_list = list(matrix_data.values())

        # 2. Budget Logic (Prioritized by Category Score * Volume)
        # Category Score = Base Priority * Pending Count
        categories = ReportCategory.query.all()
        cat_scores = []
        
        for cat in categories:
            pending_count = Report.query.filter_by(category_id=cat.id, status='Pendiente').count()
            score = cat.base_priority * pending_count
            cat_scores.append({
                'category': cat.name,
                'score': score,
                'priority': cat.base_priority,
                'count': pending_count,
                'id': cat.id
            })
            
        # Sort by Score Descending
        cat_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Allocate Budget
        settings = MunicipalitySettings.query.first()
        total_budget = settings.total_budget if settings else 0.0
        current_spend = 0.0
        budget_suggestions = []
        
        for cat_data in cat_scores:
            # Get reports for this category, sorted by individual criticality
            cat_reports = Report.query.filter_by(category_id=cat_data['id'], status='Pendiente').all()
            cat_reports.sort(key=lambda x: x.calculate_priority_score(), reverse=True)
            
            for r in cat_reports:
                funded = False
                if current_spend + r.estimated_cost <= total_budget:
                    current_spend += r.estimated_cost
                    funded = True
                
                budget_suggestions.append({
                    'category': cat_data['category'],
                    'score': cat_data['score'], # Category-level score
                    'cost': r.estimated_cost,
                    'funded': funded
                })

        return self.render('admin/index.html', 
                           matrix_data=matrix_list, 
                           budget_suggestions=budget_suggestions,
                           budget=total_budget,
                           spent=current_spend)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))"""

content = content.replace(target, replacement)

with open('admin_config.py', 'w', encoding='utf-8') as f:
    f.write(content)
