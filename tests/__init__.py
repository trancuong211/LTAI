"""
Unit tests for house price prediction project
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestDataLoading(unittest.TestCase):
    """Test cases for data loading functionality"""
    
    def test_imports(self):
        """Test that all imports work"""
        try:
            from data.load_data import load_raw_data
            from data.preprocess import handle_missing_values
            from features.build_features import create_polynomial_features
            from models.train_model import ModelTrainer
            from models.evaluate import ModelEvaluator
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == '__main__':
    unittest.main()
