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


if __name__ == '__main__':
    unittest.main()
