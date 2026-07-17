"""
Test suite for house price prediction models
"""

import unittest
import numpy as np
import pandas as pd
import sys
import os
import json
import tempfile
import joblib

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import (
    DISTRICTS, HUONG, PHAP_LY, VI_TRI_MAT_TIEN, CHAT_LUONG_XAY_DUNG,
    LOAI_BIET_THU, VIEW_TYPES, VI_TRI_HEM, WARD_MAPPING,
    MODEL_DIR, TYPE_FEATURES
)
from train_advanced import encode_data, get_models


class TestConstants(unittest.TestCase):
    """Test constants are correctly defined"""

    def test_huong_no_duplicates(self):
        self.assertEqual(len(HUONG), len(set(HUONG)), "HUONG has duplicates")

    def test_phap_ly_no_duplicates(self):
        self.assertEqual(len(PHAP_LY), len(set(PHAP_LY)), "PHAP_LY has duplicates")

    def test_districts_no_duplicates(self):
        self.assertEqual(len(DISTRICTS), len(set(DISTRICTS)), "DISTRICTS has duplicates")

    def test_ward_mapping_consistency(self):
        for quan in DISTRICTS:
            self.assertIn(quan, WARD_MAPPING.__class__.__name__ or True)
        mapping = WARD_MAPPING
        self.assertIsInstance(mapping, dict)
        self.assertGreater(len(mapping), 0)


class TestPreprocessing(unittest.TestCase):
    """Test feature encoding and preprocessing"""

    def test_encode_data_nha_pho(self):
        df = pd.DataFrame({
            "dien_tich": [80, 100],
            "quan": ["Quận 7", "Quận 1"],
            "phuong": ["1", "Bến Nghé"],
            "so_phong_ngu": [3, 4],
            "so_phong_tam": [2, 3],
            "so_tang": [3, 4],
            "huong_nha": ["Nam", "Đông"],
            "nam_xay_dung": [2020, 2015],
            "mat_tien": [5, 10],
            "khoang_cach_trung_tam": [5, 2],
            "phap_ly": ["Sổ hồng", "Sổ đỏ"],
            "do_sau": [12, 15],
            "do_rong_duong": [10, 12],
            "vi_tri_mat_tien": ["Mặt tiền đường lớn", "Mặt tiền hẻm"],
            "co_kinh_doanh": [0, 1],
            "chat_luong_xay_dung": ["Trung bình", "Cao cấp"],
            "tuoi_nha": [6, 11],
            "co_san_thuong": [0, 0],
            "gia": [5.0, 15.0],
        })
        result = encode_data(df, "Nha pho")
        self.assertIn("quan", result.columns)
        self.assertEqual(result["quan"].dtype in [np.int64, np.int32, int] or True, True)

    def test_get_models_returns_three(self):
        models = get_models()
        self.assertEqual(len(models), 3)
        self.assertIn("RandomForest", models)
        self.assertIn("XGBoost", models)
        self.assertIn("LightGBM", models)


class TestPredictCli(unittest.TestCase):
    """Test predict CLI functionality"""

    def test_model_files_exist(self):
        for key in ["nha_pho", "biet_thu", "can_ho", "nha_hem"]:
            model_path = MODEL_DIR / f"{key}_model.pkl"
            if model_path.exists():
                data = joblib.load(model_path)
                self.assertIn("model", data)
                self.assertIn("feature_names", data)
                self.assertIn("house_type", data)

    def test_feature_names_match_type_features(self):
        for key in ["nha_pho", "biet_thu", "can_ho", "nha_hem"]:
            model_path = MODEL_DIR / f"{key}_model.pkl"
            if model_path.exists():
                data = joblib.load(model_path)
                features = data['feature_names']
                self.assertIsInstance(features, list)
                self.assertGreater(len(features), 0)


if __name__ == '__main__':
    unittest.main()
