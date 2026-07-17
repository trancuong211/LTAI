"""
Predict Server - Pre-load models khi start, serve predict requests
Chay tren port rieng, Node.js goi HTTP den day
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, request, jsonify
import numpy as np
import joblib
import pandas as pd
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
loaded_models = {}

MODEL_KEYS = ["nha_pho", "biet_thu", "can_ho", "nha_hem"]


def load_all_models():
    """Load tat ca models khi server start"""
    start = time.time()
    for key in MODEL_KEYS:
        model_path = MODEL_DIR / f"{key}_model.pkl"
        if model_path.exists():
            data = joblib.load(model_path)
            loaded_models[key] = data
            logger.info(f"Loaded model: {key} ({data.get('model_name', 'unknown')}, features={len(data['feature_names'])})")
        else:
            logger.warning(f"Model not found: {model_path}")
    elapsed = time.time() - start
    logger.info(f"All models loaded in {elapsed:.2f}s")


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "models_loaded": list(loaded_models.keys()),
        "model_count": len(loaded_models)
    })


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        house_type = data.get('house_type')
        features = data.get('features', {})

        if not house_type or house_type not in loaded_models:
            return jsonify({"error": f"Invalid or unloaded house_type: {house_type}"}), 400

        model_data = loaded_models[house_type]
        model = model_data['model']
        feature_names = model_data['feature_names']

        feat_dict = {f: features.get(f, 0) for f in feature_names}
        feat_df = pd.DataFrame([feat_dict])

        logger.info(f"Input features: {feat_dict}")

        start = time.time()
        log_pred = model.predict(feat_df)[0]
        elapsed = time.time() - start

        prediction = np.expm1(log_pred)
        price_vnd = int(prediction * 1_000_000_000)

        logger.info(f"Predict {house_type}: {round(prediction, 2)} ty ({elapsed*1000:.1f}ms)")

        return jsonify({
            "price_billion": round(prediction, 2),
            "price_vnd": price_vnd,
            "model_used": f"{house_type}_model.pkl",
            "house_type": house_type
        })

    except Exception as e:
        logger.error(f"Predict error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    load_all_models()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    logger.info(f"Starting predict server on port {port}")
    app.run(host='127.0.0.1', port=port, debug=False)
