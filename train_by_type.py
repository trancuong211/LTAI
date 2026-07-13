"""
Train 4 model rieng cho tung loai nha

Nha pho:    18 features
Biet thu:   18 features
Can ho:     17 features
Nha hem:    16 features
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

from constants import (
    DATA_DIR, MODEL_DIR, DISTRICTS, HUONG, PHAP_LY,
    VI_TRI_MAT_TIEN, CHAT_LUONG_XAY_DUNG, LOAI_BIET_THU,
    VIEW_TYPES, VI_TRI_HEM, WARD_MAPPING, TYPE_FEATURES, TYPE_KEYS,
    DU_AN_CAN_HO
)

TYPE_CONFIG = {
    "Nha pho": {"csv": DATA_DIR / "nha_pho.csv", "model_key": "nha_pho"},
    "Biet thu": {"csv": DATA_DIR / "biet_thu.csv", "model_key": "biet_thu"},
    "Can ho chung cu": {"csv": DATA_DIR / "can_ho_chung_cu.csv", "model_key": "can_ho"},
    "Nha hem": {"csv": DATA_DIR / "nha_hem.csv", "model_key": "nha_hem"},
}


def encode_data(df, house_type_name):
    df = df.copy()
    df['phuong'] = df.apply(lambda row: WARD_MAPPING.get(f"{row['quan']}_{row['phuong']}", 0), axis=1)
    df['quan'] = df['quan'].map({d: i for i, d in enumerate(DISTRICTS)})
    df['huong_nha'] = df['huong_nha'].map({h: i for i, h in enumerate(HUONG)})
    df['phap_ly'] = df['phap_ly'].map({p: i for i, p in enumerate(PHAP_LY)})

    if house_type_name == "Nha pho":
        df['vi_tri_mat_tien'] = df['vi_tri_mat_tien'].map({v: i for i, v in enumerate(VI_TRI_MAT_TIEN)})
        df['chat_luong_xay_dung'] = df['chat_luong_xay_dung'].map({c: i for i, c in enumerate(CHAT_LUONG_XAY_DUNG)})
    elif house_type_name == "Biet thu":
        df['loai_biet_thu'] = df['loai_biet_thu'].map({l: i for i, l in enumerate(LOAI_BIET_THU)})
        df['view'] = df['view'].map({v: i for i, v in enumerate(VIEW_TYPES)})
        df['chat_luong_xay_dung'] = df['chat_luong_xay_dung'].map({c: i for i, c in enumerate(CHAT_LUONG_XAY_DUNG)})
    elif house_type_name == "Can ho chung cu":
        df['view'] = df['view'].map({v: i for i, v in enumerate(VIEW_TYPES)})
        df['chat_luong_xay_dung'] = df['chat_luong_xay_dung'].map({c: i for i, c in enumerate(CHAT_LUONG_XAY_DUNG)})
        if 'ten_du_an' in df.columns:
            du_an_map = {name: i for i, name in enumerate(DU_AN_CAN_HO)}
            df['ten_du_an'] = df['ten_du_an'].map(du_an_map).fillna(0).astype(int)
    elif house_type_name == "Nha hem":
        df['vi_tri_hem'] = df['vi_tri_hem'].map({v: i for i, v in enumerate(VI_TRI_HEM)})

    return df


def train_model_for_type(house_type_name, config):
    csv_path = config["csv"]
    model_key = config["model_key"]

    print(f"\n{'='*50}")
    print(f"Training: {house_type_name}")
    print(f"Du lieu: {csv_path}")

    if not csv_path.exists():
        print(f"  Khong tim thay file. Bo qua.")
        return None, None

    df = pd.read_csv(csv_path)
    print(f"So luong mau: {len(df)}")

    if len(df) < 10:
        print(f"  Khong du mau. Bo qua.")
        return None, None

    df_encoded = encode_data(df, house_type_name)
    feature_names = TYPE_FEATURES[house_type_name]

    available_features = [f for f in feature_names if f in df_encoded.columns]
    df_clean = df_encoded[available_features + ['gia']].dropna()
    print(f"Sau khi loai bo NaN: {len(df_clean)} mau")
    print(f"Features ({len(available_features)}): {available_features}")

    X = df_clean[available_features]
    y = np.log1p(df_clean['gia'])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    gia_that = np.expm1(y_test)
    gia_pred = np.expm1(y_pred)
    rmse_ty = np.sqrt(mean_squared_error(gia_that, gia_pred))
    mae_ty = mean_absolute_error(gia_that, gia_pred)
    r2_ty = r2_score(gia_that, gia_pred)

    print(f"RMSE (ty):  {rmse_ty:.2f} ty")
    print(f"MAE (ty):   {mae_ty:.2f} ty")
    print(f"R2 (ty):    {r2_ty:.4f}")

    importances = model.feature_importances_
    feat_imp = sorted(zip(available_features, importances), key=lambda x: x[1], reverse=True)
    print(f"\nFeature importance:")
    for fname, imp in feat_imp:
        print(f"  {fname}: {imp:.4f}")

    model_path = MODEL_DIR / f"{model_key}_model.pkl"
    joblib.dump({
        'model': model,
        'feature_names': available_features,
        'house_type': house_type_name,
    }, model_path)
    print(f"Saved: {model_path}")

    return model, r2_ty


def main():
    print("=== Train 4 model rieng cho tung loai nha ===")

    MODEL_DIR.mkdir(exist_ok=True)

    results = {}
    for house_type_name, config in TYPE_CONFIG.items():
        model, r2 = train_model_for_type(house_type_name, config)
        if r2 is not None:
            results[house_type_name] = r2

    print(f"\n{'='*50}")
    print("TONG KET")
    print(f"{'='*50}")
    for name, r2 in results.items():
        print(f"{name}: R2 = {r2:.4f}")


if __name__ == "__main__":
    main()
