from app import app, db
from models import Report, ReportCategory, User, MunicipalitySettings

def verify_logic():
    with app.app_context():
        # Setup
        db.create_all()
        
        # Ensure categories exist
        agua = ReportCategory.query.filter_by(name='Agua').first() # Priority 10
        ruido = ReportCategory.query.filter_by(name='Ruido').first() # Priority 4
        
        if not agua or not ruido:
            print("Categories not found!")
            return

        # Create User
        user = User.query.filter_by(username='test_logic').first()
        if not user:
            user = User(username='test_logic', password='password')
            db.session.add(user)
            db.session.commit()

        # Clear existing reports for clean test
        Report.query.delete()
        db.session.commit()

        # Create Reports
        # 1 Agua (Score = 10 * 1 = 10)
        r1 = Report(title='Agua 1', description='desc', criticality='Alto', category_id=agua.id, user_id=user.id, estimated_cost=100)
        db.session.add(r1)
        
        # 3 Ruido (Score = 4 * 3 = 12)
        r2 = Report(title='Ruido 1', description='desc', criticality='Bajo', category_id=ruido.id, user_id=user.id, estimated_cost=100)
        r3 = Report(title='Ruido 2', description='desc', criticality='Bajo', category_id=ruido.id, user_id=user.id, estimated_cost=100)
        r4 = Report(title='Ruido 3', description='desc', criticality='Bajo', category_id=ruido.id, user_id=user.id, estimated_cost=100)
        db.session.add_all([r2, r3, r4])
        db.session.commit()

        # Execute Logic (Copied from admin_config.py)
        categories = ReportCategory.query.all()
        cat_scores = []
        
        for cat in categories:
            pending_count = Report.query.filter_by(category_id=cat.id, status='Pendiente').count()
            score = cat.base_priority * pending_count
            cat_scores.append({
                'category': cat.name,
                'score': score
            })
            
        # Sort by Score Descending
        cat_scores.sort(key=lambda x: x['score'], reverse=True)
        
        print("Sorted Categories:")
        for item in cat_scores:
            if item['score'] > 0:
                print(f"{item['category']}: {item['score']}")

        # Verification
        top_cat = cat_scores[0]['category']
        if top_cat == 'Ruido':
            print("SUCCESS: Ruido is top priority.")
        else:
            print(f"FAILURE: {top_cat} is top priority (Expected Ruido).")

if __name__ == '__main__':
    verify_logic()
