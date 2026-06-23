# main.py
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

from src.data.load_data import load_raw_data
from src.data.preprocess import preprocess_data
from src.features.build_features import build_features
from src.models.train_model import train_model
from src.models.evaluate import evaluate_model

# Danh sách các quận/huyện trong HCM
DISTRICTS = ["Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 7", "Quận 10",
             "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Gò Vấp", "Thủ Đức",
             "Bình Tân", "Tân Phú", "Quận 12", "Bình Chánh", "Nhà Bè"]
HOUSE_TYPES = ["Nhà phố", "Biệt thự", "Căn hộ chung cư", "Nhà hẻm"]
LEGAL_STATUSES = ["Sổ đỏ/Sổ hồng đầy đủ", "Đang chờ sổ", "Giấy tay"]


def create_encoding_mappings(X_processed):
    """
    Tạo mapping từ original values sang encoded values từ training data
    
    Args:
        X_processed: Preprocessed training features
    
    Returns:
        dict: Mapping cho categorical columns
    """
    # Các columns categorical gốc
    categorical_cols = ['district', 'house_type', 'legal_status']
    encodings = {}
    
    # Tạo mapping cho mỗi categorical column
    for col in categorical_cols:
        if col in X_processed.columns:
            # Lấy các unique values đã được encode
            unique_encoded = sorted(X_processed[col].unique())
            # Tạo mapping: encoded_value -> index (0, 1, 2, ...)
            value_to_encoded = {i: int(val) for i, val in enumerate(unique_encoded)}
            encodings[col] = value_to_encoded
    
    return encodings


def prompt_choice(label, options):
    """Hỏi người dùng chọn từ danh sách"""
    print(f"\n{label}:")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Chọn số: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Vui lòng chọn số hợp lệ.")


def prompt_number(label, cast=float):
    """Hỏi người dùng nhập số"""
    while True:
        value = input(f"{label}: ").strip()
        try:
            return cast(value)
        except ValueError:
            print("Vui lòng nhập số hợp lệ.")


def predict_house_price(model, X_processed, feature_names, encodings):
    """
    Interactive function để dự đoán giá nhà
    
    Args:
        model: Trained model
        X_processed: Preprocessed training features (để lấy thông tin)
        feature_names: Tên các features của model
        encodings: Mapping cho categorical columns
    """
    print("\n" + "="*70)
    print("DỰ ĐOÁN GIÁ NHÀ TẠI HỒ CHÍ MINH")
    print("="*70)
    
    while True:
        try:
            # Hỏi thông tin ngôi nhà
            print("\nVui lòng nhập thông tin ngôi nhà:")
            
            area = prompt_number("Diện tích (m²)")
            bedrooms = prompt_number("Số phòng ngủ", int)
            bathrooms = prompt_number("Số phòng tắm", int)
            age = prompt_number("Tuổi nhà (năm)", int)
            district = prompt_choice("Quận/Huyện", DISTRICTS)
            house_type = prompt_choice("Loại nhà", HOUSE_TYPES)
            legal_status = prompt_choice("Pháp lý", LEGAL_STATUSES)
            
            # Tạo dataframe từ input user
            user_data = pd.DataFrame([{
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'age': age,
                'district': district,
                'house_type': house_type,
                'legal_status': legal_status
            }])
            
            # Encode categorical columns
            for col in ['district', 'house_type', 'legal_status']:
                if col in user_data.columns and col in encodings:
                    # Tìm index của value trong DISTRICTS/HOUSE_TYPES/LEGAL_STATUSES
                    if col == 'district':
                        original_idx = DISTRICTS.index(user_data[col].iloc[0])
                    elif col == 'house_type':
                        original_idx = HOUSE_TYPES.index(user_data[col].iloc[0])
                    else:  # legal_status
                        original_idx = LEGAL_STATUSES.index(user_data[col].iloc[0])
                    
                    # Lấy encoded value từ mapping
                    user_data[col] = encodings[col].get(original_idx, 0)
            
            # Tạo engineered features
            user_data['total_rooms'] = user_data['bedrooms'] + user_data['bathrooms']
            user_data['area_per_bedroom'] = user_data['area'] / user_data['bedrooms'].replace(0, 1)
            user_data['age_group'] = pd.cut(user_data['age'], bins=[-1, 5, 15, 200], labels=False)
            
            # Chọn chỉ các columns mà model cần
            user_data = user_data[feature_names]
            
            # Dự đoán
            prediction = model.predict(user_data)[0]
            
            # Hiển thị kết quả
            print("\n" + "="*70)
            print("KẾT QUẢ DỰ ĐOÁN")
            print("="*70)
            print(f"Giá nhà dự đoán: {prediction:.2f} tỷ VNĐ")
            print(f"Tương đương: {prediction * 1_000_000_000:,.0f} VNĐ")
            print("="*70)
            
            # Hỏi có tiếp tục không
            another = input("\nBạn muốn dự đoán ngôi nhà khác? (y/n): ").strip().lower()
            if another != 'y':
                print("\nCảm ơn bạn đã sử dụng dịch vụ dự đoán giá nhà!")
                break
        
        except Exception as e:
            print(f"\nLỗi xảy ra: {e}")
            print("Vui lòng thử lại.")


def main():
    df = load_raw_data("data/raw/house_data.csv")
    df = preprocess_data(df)
    df = build_features(df)
    model, X_test, y_test, X_full, feature_names = train_model(df)
    evaluate_model(model, X_test, y_test)

    # Lưu model với timestamp
    Path("models").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"models/house_price_model_{timestamp}.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")
    
    # Hỏi có muốn dự đoán không
    print("\n")
    predict_choice = input("Bạn có muốn dự đoán giá nhà không? (y/n): ").strip().lower()
    if predict_choice == 'y':
        # Tạo encoding mappings từ training data
        encodings = create_encoding_mappings(X_full)
        # Gọi hàm dự đoán interactive
        predict_house_price(model, X_full, feature_names, encodings)

if __name__ == "__main__":
    main()