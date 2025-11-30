"""
Verification script to test priority-budget matrix functionality
"""

from app import app, db
from models import Report, ReportCategory, PriorityBudgetMatrix

def verify_matrices():
    with app.app_context():
        print("=" * 60)
        print("VERIFICATION: Priority-Budget Matrix System")
        print("=" * 60)
        
        # Test 1: Verify all matrices exist
        print("\n[Test 1] Checking Priority-Budget Matrices...")
        matrices = PriorityBudgetMatrix.query.all()
        print(f"Total matrices found: {len(matrices)}")
        
        categories = ReportCategory.query.all()
        for cat in categories:
            print(f"\n  Category: {cat.name}")
            cat_matrices = PriorityBudgetMatrix.query.filter_by(category_id=cat.id).all()
            for matrix in cat_matrices:
                print(f"    {matrix.priority_level}: ${matrix.budget_amount}")
        
        # Test 2: Test budget lookup method
        print("\n\n[Test 2] Testing Budget Lookup Methods...")
        agua_cat = ReportCategory.query.filter_by(name='Agua').first()
        if agua_cat:
            print(f"  Category: {agua_cat.name}")
            print(f"    Bajo budget: ${agua_cat.get_budget_for_priority('Bajo')}")
            print(f"    Medio budget: ${agua_cat.get_budget_for_priority('Medio')}")
            print(f"    Alto budget: ${agua_cat.get_budget_for_priority('Alto')}")
        
        # Test 3: Test suggested budget on reports
        print("\n\n[Test 3] Testing Suggested Budget on Sample Reports...")
        reports = Report.query.limit(5).all()
        if reports:
            for report in reports:
                suggested = report.get_suggested_budget()
                print(f"  Report: {report.title}")
                print(f"    Category: {report.category.name}")
                print(f"    Criticality: {report.criticality}")
                print(f"    Suggested Budget: ${suggested}")
                print(f"    Priority Score: {report.calculate_priority_score()}")
                print()
        else:
            print("  No reports found. Create some reports to test this feature.")
        
        # Test 4: Verify recommendation system integration
        print("\n[Test 4] Testing Recommendation System...")
        pending_reports = Report.query.filter_by(status='Pendiente').all()
        print(f"  Total pending reports: {len(pending_reports)}")
        
        if pending_reports:
            # Sort by priority score
            pending_reports.sort(key=lambda x: x.calculate_priority_score(), reverse=True)
            print("\n  Top 5 Recommended Reports (by priority):")
            for i, report in enumerate(pending_reports[:5], 1):
                print(f"    {i}. {report.title}")
                print(f"       Category: {report.category.name} | Criticality: {report.criticality}")
                print(f"       Priority Score: {report.calculate_priority_score()}")
                print(f"       Suggested Budget: ${report.get_suggested_budget()}")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All verification tests completed!")
        print("=" * 60)

if __name__ == '__main__':
    verify_matrices()
