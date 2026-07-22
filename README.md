# AI Dự Đoán Giá Nhà TP.HCM

Dự án Machine Learning dự đoán giá nhà tại TP.HCM sử dụng 4 mô hình riêng biệt cho từng loại nhà.

## Mô tả

- Dự đoán giá nhà cho 4 loại: **Nhà phố**, **Biệt thự**, **Căn hộ chung cư**, **Nhà hẻm**
- Mỗi loại nhà có **file CSV riêng** và **model riêng** với features đặc trưng
- **Tự động chọn thuật toán tốt nhất** qua 5-fold Cross-Validation (RandomForest vs XGBoost vs LightGBM)
- Sai số trung bình (MAPE): **~20.4%** so với giá thực tế
- **~56.5% dự đoán sai dưới 20%**

## Hiệu Suất Model

| Loại nhà | Model | R2 | MAE | MAPE | Sai < 10% | Sai < 15% | Sai < 20% |
|----------|-------|-----|------|------|-----------|-----------|-----------|
| Nhà phố | XGBoost | 0.841 | 5.05 ty | 21.1% | 30.6% | 41.7% | 61.1% |
| Biệt thự | LightGBM | 0.824 | 22.64 ty | 18.7% | 33.3% | 47.2% | 66.7% |
| Căn hộ | LightGBM | 0.880 | 1.81 ty | 18.6% | 19.4% | 52.8% | 63.9% |
| Nhà hẻm | XGBoost | 0.804 | 2.27 ty | 23.2% | 25.0% | 36.1% | 44.4% |
| **Trung bình** | | **0.837** | | **20.4%** | **27.1%** | **44.5%** | **59.0%** |

## Kiến Trúc Hệ Thống

```
Frontend (HTML/JS)  →  Node.js Server (port 8000)  →  Python Predict Server (port 5001)
                         │                                  │
                         ├── preprocessing.js               ├── Pre-loaded models
                         └── static files                   └── Flask API
```

- **Frontend**: Giao diện nhập thông tin nhà
- **Node.js Server**: Xử lý request, preprocessing, serve frontend
- **Python Predict Server**: Flask server, pre-load models khi start, serve predictions

## Cấu Trúc Project

```
LTAI/
│
├── data/raw/                        # Dữ liệu theo loại nhà
│   ├── nha_pho.csv                  # Nhà phố (~200 mẫu)
│   ├── biet_thu.csv                 # Biệt thự (~200 mẫu)
│   ├── can_ho_chung_cu.csv          # Căn hộ chung cư (~200 mẫu)
│   └── nha_hem.csv                  # Nhà hẻm (~200 mẫu)
│
├── models/                          # Model đã train
│   ├── nha_pho_model.pkl
│   ├── biet_thu_model.pkl
│   ├── can_ho_model.pkl
│   └── nha_hem_model.pkl
│
├── backend/                         # Web API
│   ├── server.js                    # Express server (port 8000)
│   ├── predict_server.py            # Flask predict server (port 5001)
│   ├── preprocessing.js             # Xử lý input
│   └── package.json
│
├── frontend/                        # Giao diện web
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── notebooks/                       # Jupyter notebooks (EDA, modeling)
├── tests/                           # Unit tests
├── reports/                         # Báo cáo, biểu đồ
│
├── constants.py                     # Danh mục dùng chung
├── train_advanced.py                # Train nâng cao (CV + model comparison)
├── train_improved.py                # Train với feature engineering + tuning
├── predict_cli.py                   # Predict CLI (JSON bridge)
├── evaluate_models.py               # Đánh giá sai số model
├── add_data.py                      # Thêm dữ liệu thủ công
├── config.yaml                      # Cấu hình
├── requirements.txt                 # Python dependencies
└── README.md
```

## Features Theo Loại Nhà

### Nhà phố (22 features)
```
dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
huong_nha, nam_xay_dung, mat_tien, khoang_cach_trung_tam, phap_ly,
do_sau, do_rong_duong, vi_tri_mat_tien, co_kinh_doanh,
chat_luong_xay_dung, tuoi_nha, co_san_thuong,
dien_tich_x_mat_tien, dien_tich_per_phong, dien_tich_per_tang, mat_tien_per_duong
```

### Biệt thự (21 features)
```
dien_tich_dat, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
huong_nha, nam_xay_dung, mat_tien, khoang_cach_trung_tam, phap_ly,
dien_tich_san_vuon, co_be_boi, co_gara, loai_biet_thu, view,
chat_luong_xay_dung, tuoi_nha,
ty_le_vuon, dien_tich_per_phong, dien_tich_x_mat_tien
```

### Căn hộ chung cư (20 features)
```
dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, tang,
tong_so_tang_toa_nha, huong_nha, nam_xay_dung, view, ten_du_an,
nam_ban_giao, phi_quan_ly, co_thang_may, co_ham, phap_ly,
chat_luong_xay_dung,
dien_tich_per_phong, ty_le_tang, phi_x_dien_tich
```

### Nhà hẻm (19 features)
```
dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
huong_nha, nam_xay_dung, mat_tien, khoang_cach_trung_tam, phap_ly,
do_rong_hem, vi_tri_hem, do_rong_duong_chinh, co_oto_vao_hem,
khoang_cach_ra_duong_chinh,
dien_tich_x_rong_hem, dien_tich_per_phong, kc_x_rong_hem
```

## Cài Đặt

```bash
# Clone repo
git clone <url>
cd LTAI

# Tạo venv
python -m venv .venv
.venv\Scripts\activate  # Windows

# Cài Python dependencies
pip install -r requirements.txt

# Cài Node.js dependencies
cd backend
npm install
```

> **Lưu ý:** Model files (`.pkl`) không được commit lên git. Khi chạy server lần đầu, predict server sẽ tự động train model nếu chưa có.

## Sử Dụng

### 1. Train model

```bash
# Train với feature engineering + hyperparameter tuning
python train_improved.py

# Train nâng cao (CV + Model Comparison)
python train_advanced.py

# Đánh giá sai số
python evaluate_models.py
```

### 2. Chạy Web App

```bash
# Chạy server (tự start predict server)
cd backend
npm start

# Web app: http://localhost:8000
# Predict server: http://localhost:5001
```

### 3. Thêm dữ liệu thủ công

```bash
python add_data.py
```

## Danh Mục Giá Trị

**Quận/Huyện:** Quận 1, Quận 3, Quận 4, Quận 5, Quận 7, Quận 10, Bình Thạnh, Phú Nhuận, Tân Bình, Gò Vấp, Thủ Đức, Bình Tân, Tân Phú, Quận 12, Bình Chánh, Nhà Bè

**Hướng nhà:** Đông, Tây, Nam, Bắc, Đông Nam, Đông Bắc, Tây Nam, Tây Bắc

**Pháp lý:** Sổ hồng, Sổ đỏ, Giấy tờ tay, Đang chờ sổ

**Loại biệt thự:** Đơn lập, Song lập, Hàng kề

**View:** Sông, Thành phố, Nội khu, Không view

**Chất lượng xây dựng:** Cao cấp, Trung bình, Thô

**Vị trí mặt tiền:** Mặt tiền đường lớn, Mặt tiền hẻm, Mặt tiền ngã tư

**Vị trí hẻm:** Hẻm thông, Hẻm cụt

**Tên dự án căn hộ:** Vinhomes Grand Park, Sunrise City, The Estella, Masteri Thao Dien, Saigon Pearl, Vinci Grand Plaza, The Sun Avenue, Icon 56, Saigon Royal, D'Edge, City Garden, Midtown, Charmington, SC VivoCity, Centre Mall, Happy Valley, Millennium

## License

MIT License
