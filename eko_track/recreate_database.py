"""
Script to recreate the database with all new models including PriorityBudgetMatrix
WARNING: This will delete all existing data!
"""

import os
from app import app, db
from models import User, Report, ReportCategory, MunicipalitySettings, PriorityBudgetMatrix
from werkzeug.security import generate_password_hash

def recreate_database():
    with app.app_context():
        print("=" * 60)
        print("DATABASE RECREATION")
        print("=" * 60)
        print("\nWARNING: This will delete all existing data!")
        
        # Drop all tables
        print("\nDropping all existing tables...")
        db.drop_all()
        print("  [DONE] All tables dropped")
        
        # Create all tables with new schema
        print("\nCreating new tables...")
        db.create_all()
        print("  [DONE] All tables created")
        
        # Create default municipality settings
        print("\nCreating municipality settings...")
        settings = MunicipalitySettings(total_budget=50000.0)
        db.session.add(settings)
        db.session.commit()
        print("  [DONE] Municipality budget set to $50,000")
        
        # Create default categories
        print("\nCreating default categories...")
        categories_data = [
            ('Residuos', 8),
            ('Agua', 10),
            ('Aire', 7),
            ('Ruido', 4)
        ]
        
        for name, priority in categories_data:
            cat = ReportCategory(name=name, base_priority=priority)
            db.session.add(cat)
            print(f"  - {name} (priority: {priority})")
        
        db.session.commit()
        print("  [DONE] Categories created")
        
        # Create priority-budget matrices
        print("\nCreating priority-budget matrices...")
        budget_config = {
            'Agua': {'Bajo': 500, 'Medio': 1000, 'Alto': 2000},
            'Residuos': {'Bajo': 300, 'Medio': 700, 'Alto': 1500},
            'Aire': {'Bajo': 400, 'Medio': 900, 'Alto': 1800},
            'Ruido': {'Bajo': 200, 'Medio': 500, 'Alto': 1000}
        }
        
        categories = ReportCategory.query.all()
        for cat in categories:
            if cat.name in budget_config:
                print(f"  Category: {cat.name}")
                for priority, budget in budget_config[cat.name].items():
                    matrix = PriorityBudgetMatrix(
                        category_id=cat.id,
                        priority_level=priority,
                        budget_amount=budget
                    )
                    db.session.add(matrix)
                    print(f"    {priority}: ${budget}")
        
        db.session.commit()
        print("  [DONE] Matrices created")
        
        # Create default admin user
        print("\nCreating default admin user...")
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin', method='scrypt'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("  [DONE] Admin user created (username: admin, password: admin)")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Database recreated successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("  1. Run the app with: python app.py")
        print("  2. Login with: admin/admin")
        print("  3. Create reports and test the priority-budget system")

if __name__ == '__main__':
    recreate_database()
