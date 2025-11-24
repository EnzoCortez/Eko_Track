from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import flash, redirect, url_for
from wtforms import ValidationError

class MyAdminIndexView(AdminIndexView):
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
