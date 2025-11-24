import unittest
from unittest.mock import MagicMock
from wtforms import ValidationError
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from admin_config import ReportView, MunicipalitySettingsView
from models import Report, MunicipalitySettings

class TestAdminValidation(unittest.TestCase):
    def test_report_negative_cost(self):
        model = Report()
        model.estimated_cost = -10
        
        print("Testing Negative Cost Validation...")
        with self.assertRaises(ValidationError) as cm:
            # Call method directly on the class, passing None as self
            ReportView.on_model_change(None, None, model, True)
        self.assertEqual(str(cm.exception), 'El costo estimado no puede ser negativo.')
        print("PASS: Negative cost raised ValidationError")

    def test_report_excessive_cost(self):
        model = Report()
        model.estimated_cost = 1000001
        
        print("Testing Excessive Cost Validation...")
        with self.assertRaises(ValidationError) as cm:
            ReportView.on_model_change(None, None, model, True)
        self.assertEqual(str(cm.exception), 'El costo excede el límite permitido para aprobación automática (1,000,000).')
        print("PASS: Excessive cost raised ValidationError")

    def test_report_valid_cost(self):
        model = Report()
        model.estimated_cost = 500
        
        print("Testing Valid Cost...")
        try:
            ReportView.on_model_change(None, None, model, True)
            print("PASS: Valid cost did not raise ValidationError")
        except ValidationError:
            self.fail("Valid cost raised ValidationError unexpectedly!")

    def test_municipality_negative_budget(self):
        model = MunicipalitySettings()
        model.total_budget = -500
        
        print("Testing Negative Budget Validation...")
        with self.assertRaises(ValidationError) as cm:
            MunicipalitySettingsView.on_model_change(None, None, model, True)
        self.assertEqual(str(cm.exception), 'El presupuesto municipal no puede ser negativo.')
        print("PASS: Negative budget raised ValidationError")

if __name__ == '__main__':
    unittest.main()
