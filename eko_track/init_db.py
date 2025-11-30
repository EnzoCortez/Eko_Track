from app import app, db, User, ReportCategory, MunicipalitySettings
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.create_all()
        print('Tablas creadas.')
        if not MunicipalitySettings.query.first():
            db.session.add(MunicipalitySettings(total_budget=50000.0))
        if not ReportCategory.query.first():
            categories = [
                ReportCategory(name='Residuos', base_priority=8),
                ReportCategory(name='Agua', base_priority=10),
                ReportCategory(name='Aire', base_priority=7),
                ReportCategory(name='Ruido', base_priority=4)
            ]
            db.session.add_all(categories)
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin', method='scrypt')
            admin_user = User(username='admin', password=hashed_pw, is_admin=True)
            db.session.add(admin_user)
        db.session.commit()
        print('Inicialización completada.')

if __name__ == '__main__':
    init_db()
