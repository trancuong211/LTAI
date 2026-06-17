# main.py
import joblib
from datetime import datetime
from pathlib import Path

from src.data.load_data import load_raw_data
from src.data.preprocess import preprocess_data
from src.features.build_features import build_features
from src.models.train_model import train_model
from src.models.evaluate import evaluate_model

def main():
    df = load_raw_data("data/raw/house_data.csv")
    df = preprocess_data(df)
    df = build_features(df)
    model, X_test, y_test = train_model(df)
    evaluate_model(model, X_test, y_test)

    # Lưu model với timestamp trong tên file để giữ lại lịch sử các version,
    # không ghi đè model cũ mỗi lần train lại
    Path("models").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"models/house_price_model_{timestamp}.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

if __name__ == "__main__":
    main()