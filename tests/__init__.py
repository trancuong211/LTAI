"""
Unit tests for house price prediction project
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestDataLoading(unittest.TestCase):
    """Test cases for data loading functionality"""

    def test_imports(self):
        """Test that core modules can be imported"""
        try:
            from constants import DISTRICTS, HUONG, TYPE_FEATURES
            self.assertTrue(len(DISTRICTS) > 0)
            self.assertTrue(len(HUONG) > 0)
            self.assertTrue(len(TYPE_FEATURES) > 0)
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == '__main__':
    unittest.main()
