import unittest
import sys
import os
from flask import url_for

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Report, ReportCategory, MunicipalitySettings

class TestEkoTrackRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        
        # Setup initial data
        self.user = User(username='testuser', password='scrypt:32768:8:1$test$hash') # Mock hash
        db.session.add(self.user)
        
        self.category = ReportCategory(name='TestCat', base_priority=5)
        db.session.add(self.category)
        
        self.settings = MunicipalitySettings(total_budget=1000.0)
        db.session.add(self.settings)
        
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self):
        # We need to create a user with a known password to login properly
        # Or we can mock the login_user. 
        # But let's try to use the login route if we can hash the password correctly.
        # Actually, simpler to just mock the session or use flask_login.login_user in a request context?
        # No, let's just use the login route.
        # We need to generate a real hash for the password "password"
        from werkzeug.security import generate_password_hash
        user = User.query.get(1)
        user.password = generate_password_hash('password', method='scrypt')
        db.session.commit()
        
        return self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)

    def test_create_report(self):
        self.login()
        response = self.app.post('/report', data=dict(
            title='Test Report',
            description='Test Description',
            criticality='Alto',
            category=self.category.id
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte creado exitosamente!', response.data)
        
        report = Report.query.first()
        self.assertIsNotNone(report)
        self.assertEqual(report.title, 'Test Report')
        self.assertEqual(report.criticality, 'Alto')

    def test_prioritization_logic(self):
        # Create reports with different priorities
        # Report 1: High Criticality (3) * Base Priority (5) = 15
        r1 = Report(title='R1', description='D1', criticality='Alto', category_id=self.category.id, user_id=1, estimated_cost=100, status='Pendiente')
        
        # Create another category with higher priority
        cat2 = ReportCategory(name='HighPrio', base_priority=10)
        db.session.add(cat2)
        db.session.commit()
        
        # Report 2: Medium Criticality (2) * HighPrio (10) = 20
        r2 = Report(title='R2', description='D2', criticality='Medio', category_id=cat2.id, user_id=1, estimated_cost=100, status='Pendiente')
        
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        
        # Check prioritization score
        # Alto=3, Medio=2, Bajo=1
        self.assertEqual(r1.calculate_priority_score(), 3 * 5)
        self.assertEqual(r2.calculate_priority_score(), 2 * 10)
        
        # R2 (20) should be higher than R1 (15)
        self.assertTrue(r2.calculate_priority_score() > r1.calculate_priority_score())

if __name__ == '__main__':
    unittest.main()
