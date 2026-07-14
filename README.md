# AI Dự Đoán Giá Nhà TP.HCM

Dự án Machine Learning dự đoán giá nhà tại TP.HCM sử dụng 4 mô hình riêng biệt cho từng loại nhà.

## Mô tả

- Dự đoán giá nhà cho 4 loại: **Nhà phố**, **Biệt thự**, **Căn hộ chung cư**, **Nhà hẻm**
- Mỗi loại nhà có **file CSV riêng** và **model riêng** với features đặc trưng
- **Tự động chọn thuật toán tốt nhất** qua 5-fold Cross-Validation (RandomForest vs XGBoost vs LightGBM)
- Sai số trung bình: **~14%** so với giá thực tế

## Cấu trúc Project

```
LTAI/
│
├── data/raw/                        # Dữ liệu theo loại nhà
│   ├── nha_pho.csv                  # Nhà phố
│   ├── biet_thu.csv                 # Biệt thự
│   ├── can_ho_chung_cu.csv          # Căn hộ chung cư
│   └── nha_hem.csv                  # Nhà hẻm
│
├── backend/                         # Web API (Node.js/Express)
│   ├── server.js                    # Express server
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
├── predict_cli.py                   # Predict (JSON bridge cho backend)
├── add_data.py                      # Thêm dữ liệu thủ công
├── config.yaml                      # Cấu hình
├── requirements.txt                 # Python dependencies
└── README.md
```

## Features Theo Loại Nhà

### Nhà phố (18 features)
```
dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
huong_nha, nam_xay_dung, mat_tien, khoang_cach_trung_tam, phap_ly,
do_sau, do_rong_duong, vi_tri_mat_tien, co_kinh_doanh,
chat_luong_xay_dung, tuoi_nha, co_san_thuong
```

### Biệt thự (18 features)
```
dien_tich_dat, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
huong_nha, nam_xay_dung, mat_tien, khoang_cach_trung_tam, phap_ly,
dien_tich_san_vuon, co_be_boi, co_gara, loai_biet_thu, view,
chat_luong_xay_dung, tuoi_nha
```

### Căn hộ chung cư (17 features)
```
dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, tang,
tong_so_tang_toa_nha, huong_nha, nam_xay_dung, view, ten_du_an,
nam_ban_giao, phi_quan_ly, co_thang_may, co_ham, phap_ly,
chat_luong_xay_dung
```

### Nhà hẻm (16 features)
```
dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
huong_nha, nam_xay_dung, mat_tien, khoang_cach_trung_tam, phap_ly,
do_rong_hem, vi_tri_hem, do_rong_duong_chinh, co_oto_vao_hem,
khoang_cach_ra_duong_chinh
```

## Cài Đặt

```bash
# Clone repo
git clone <url>
cd AI_Du_doan_gia_nha_HCM

# Tạo venv
python -m venv .venv
.venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt
```

## Sử Dụng

### 1. Train model

#### Train nâng cao (CV + Model Comparison) - Khuyến nghị
```bash
python train_advanced.py
```

Kết quả train nâng cao:
| Model | Model tốt nhất | CV R2 | Test R2 | MAE (ty) | Sai số % |
|-------|----------------|-------|---------|----------|----------|
| Nhà phố | LightGBM | 0.9376 | 0.9496 | 1.02 | ~14% |
| Biệt thự | LightGBM | 0.9288 | 0.9233 | 2.81 | ~12% |
| Chung cư | RandomForest | 0.9228 | 0.9202 | 0.81 | ~15% |
| Nhà hẻm | LightGBM | 0.9314 | 0.9089 | 0.59 | ~16% |

### 2. Predict (qua web app)
```bash
# Chạy backend server
cd backend
npm install  # nếu chưa cài
node server.js

# Web app sẽ gọi predict_cli.py tự động
```

### 3. Thêm dữ liệu thủ công
```bash
python add_data.py
```

### 4. Chạy Web App
```bash
# Cài dependencies (nếu chưa)
cd backend
npm install

# Chạy server
node server.js

# Mở trình duyệt: http://localhost:3000
```

## Giá Trị Đầu Vào

| Giá trị | Mô tả | Ví dụ |
|---------|-------|-------|
| dien_tich | Diện tích (m²) | 75 |
| quan | Quận/Huyện | Quận 7 |
| phuong | Phường | Tân Phong |
| so_phong_ngu | Số phòng ngủ | 2 |
| so_phong_tam | Số phòng tắm | 2 |
| so_tang | Số tầng | 15 |
| huong_nha | Hướng nhà | Đông Nam |
| nam_xay_dung | Năm xây dựng | 2023 |
| phap_ly | Pháp lý | Sổ hồng |

### Đặc trưng Nhà phố
| Giá trị | Mô tả | Ví dụ |
|---------|-------|-------|
| mat_tien | Mặt tiền (m) | 7 |
| do_sau | Độ sâu (m) | 12 |
| do_rong_duong | Độ rộng đường (m) | 10 |
| vi_tri_mat_tien | Vị trí mặt tiền | Mặt tiền đường lớn / Mặt tiền hẻm / Mặt tiền ngã tư |
| co_kinh_doanh | Có kinh doanh (0/1) | 1 |
| chat_luong_xay_dung | Chất lượng xây dựng | Cao cấp / Trung bình / Thô |
| tuoi_nha | Tuổi nhà (năm) | 5 |
| co_san_thuong | Có sầm u thương (0/1) | 1 |

### Đặc trưng Biệt thự
| Giá trị | Mô tả | Ví dụ |
|---------|-------|-------|
| dien_tich_dat | Diện tích đất (m²) | 250 |
| dien_tich_san_vuon | Diện tích sân vườn (m²) | 120 |
| co_be_boi | Có bể bơi (0/1) | 1 |
| co_gara | Có gara (0/1) | 1 |
| loai_biet_thu | Loại biệt thự | Đơn lập / Song lập / Hàng kề |
| view | View | Sông / Thành phố / Nội khu / Không view |

### Đặc trưng Căn hộ
| Giá trị | Mô tả | Ví dụ |
|---------|-------|-------|
| tang | Tầng hiện tại | 15 |
| tong_so_tang_toa_nha | Tổng số tầng tòa nhà | 25 |
| view | View | Sông / Thành phố / Nội khu / Không view |
| ten_du_an | Tên dự án (index 0-16) | 3 |
| nam_ban_giao | Năm bàn giao | 2024 |
| co_thang_may | Có thang máy (0/1) | 1 |
| phi_quan_ly | Phí quản lý (nghìn/m²/tháng) | 18 |
| co_ham | Có hầm (0/1) | 1 |

### Đặc trưng Nhà hẻm
| Giá trị | Mô tả | Ví dụ |
|---------|-------|-------|
| do_rong_hem | Độ rộng hẻm (m) | 3.5 |
| vi_tri_hem | Vị trí hẻm | Hẻm thông / Hẻm cụt |
| do_rong_duong_chinh | Độ rộng đường chính (m) | 8 |
| co_oto_vao_hem | Ô tô vào hẻm được (0/1) | 1 |
| khoang_cach_ra_duong_chinh | Khoảng cách ra đường chính (m) | 50 |

## Danh Mục Giá Trị

**Quận/Huyện:** Quận 1, Quận 3, Quận 4, Quận 5, Quận 7, Quận 10, Bình Thạnh, Phú Nhuận, Tân Bình, Gò Vấp, Thủ Đức, Bình Tân, Tân Phú, Quận 12, Bình Chánh, Nhà Bè

**Hướng nhà:** Đông, Tây, Nam, Bắc, Đông Nam, Đông Tây, Tây Nam, Tây Bắc, Đông Bắc, Tây Bắc

**Pháp lý:** Sổ hồng, Sổ đỏ, Giấy tờ tay, Đang chờ sổ

**Loại biệt thự:** Đơn lập, Song lập, Hàng kề

**View:** Sông, Thành phố, Nội khu, Không view

**Chất lượng xây dựng:** Cao cấp, Trung bình, Thô

**Vị trí mặt tiền:** Mặt tiền đường lớn, Mặt tiền hẻm, Mặt tiền ngã tư

**Vị trí hẻm:** Hẻm thông, Hẻm cụt

**Tên dự án căn hộ:** Vinhomes Grand Park, Sunrise City, The Estella, Masteri Thao Dien, Saigon Pearl, Vinci Grand Plaza, The Sun Avenue, Icon 56, Saigon Royal, D'Edge, City Garden, Midtown, Charmington, SC VivoCity, Centre Mall, Happy Valley, Millennium

## License

MIT License
