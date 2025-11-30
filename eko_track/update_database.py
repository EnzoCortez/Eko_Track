"""
Script to update the database with the new PriorityBudgetMatrix model
and populate default values for existing categories.
"""

from app import app, db
from models import ReportCategory, PriorityBudgetMatrix

def update_database():
    with app.app_context():
        print("Creating new tables...")
        db.create_all()
        
        print("Checking for existing priority-budget matrices...")
        if PriorityBudgetMatrix.query.first():
            print("Priority-budget matrices already exist. Skipping initialization.")
            return
        
        print("Creating default priority-budget matrices...")
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
                print(f"Creating matrices for category: {cat.name}")
                for priority, budget in budget_config[cat.name].items():
                    matrix = PriorityBudgetMatrix(
                        category_id=cat.id,
                        priority_level=priority,
                        budget_amount=budget
                    )
                    db.session.add(matrix)
                    print(f"  - {priority}: ${budget}")
        
        db.session.commit()
        print("\n[SUCCESS] Database updated successfully!")
        print("\nPriority-Budget Matrices Created:")
        
        # Display all matrices
        all_matrices = PriorityBudgetMatrix.query.all()
        for matrix in all_matrices:
            print(f"  {matrix}")

if __name__ == '__main__':
    update_database()
