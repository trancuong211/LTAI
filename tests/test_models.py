"""
Test suite for house price prediction models
"""

import unittest
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.evaluate import ModelEvaluator
from models.price_estimator import PriceEstimate, estimate_price, estimate_from_property


class TestModelEvaluation(unittest.TestCase):
    """Test cases for model evaluation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.y_pred = np.array([1.1, 2.0, 3.2, 3.9, 5.1])
    
    def test_rmse_calculation(self):
        """Test RMSE calculation"""
        rmse = ModelEvaluator.calculate_rmse(self.y_true, self.y_pred)
        self.assertGreater(rmse, 0)
        self.assertLess(rmse, 1)
    
    def test_mae_calculation(self):
        """Test MAE calculation"""
        mae = ModelEvaluator.calculate_mae(self.y_true, self.y_pred)
        self.assertGreater(mae, 0)
        self.assertLess(mae, 0.5)
    
    def test_r2_calculation(self):
        """Test R2 calculation"""
        r2 = ModelEvaluator.calculate_r2(self.y_true, self.y_pred)
        self.assertGreater(r2, 0.9)
        self.assertLessEqual(r2, 1.0)


class TestRuleBasedPriceEstimator(unittest.TestCase):
    """Test cases for the rule-based house pricing estimator."""

    def test_estimate_price_returns_expected_structure(self):
        result = estimate_price(
            house_type="Nhà phố",
            legal_status="Sổ đỏ/Sổ hồng đầy đủ",
            district="Trung tâm (Q1, Q3, Q4, Bình Thạnh, Phú Nhuận)",
            land_area_m2=80,
            num_floors=3,
            position="Mặt tiền đường",
        )

        self.assertIsInstance(result, PriceEstimate)
        self.assertGreater(result.mid_bil, 0)
        self.assertGreater(result.high_bil, result.mid_bil)
        self.assertIn("diện tích đất (m2)", result.breakdown)
        self.assertIsNotNone(result.price_per_m2_mid)

    def test_estimate_from_property_uses_available_project_fields(self):
        result = estimate_from_property(
            area=90,
            bedrooms=3,
            bathrooms=2,
            age=5,
            district="Quận 7",
            house_type="Nhà phố",
            legal_status="Đang chờ sổ",
        )

        self.assertIsInstance(result, PriceEstimate)
        self.assertGreater(result.mid_bil, 0)
        self.assertEqual(result.district, "Quận 7")


if __name__ == '__main__':
    unittest.main()
