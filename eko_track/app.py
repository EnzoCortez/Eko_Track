import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash

# Import models and admin
from models import db, User, Report, ReportCategory, MunicipalitySettings, PriorityBudgetMatrix
from admin_config import MyAdminIndexView, ReportView, MunicipalitySettingsView, UserView, SecureModelView, PriorityBudgetMatrixView

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'eko_track_secret_key_123')

# Database Configuration: Use DATABASE_URL if available (Render), else local SQLite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///eko_track_v2.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin Setup
from flask_admin.menu import MenuLink
admin = Admin(app, name='Eko Track Admin', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(ReportView(Report, db.session))
admin.add_view(SecureModelView(ReportCategory, db.session))
admin.add_view(MunicipalitySettingsView(MunicipalitySettings, db.session))
admin.add_view(PriorityBudgetMatrixView(PriorityBudgetMatrix, db.session, name='Budget Matrices'))

# Add Navigation Links
admin.add_link(MenuLink(name='Main Menu', category='', url='/'))
admin.add_link(MenuLink(name='Logout', category='', url='/logout'))

@app.route('/')
def index():
    """
    Main Dashboard.
    - If authenticated: Shows reports and suggested interventions.
    - If unauthenticated: Redirects to login.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Logic for "Suggested Interventions"
    # 1. Get total budget
    settings = MunicipalitySettings.query.first()
    total_budget = settings.total_budget if settings else 0.0
    
    # 2. Get all pending reports
    reports = Report.query.filter_by(status='Pendiente').all()
    
    # 3. Sort by priority (Criticality * Category Priority)
    # We do this in python for simplicity, could be SQL
    reports.sort(key=lambda x: x.calculate_priority_score(), reverse=True)
    
    # 4. Determine which can be funded based on suggested budgets from matrix
    suggested_interventions = []
    current_spend = 0.0
    
    for r in reports:
        suggested_budget = r.get_suggested_budget()
        if current_spend + suggested_budget <= total_budget:
            suggested_interventions.append(r)
            current_spend += suggested_budget
            
    return render_template('index.html', 
                           reports=reports, 
                           suggested=suggested_interventions, 
                           budget=total_budget, 
                           spent=current_spend)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            # Role-based redirection
            if user.is_admin:
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Login Failed. Check details.')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password=hashed_pw)
        
        # First user is admin for demo purposes
        if User.query.count() == 0:
            new_user.is_admin = True
            
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/report', methods=['GET', 'POST'])
@login_required
def create_report():
    """
    Create a new report.
    Requires authentication.
    """
    categories = ReportCategory.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        crit = request.form.get('criticality')
        cat_id = request.form.get('category')
        location = request.form.get('location') # New Location Field
        
        new_report = Report(
            title=title,
            description=desc,
            criticality=crit,
            category_id=cat_id,
            location=location,
            user_id=current_user.id,
            status='Pendiente'
        )
        db.session.add(new_report)
        db.session.commit()
        flash('Reporte creado exitosamente!')
        return redirect(url_for('index'))
        
    # Pass Quito Sectors to template

    sectors = Report.QUITO_SECTORS
    
    return render_template('create_report.html', categories=categories, sectors=sectors)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default settings if not exists
        if not MunicipalitySettings.query.first():
            db.session.add(MunicipalitySettings(total_budget=50000.0))
            db.session.commit()
            
        # Create default categories
        if not ReportCategory.query.first():
            db.session.add(ReportCategory(name='Residuos', base_priority=8))
            db.session.add(ReportCategory(name='Agua', base_priority=10))
            db.session.add(ReportCategory(name='Aire', base_priority=7))
            db.session.add(ReportCategory(name='Ruido', base_priority=4))
            db.session.commit()
            
        # Create default priority-budget matrices for each category
        if not PriorityBudgetMatrix.query.first():
            categories = ReportCategory.query.all()
            
            # Budget allocations per category and priority level
            budget_config = {
                'Agua': {'Bajo': 500, 'Medio': 1000, 'Alto': 2000},
                'Residuos': {'Bajo': 300, 'Medio': 700, 'Alto': 1500},
                'Aire': {'Bajo': 400, 'Medio': 900, 'Alto': 1800},
                'Ruido': {'Bajo': 200, 'Medio': 500, 'Alto': 1000}
            }
            
            for cat in categories:
                if cat.name in budget_config:
                    for priority, budget in budget_config[cat.name].items():
                        matrix = PriorityBudgetMatrix(
                            category_id=cat.id,
                            priority_level=priority,
                            budget_amount=budget
                        )
                        db.session.add(matrix)
            
            db.session.commit()

        # Create default admin user
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin', method='scrypt')
            admin_user = User(username='admin', password=hashed_pw, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
            pass
            
    app.run()
