from app import app, db
from models import Report, User, ReportCategory

def verify_assignment():
    with app.test_client() as client:
        with app.app_context():
            # Setup
            db.create_all()
            
            # Ensure admin exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Admin user not found!")
                return

            # Ensure category exists
            cat = ReportCategory.query.first()
            
            # Create Report
            report = Report(title='Budget Test', description='desc', criticality='Alto', category_id=cat.id, user_id=admin.id, estimated_cost=100)
            db.session.add(report)
            db.session.commit()
            report_id = report.id
            
            print(f"Created Report ID: {report_id}, Initial Budget: {report.allocated_budget}")

        # Login
        client.post('/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
        
        # Assign Budget via POST
        response = client.post('/admin/', data={
            'report_id': report_id,
            'allocated_amount': 500.0
        }, follow_redirects=True)
        
        if response.status_code == 200:
            print("POST request successful.")
        else:
            print(f"POST request failed: {response.status_code}")

        # Verify DB
        with app.app_context():
            updated_report = Report.query.get(report_id)
            if updated_report.allocated_budget == 500.0:
                print(f"SUCCESS: Budget updated to {updated_report.allocated_budget}")
            else:
                print(f"FAILURE: Budget is {updated_report.allocated_budget} (Expected 500.0)")

if __name__ == '__main__':
    verify_assignment()
