# House Price Prediction Project

Dự án dự đoán giá nhà sử dụng các kỹ thuật Machine Learning.

## Mô tả Dự án

Đây là một dự án Machine Learning nhằm xây dựng mô hình dự đoán giá nhà dựa trên các đặc trưng như diện tích, số phòng ngủ, vị trí, v.v.

## Cấu trúc Dự án

```
house-price-prediction/
│
├── data/                          # Dữ liệu
│   ├── raw/                       # Dữ liệu gốc, chưa xử lý
│   ├── processed/                 # Dữ liệu đã làm sạch, sẵn sàng train
│   └── external/                  # Dữ liệu phụ (vị trí, lãi suất, v.v.)
│
├── notebooks/                     # Jupyter Notebooks
│   ├── 01_eda.ipynb              # Phân tích dữ liệu khám phá (EDA)
│   ├── 02_feature_engineering.ipynb  # Xây dựng đặc trưng
│   ├── 03_modeling.ipynb         # Huấn luyện mô hình
│   └── 04_evaluation.ipynb       # Đánh giá mô hình
│
├── src/                           # Mã nguồn
│   ├── data/
│   │   ├── load_data.py          # Đọc dữ liệu
│   │   └── preprocess.py         # Xử lý missing values, outliers, encoding
│   │
│   ├── features/
│   │   └── build_features.py     # Tạo đặc trưng mới
│   │
│   ├── models/
│   │   ├── train_model.py        # Huấn luyện mô hình
│   │   ├── predict_model.py      # Dự đoán
│   │   └── evaluate.py           # Đánh giá (RMSE, MAE, R²...)
│   │
│   └── utils/
│       └── helpers.py             # Hàm hỗ trợ chung
│
├── models/                        # Lưu mô hình đã train (.pkl, .joblib)
│
├── reports/                       # Báo cáo
│   ├── figures/                  # Biểu đồ, visualizations
│   └── results.md                # Kết quả thí nghiệm
│
├── api/                          # FastAPI serving model
│   ├── main.py
│   └── schemas.py
│
├── tests/                        # Unit tests
│
├── requirements.txt              # Dependencies
├── config.yaml                   # Cấu hình
├── README.md                     # Tài liệu này
└── .gitignore                    # Git ignore rules
```

## Các Bước Chính

### 1. Chuẩn Bị Dữ Liệu

- Đặt dữ liệu gốc vào thư mục `data/raw/`
- Chạy notebook `01_eda.ipynb` để phân tích dữ liệu

### 2. Tiền Xử Lý & Feature Engineering

- Xử lý missing values, outliers
- Encoding categorical variables
- Tạo đặc trưng mới
- Chạy notebook `02_feature_engineering.ipynb`

### 3. Huấn Luyện Mô Hình

- Huấn luyện nhiều mô hình khác nhau
- So sánh hiệu suất
- Chạy notebook `03_modeling.ipynb`

### 4. Đánh Giá & Kết Quả

- Đánh giá mô hình trên test set
- Phân tích residuals
- Lưu mô hình tốt nhất
- Chạy notebook `04_evaluation.ipynb`

## Cài Đặt

### Yêu Cầu
- Python 3.9+
- pip hoặc conda

### Bước Cài Đặt

1. Clone repository:
```bash
git clone <repository-url>
cd house-price-prediction
```

2. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Chạy Jupyter:
```bash
jupyter lab
```

## Các Mô Hình Được Sử Dụng

1. **Linear Regression** - Baseline model
2. **Ridge Regression** - Với regularization L2
3. **Lasso Regression** - Với regularization L1
4. **Random Forest** - Ensemble learning
5. **Gradient Boosting** - Advanced ensemble method
6. **Support Vector Regression** - SVM approach

## Metrics Đánh Giá

- **RMSE** (Root Mean Squared Error)
- **MAE** (Mean Absolute Error)
- **R² Score** (Coefficient of Determination)
- **MAPE** (Mean Absolute Percentage Error)

## API Deployment

Để chạy API:

```bash
cd api
uvicorn main:app --reload
```

API sẽ chạy tại `http://localhost:8000`

### API Endpoints

- `GET /` - Trang chủ
- `GET /health` - Health check
- `POST /predict` - Dự đoán giá nhà

## Cấu Hình

Tất cả các hyperparameters và cấu hình được lưu trong file `config.yaml`:

- Đường dẫn dữ liệu
- Tham số tiền xử lý
- Hyperparameters của mô hình
- Cấu hình API

## Testing

Chạy unit tests:

```bash
pytest tests/
```

## Tác Giả

Dự án được tạo cho mục đích học tập và thực hành Machine Learning.

## License

MIT License

## Liên Hệ

Để thắc mắc hoặc đóng góp, vui lòng tạo issue hoặc pull request.

## Tài Liệu Tham Khảo

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
