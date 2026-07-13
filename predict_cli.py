"""
Predict CLI - Goi tu Node.js backend
Nhan JSON features, tra ve JSON ket qua
"""
import sys
import json
import numpy as np
import joblib
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent / "models"

def predict(house_type, features):
    model_path = MODEL_DIR / f"{house_type}_model.pkl"
    if not model_path.exists():
        return {"error": f"Model not found: {house_type}"}

    data = joblib.load(model_path)
    model = data['model']
    feature_names = data['feature_names']

    # Build feature array in correct order
    feat_dict = {f: features.get(f, 0) for f in feature_names}

    import pandas as pd
    feat_df = pd.DataFrame([feat_dict])

    log_pred = model.predict(feat_df)[0]
    prediction = np.expm1(log_pred)
    price_vnd = int(prediction * 1_000_000_000)

    return {
        "price_billion": round(prediction, 2),
        "price_vnd": price_vnd,
        "model_used": model_path.name,
        "house_type": house_type
    }

if __name__ == "__main__":
    house_type = sys.argv[1]
    features_json = sys.argv[2]
    features = json.loads(features_json)

    result = predict(house_type, features)
    print(json.dumps(result))
