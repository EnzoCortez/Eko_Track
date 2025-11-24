from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class ReportCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    base_priority = db.Column(db.Integer, default=1, help_text="1 (Low) to 10 (High)")

    def __repr__(self):
        return self.name

class MunicipalitySettings(db.Model):
    """Singleton to store global settings like Budget"""
    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f"Settings (Budget: {self.total_budget})"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Criticality Levels: High, Medium, Low
    criticality = db.Column(db.String(20), nullable=False, default='Bajo') 
    
    # Estimated cost to fix this issue
    estimated_cost = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='Pendiente') # Pendiente, En Progreso, Resuelto

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reports', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('report_category.id'), nullable=False)
    category = db.relationship('ReportCategory', backref=db.backref('reports', lazy=True))
    # Quito Sectors
    QUITO_SECTORS = [
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
    ]
    
    location = db.Column(db.String(50), nullable=False, default='Norte')


    def calculate_priority_score(self):
        # Simple algorithm: Category Priority * Criticality Multiplier
        crit_map = {'Alto': 3, 'Medio': 2, 'Bajo': 1}
        crit_score = crit_map.get(self.criticality, 1)
        cat_score = self.category.base_priority if self.category else 1
        return crit_score * cat_score

    def __repr__(self):
        return f'<Report {self.title}>'
