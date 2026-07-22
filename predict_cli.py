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

def train_model(house_type):
    import subprocess
    script = Path(__file__).resolve().parent / "train_advanced.py"
    result = subprocess.run(["python", str(script)], capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        return False, result.stderr
    return True, result.stdout

def predict(house_type, features):
    model_path = MODEL_DIR / f"{house_type}_model.pkl"
    if not model_path.exists():
        ok, msg = train_model(house_type)
        if not ok:
            return {"error": f"Train failed: {msg}"}

    try:
        data = joblib.load(model_path)
    except Exception as e:
        return {"error": f"Failed to load model: {e}"}

    model = data['model']
    feature_names = data['feature_names']

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
    try:
        if len(sys.argv) > 1 and sys.argv[1] == '--stdin':
            input_data = json.loads(sys.stdin.read())
            house_type = input_data['house_type']
            features = input_data['features']
        else:
            house_type = sys.argv[1]
            features_json = sys.argv[2]
            features = json.loads(features_json)

        result = predict(house_type, features)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
