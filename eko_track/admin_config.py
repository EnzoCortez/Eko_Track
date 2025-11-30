from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import flash, redirect, url_for
from wtforms import ValidationError

class MyAdminIndexView(AdminIndexView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('login'))
            
        from models import Report, ReportCategory, MunicipalitySettings, PriorityBudgetMatrix, db
        from sqlalchemy import func
        from flask import request, flash

        # Handle Budget Assignment POST
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
                    'suggested': r.get_suggested_budget(),  # Budget from matrix
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
        return redirect(url_for('login'))

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class ReportView(SecureModelView):
    # Ensure category is a dropdown (Flask-Admin does this by default for relationships, 
    # but we can customize the form columns if needed)
    form_columns = ['title', 'description', 'criticality', 'location', 'estimated_cost', 'status', 'user', 'category']
    
    column_list = ['title', 'criticality', 'location', 'estimated_cost', 'status', 'category', 'priority_score']
    
    def _priority_formatter(view, context, model, name):
        return model.calculate_priority_score()

    column_formatters = {
        'priority_score': _priority_formatter
    }

    form_choices = {
        'criticality': [
            ('Alto', 'Alto'),
            ('Medio', 'Medio'),
            ('Bajo', 'Bajo')
        ],
        'location': [
            ('Norte', 'Norte'),
            ('Centro', 'Centro'),
            ('Sur', 'Sur'),
            ('Valles', 'Valles'),
            ('Calderón', 'Calderón'),
            ('Quitumbe', 'Quitumbe'),
            ('La Delicia', 'La Delicia'),
            ('Eugenio Espejo', 'Eugenio Espejo'),
            ('Manuela Sáenz', 'Manuela Sáenz'),
            ('Eloy Alfaro', 'Eloy Alfaro'),
            ('Tumbaco', 'Tumbaco'),
            ('Los Chillos', 'Los Chillos')
        ],
        'status': [
            ('Pendiente', 'Pendiente'),
            ('En Progreso', 'En Progreso'),
            ('Resuelto', 'Resuelto')
        ]
    }

    # BACKEND VALIDATION FOR SENSITIVE DATA (Budget/Cost)
    def on_model_change(self, form, model, is_created):
        # Validation 1: Cost cannot be negative
        if model.estimated_cost < 0:
            raise ValidationError('El costo estimado no puede ser negativo.')
        
        # Validation 2: Cost cannot exceed a hard limit without special approval (Simulated)
        # This is the "Backend Validation" requested.
        if model.estimated_cost > 1000000:
             raise ValidationError('El costo excede el límite permitido para aprobación automática (1,000,000).')

class MunicipalitySettingsView(SecureModelView):
    def on_model_change(self, form, model, is_created):
        if model.total_budget < 0:
            raise ValidationError('El presupuesto municipal no puede ser negativo.')

class UserView(SecureModelView):
    column_exclude_list = ['password']
    form_columns = ['username', 'password', 'is_admin']

class PriorityBudgetMatrixView(SecureModelView):
    """Admin view for managing priority-budget matrices"""
    form_columns = ['category', 'priority_level', 'budget_amount']
    column_list = ['category', 'priority_level', 'budget_amount']
    
    form_choices = {
        'priority_level': [
            ('Bajo', 'Bajo'),
            ('Medio', 'Medio'),
            ('Alto', 'Alto')
        ]
    }
    
    def on_model_change(self, form, model, is_created):
        # Validation: Budget cannot be negative
        if model.budget_amount < 0:
            raise ValidationError('El presupuesto no puede ser negativo.')

