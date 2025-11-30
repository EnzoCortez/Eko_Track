"""
Test script to verify that suggested budgets are working correctly
Creates sample reports and verifies calculations
"""

from app import app, db
from models import Report, ReportCategory, User

def test_suggested_budgets():
    with app.app_context():
        print("=" * 60)
        print("TEST: Suggested Budget Calculation")
        print("=" * 60)
        
        # Get categories
        agua = ReportCategory.query.filter_by(name='Agua').first()
        residuos = ReportCategory.query.filter_by(name='Residuos').first()
        
        # Get a user
        user = User.query.first()
        
        if not user or not agua or not residuos:
            print("[ERROR] Database not initialized. Run recreate_database.py first.")
            return
        
        print("\n[Test 1] Creating sample reports...")
        
        # Create test reports
        test_reports = [
            {
                'title': 'Agua - Alta Prioridad',
                'description': 'Problema de agua crítico',
                'criticality': 'Alto',
                'category': agua,
                'expected_budget': 2000
            },
            {
                'title': 'Agua - Media Prioridad',
                'description': 'Problema de agua moderado',
                'criticality': 'Medio',
                'category': agua,
                'expected_budget': 1000
            },
            {
                'title': 'Agua - Baja Prioridad',
                'description': 'Problema de agua menor',
                'criticality': 'Bajo',
                'category': agua,
                'expected_budget': 500
            },
            {
                'title': 'Residuos - Alta Prioridad',
                'description': 'Problema de residuos crítico',
                'criticality': 'Alto',
                'category': residuos,
                'expected_budget': 1500
            }
        ]
        
        created_reports = []
        for test in test_reports:
            report = Report(
                title=test['title'],
                description=test['description'],
                criticality=test['criticality'],
                category_id=test['category'].id,
                location='Norte',
                estimated_cost=100,  # Small estimated cost
                user_id=user.id,
                status='Pendiente'
            )
            db.session.add(report)
            created_reports.append((report, test['expected_budget']))
        
        db.session.commit()
        print(f"  Created {len(test_reports)} test reports")
        
        print("\n[Test 2] Verifying suggested budgets...")
        all_passed = True
        
        for report, expected in created_reports:
            suggested = report.get_suggested_budget()
            status = "[PASS]" if suggested == expected else "[FAIL]"
            
            if suggested != expected:
                all_passed = False
            
            print(f"  {status} {report.title}")
            print(f"    Category: {report.category.name} | Criticality: {report.criticality}")
            print(f"    Expected: ${expected} | Got: ${suggested}")
        
        print("\n[Test 3] Verifying priority scores...")
        for report, _ in created_reports:
            score = report.calculate_priority_score()
            print(f"  {report.title}: Priority Score = {score}")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("[SUCCESS] All tests passed!")
        else:
            print("[FAILURE] Some tests failed")
        print("=" * 60)
        
        # Clean up
        print("\nCleaning up test reports...")
        for report, _ in created_reports:
            db.session.delete(report)
        db.session.commit()
        print("  [DONE] Test reports deleted\n")

if __name__ == '__main__':
    test_suggested_budgets()
