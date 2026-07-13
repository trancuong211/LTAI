"""
Script sinh du lieu nha o HCMC cho 4 model
Mo loai nha co 1 file CSV rieng voi features chuyen biet

Features chung (13):
  dien_tich, quan, phuong, so_phong_ngu, so_phong_tam, so_tang,
  huong_nha, nam_xay_dung, mat_tien, do_rong_hem, khoang_cach_trung_tam,
  phap_ly, gia

Features dac trung Biet thu (5):
  dien_tich_san_vuon, co_be_boi, co_gara_xe_hoi, loai_biet_thu, view

Features dac trung Can ho (7):
  tong_so_tang_toa_nha, tang, view, ten_du_an, nam_ban_giao,
  co_thang_may, phi_quan_ly

Features dac trung Nha hem (4):
  vi_tri_hem, do_rong_duong_chinh, co_oto_vao_hem, khoang_cach_ra_duong_chinh
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import argparse
from pathlib import Path

DATA_DIR = Path("data/raw")

CSV_FILES = {
    "Nha pho": DATA_DIR / "nha_pho.csv",
    "Biet thu": DATA_DIR / "biet_thu.csv",
    "Can ho chung cu": DATA_DIR / "can_ho_chung_cu.csv",
    "Nha hem": DATA_DIR / "nha_hem.csv",
}

COMMON_COLUMNS = [
    "dien_tich", "quan", "phuong", "so_phong_ngu", "so_phong_tam", "so_tang",
    "huong_nha", "nam_xay_dung", "mat_tien",
    "khoang_cach_trung_tam", "phap_ly", "gia"
]

NHA_PHO_EXTRA = ["do_sau", "do_rong_duong", "vi_tri_mat_tien", "co_kinh_doanh", "chat_luong_xay_dung", "tuoi_nha", "co_san_thuong"]
BIET_THU_EXTRA = ["dien_tich_san_vuon", "co_be_boi", "co_gara", "loai_biet_thu", "view", "chat_luong_xay_dung", "tuoi_nha"]
CAN_HO_EXTRA = ["tong_so_tang_toa_nha", "tang", "view", "ten_du_an", "nam_ban_giao", "co_thang_may", "phi_quan_ly", "co_ham", "chat_luong_xay_dung"]
NHA_HEM_EXTRA = ["do_rong_hem", "vi_tri_hem", "do_rong_duong_chinh", "co_oto_vao_hem", "khoang_cach_ra_duong_chinh"]

COLUMNS = {
    "Nha pho": COMMON_COLUMNS + NHA_PHO_EXTRA,
    "Biet thu": ["dien_tich_dat" if c == "dien_tich" else c for c in COMMON_COLUMNS] + BIET_THU_EXTRA,
    "Can ho chung cu": [c for c in COMMON_COLUMNS if c not in ["so_tang", "mat_tien", "khoang_cach_trung_tam"]] + CAN_HO_EXTRA,
    "Nha hem": COMMON_COLUMNS + NHA_HEM_EXTRA,
}

DISTRICTS = ["Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 7", "Quận 10",
             "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Gò Vấp", "Thủ Đức",
             "Bình Tân", "Tân Phú", "Quận 12", "Bình Chánh", "Nhà Bè"]

WARDS = {
    "Quận 1": ["Bến Nghé", "Bến Thành", "Cầu Kho", "Cầu Ông Lãnh", "Đa Kao", "Nguyễn Cư Trinh", "Nguyễn Thái Bình", "Tân Định"],
    "Quận 3": ["Phú Nhuận", "Võ Thị Sáu", "9", "10", "11", "12", "13", "14"],
    "Quận 4": ["Tân Thuận Đông", "Tân Thuận Tây", "Tân Kiểng", "Tân Hưng", "Bình Thuận", "Phú Thuận"],
    "Quận 5": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    "Quận 7": ["Tân Phong", "Tân Phú", "Tân Kiểng", "Tân Hưng", "Bình Thuận", "Phú Thuận", "Tân Quy", "Tân Mỹ"],
    "Quận 10": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    "Bình Thạnh": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"],
    "Phú Nhuận": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"],
    "Tân Bình": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    "Gò Vấp": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"],
    "Thủ Đức": ["Linh Chiểu", "Linh Tây", "Linh Đông", "Linh Trung", "Bình Chiểu", "Hiệp Bình Chánh", "Hiệp Bình Phước", "Tam Phú", "Trường Thọ"],
    "Bình Tân": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    "Tân Phú": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    "Quận 12": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    "Bình Chánh": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
    "Nhà Bè": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

HUONG = ["Đông", "Tây", "Nam", "Bắc", "Đông Nam", "Đông Tây", "Tây Nam", "Tây Bắc", "Đông Bắc", "Tây Bắc"]
PHAP_LY = ["Sổ hồng", "Sổ đỏ", "Giấy tờ tay", "Đang chờ sổ"]
LOAI_BIET_THU = ["Đơn lập", "Song lập", "Hàng kề"]
VIEW_TYPES = ["Sông", "Thành phố", "Nội khu", "Không view"]
VI_TRI_HEM = ["Hẻm thông", "Hẻm cụt"]
DU_AN_CAN_HO = [
    "Vinhomes Grand Park", "Sunrise City", "The Estella", "Masteri Thao Dien",
    "Saigon Pearl", "Vinci Grand Plaza", "The Sun Avenue", "Icon 56",
    "Saigon Royal", "D'Edge", "City Garden", "Midtown", "Charmington",
    "SC VivoCity", "Centre Mall", "Happy Valley", "Millennium"
]

DISTRICT_PRICE = {
    "Nha pho": {
        "Quận 1": (380, 520), "Quận 3": (260, 380), "Quận 4": (200, 300), "Quận 5": (180, 280),
        "Quận 7": (180, 280), "Quận 10": (200, 300), "Bình Thạnh": (170, 270), "Phú Nhuận": (200, 320),
        "Tân Bình": (160, 260), "Gò Vấp": (120, 200), "Thủ Đức": (100, 180), "Bình Tân": (100, 170),
        "Tân Phú": (100, 170), "Quận 12": (60, 110), "Bình Chánh": (80, 140), "Nhà Bè": (70, 130),
    },
    "Biet thu": {
        "Quận 1": (550, 750), "Quận 3": (380, 550), "Quận 4": (300, 450), "Quận 5": (280, 420),
        "Quận 7": (280, 420), "Quận 10": (320, 480), "Bình Thạnh": (270, 420), "Phú Nhuận": (300, 460),
        "Tân Bình": (250, 400), "Gò Vấp": (180, 300), "Thủ Đức": (150, 260), "Bình Tân": (150, 250),
        "Tân Phú": (150, 250), "Quận 12": (90, 160), "Bình Chánh": (120, 220), "Nhà Bè": (100, 190),
    },
    "Can ho chung cu": {
        "Quận 1": (140, 220), "Quận 3": (110, 180), "Quận 4": (80, 140), "Quận 5": (70, 130),
        "Quận 7": (85, 130), "Quận 10": (90, 150), "Bình Thạnh": (70, 120), "Phú Nhuận": (80, 140),
        "Tân Bình": (65, 110), "Gò Vấp": (50, 90), "Thủ Đức": (45, 80), "Bình Tân": (45, 80),
        "Tân Phú": (45, 80), "Quận 12": (30, 60), "Bình Chánh": (45, 75), "Nhà Bè": (40, 70),
    },
    "Nha hem": {
        "Quận 1": (220, 320), "Quận 3": (160, 250), "Quận 4": (120, 200), "Quận 5": (100, 180),
        "Quận 7": (110, 180), "Quận 10": (120, 200), "Bình Thạnh": (100, 170), "Phú Nhuận": (110, 190),
        "Tân Bình": (90, 160), "Gò Vấp": (70, 130), "Thủ Đức": (60, 120), "Bình Tân": (60, 110),
        "Tân Phú": (60, 110), "Quận 12": (45, 85), "Bình Chánh": (55, 100), "Nhà Bè": (50, 90),
    },
}

DISTRICT_CENTER_DIST = {
    "Quận 1": 0, "Quận 3": 1.5, "Quận 4": 2, "Quận 5": 3,
    "Quận 7": 5, "Quận 10": 3.5, "Bình Thạnh": 3, "Phú Nhuận": 2.5,
    "Tân Bình": 4, "Gò Vấp": 5, "Thủ Đức": 7, "Bình Tân": 6,
    "Tân Phú": 5.5, "Quận 12": 8, "Bình Chánh": 12, "Nhà Bè": 10,
}


VI_TRI_MAT_TIEN = ["Mặt tiền đường lớn", "Mặt tiền hẻm", "Mặt tiền ngã tư"]
CHAT_LUONG_XAY_DUNG = ["Cao cấp", "Trung bình", "Thô"]


def generate_nha_pho(n, rng):
    rows = []
    for _ in range(n):
        district = rng.choice(DISTRICTS, p=_district_weights())
        phuong = rng.choice(WARDS.get(district, ["1"]))
        dien_tich = rng.integers(40, 200)
        so_phong_ngu = rng.integers(2, 6)
        so_phong_tam = rng.integers(1, min(so_phong_ngu, 4) + 1)
        so_tang = rng.integers(1, 5)
        huong_nha = rng.choice(HUONG)
        nam_xay_dung = rng.integers(2000, 2026)
        mat_tien = round(rng.uniform(3, 12), 1)
        khoang_cach = round(DISTRICT_CENTER_DIST[district] + rng.uniform(-2, 5), 1)
        phap_ly = rng.choice(PHAP_LY, p=[0.5, 0.2, 0.15, 0.15])

        # Features moi
        do_sau = round(rng.uniform(8, 20), 1)
        do_rong_duong = round(rng.uniform(6, 30), 1)
        vi_tri_mat_tien = rng.choice(VI_TRI_MAT_TIEN, p=[0.5, 0.3, 0.2])
        co_kinh_doanh = int(rng.random() < 0.4)
        chat_luong_xay_dung = rng.choice(CHAT_LUONG_XAY_DUNG, p=[0.3, 0.5, 0.2])
        tuoi_nha = 2026 - nam_xay_dung
        co_san_thuong = int(rng.random() < 0.35)

        gia_min, gia_max = DISTRICT_PRICE["Nha pho"][district]
        gia_m2 = rng.uniform(gia_min, gia_max)
        if mat_tien >= 5:
            gia_m2 *= 1.15
        if vi_tri_mat_tien == "Mặt tiền đường lớn":
            gia_m2 *= 1.12
        elif vi_tri_mat_tien == "Mặt tiền ngã tư":
            gia_m2 *= 1.08
        if co_kinh_doanh:
            gia_m2 *= 1.05
        if co_san_thuong:
            gia_m2 *= 1.08
        if chat_luong_xay_dung == "Cao cấp":
            gia_m2 *= 1.1
        elif chat_luong_xay_dung == "Thô":
            gia_m2 *= 0.9
        if tuoi_nha <= 5:
            gia_m2 *= 1.05
        elif tuoi_nha >= 15:
            gia_m2 *= 0.95
        gia = round(dien_tich * gia_m2 / 1000 * rng.uniform(0.9, 1.1), 2)
        gia = max(gia, 0.5)

        rows.append({
            "dien_tich": dien_tich, "quan": district, "phuong": phuong,
            "so_phong_ngu": so_phong_ngu, "so_phong_tam": so_phong_tam,
            "so_tang": so_tang, "huong_nha": huong_nha,
            "nam_xay_dung": nam_xay_dung, "mat_tien": mat_tien,
            "khoang_cach_trung_tam": khoang_cach,
            "phap_ly": phap_ly, "gia": gia,
            "do_sau": do_sau, "do_rong_duong": do_rong_duong,
            "vi_tri_mat_tien": vi_tri_mat_tien, "co_kinh_doanh": co_kinh_doanh,
            "chat_luong_xay_dung": chat_luong_xay_dung, "tuoi_nha": tuoi_nha,
            "co_san_thuong": co_san_thuong,
        })
    return rows


def generate_biet_thu(n, rng):
    rows = []
    for _ in range(n):
        district = rng.choice(DISTRICTS, p=_district_weights())
        phuong = rng.choice(WARDS.get(district, ["1"]))
        dien_tich = rng.integers(150, 500)
        so_phong_ngu = rng.integers(3, 7)
        so_phong_tam = rng.integers(2, 6)
        so_tang = rng.integers(1, 3)
        huong_nha = rng.choice(HUONG)
        nam_xay_dung = rng.integers(2005, 2026)
        mat_tien = round(rng.uniform(8, 20), 1)
        do_rong_hem = round(rng.uniform(6, 15), 1)
        khoang_cach = round(DISTRICT_CENTER_DIST[district] + rng.uniform(-2, 8), 1)
        phap_ly = rng.choice(PHAP_LY, p=[0.6, 0.2, 0.1, 0.1])

        dien_tich_san_vuon = round(rng.uniform(30, 200), 1) if rng.random() < 0.7 else 0
        co_be_boi = int(rng.random() < 0.4)
        co_gara = int(rng.random() < 0.8)
        loai_biet_thu = rng.choice(LOAI_BIET_THU, p=[0.35, 0.35, 0.3])
        view = rng.choice(VIEW_TYPES, p=[0.15, 0.15, 0.3, 0.4])
        chat_luong_xay_dung = rng.choice(CHAT_LUONG_XAY_DUNG, p=[0.4, 0.4, 0.2])
        tuoi_nha = 2026 - nam_xay_dung

        gia_min, gia_max = DISTRICT_PRICE["Biet thu"][district]
        gia_m2 = rng.uniform(gia_min, gia_max)
        if mat_tien >= 10:
            gia_m2 *= 1.1
        if co_be_boi:
            gia_m2 *= 1.05
        if co_gara:
            gia_m2 *= 1.03
        if loai_biet_thu == "Đơn lập":
            gia_m2 *= 1.08
        elif loai_biet_thu == "Song lập":
            gia_m2 *= 1.05
        if view == "Sông":
            gia_m2 *= 1.1
        elif view == "Công viên":
            gia_m2 *= 1.05
        if chat_luong_xay_dung == "Cao cấp":
            gia_m2 *= 1.1
        elif chat_luong_xay_dung == "Thô":
            gia_m2 *= 0.9
        if tuoi_nha <= 5:
            gia_m2 *= 1.05
        elif tuoi_nha >= 15:
            gia_m2 *= 0.95
        gia = round(dien_tich * gia_m2 / 1000 * rng.uniform(0.9, 1.1), 2)
        gia = max(gia, 5.0)

        rows.append({
            "dien_tich_dat": dien_tich, "quan": district, "phuong": phuong,
            "so_phong_ngu": so_phong_ngu, "so_phong_tam": so_phong_tam,
            "so_tang": so_tang, "huong_nha": huong_nha,
            "nam_xay_dung": nam_xay_dung, "mat_tien": mat_tien,
            "khoang_cach_trung_tam": khoang_cach,
            "phap_ly": phap_ly, "gia": gia,
            "dien_tich_san_vuon": dien_tich_san_vuon,
            "co_be_boi": co_be_boi, "co_gara": co_gara,
            "loai_biet_thu": loai_biet_thu, "view": view,
            "chat_luong_xay_dung": chat_luong_xay_dung, "tuoi_nha": tuoi_nha,
        })
    return rows


def generate_can_ho(n, rng):
    rows = []
    for _ in range(n):
        district = rng.choice(DISTRICTS, p=_district_weights())
        phuong = rng.choice(WARDS.get(district, ["1"]))
        dien_tich = rng.integers(35, 150)
        so_phong_ngu = rng.integers(1, 5)
        so_phong_tam = rng.integers(1, min(so_phong_ngu + 1, 4))
        tang = rng.integers(1, 30)
        huong_nha = rng.choice(HUONG)
        nam_xay_dung = rng.integers(2015, 2026)
        phap_ly = rng.choice(PHAP_LY, p=[0.6, 0.15, 0.1, 0.15])

        tong_so_tang_toa_nha = rng.choice([15, 20, 25, 30, 35, 40])
        view = rng.choice(VIEW_TYPES, p=[0.1, 0.3, 0.2, 0.4])
        ten_du_an = rng.choice(DU_AN_CAN_HO)
        nam_ban_giao = nam_xay_dung + rng.integers(1, 3)
        co_thang_may = int(tong_so_tang_toa_nha >= 5)
        phi_quan_ly = round(rng.uniform(8, 25), 1)
        co_ham = int(rng.random() < 0.3)
        chat_luong_xay_dung = rng.choice(CHAT_LUONG_XAY_DUNG, p=[0.3, 0.5, 0.2])

        gia_min, gia_max = DISTRICT_PRICE["Can ho chung cu"][district]
        gia_m2 = rng.uniform(gia_min, gia_max)
        if tang >= 15:
            gia_m2 *= 1.05
        if view == "Sông":
            gia_m2 *= 1.1
        elif view == "Nội khu":
            gia_m2 *= 1.05
        if phi_quan_ly >= 20:
            gia_m2 *= 1.03
        if co_ham:
            gia_m2 *= 1.03
        if chat_luong_xay_dung == "Cao cấp":
            gia_m2 *= 1.08
        elif chat_luong_xay_dung == "Thô":
            gia_m2 *= 0.9
        gia = round(dien_tich * gia_m2 / 1000 * rng.uniform(0.85, 1.15), 2)
        gia = max(gia, 1.0)

        rows.append({
            "dien_tich": dien_tich, "quan": district, "phuong": phuong,
            "so_phong_ngu": so_phong_ngu, "so_phong_tam": so_phong_tam,
            "tang": tang, "huong_nha": huong_nha,
            "nam_xay_dung": nam_xay_dung,
            "phap_ly": phap_ly, "gia": gia,
            "tong_so_tang_toa_nha": tong_so_tang_toa_nha,
            "view": view, "ten_du_an": ten_du_an, "nam_ban_giao": nam_ban_giao,
            "co_thang_may": co_thang_may, "phi_quan_ly": phi_quan_ly,
            "co_ham": co_ham, "chat_luong_xay_dung": chat_luong_xay_dung,
        })
    return rows


def generate_nha_hem(n, rng):
    rows = []
    for _ in range(n):
        district = rng.choice(DISTRICTS, p=_district_weights())
        phuong = rng.choice(WARDS.get(district, ["1"]))
        dien_tich = rng.integers(25, 120)
        so_phong_ngu = rng.integers(1, 5)
        so_phong_tam = rng.integers(1, min(so_phong_ngu + 1, 4))
        so_tang = rng.integers(1, 4)
        huong_nha = rng.choice(HUONG)
        nam_xay_dung = rng.integers(1995, 2026)
        mat_tien = 0
        do_rong_hem = round(rng.choice([2, 2.5, 3, 3.5, 4, 5, 6]), 1)
        khoang_cach = round(DISTRICT_CENTER_DIST[district] + rng.uniform(-2, 8), 1)
        phap_ly = rng.choice(PHAP_LY, p=[0.4, 0.25, 0.2, 0.15])

        # Features dac trung Nha hem
        vi_tri_hem = rng.choice(VI_TRI_HEM, p=[0.7, 0.3])  # 70% hem thong
        do_rong_duong_chinh = round(rng.uniform(6, 16), 1)
        co_oto_vao_hem = int(do_rong_hem >= 3.5)  # Oto vao duoc neu hem >= 3.5m
        khoang_cach_ra_duong = round(rng.uniform(10, 200), 0)

        gia_min, gia_max = DISTRICT_PRICE["Nha hem"][district]
        gia_m2 = rng.uniform(gia_min, gia_max)
        if do_rong_hem >= 5:
            gia_m2 *= 1.15
        elif do_rong_hem >= 3.5:
            gia_m2 *= 1.05
        if vi_tri_hem == "Hẻm thông":
            gia_m2 *= 1.05
        if co_oto_vao_hem:
            gia_m2 *= 1.08
        if khoang_cach_ra_duong < 50:
            gia_m2 *= 1.08
        gia = round(dien_tich * gia_m2 / 1000 * rng.uniform(0.9, 1.1), 2)
        gia = max(gia, 0.3)

        rows.append({
            "dien_tich": dien_tich, "quan": district, "phuong": phuong,
            "so_phong_ngu": so_phong_ngu, "so_phong_tam": so_phong_tam,
            "so_tang": so_tang, "huong_nha": huong_nha,
            "nam_xay_dung": nam_xay_dung, "mat_tien": mat_tien,
            "do_rong_hem": do_rong_hem, "khoang_cach_trung_tam": khoang_cach,
            "phap_ly": phap_ly, "gia": gia,
            "vi_tri_hem": vi_tri_hem, "do_rong_duong_chinh": do_rong_duong_chinh,
            "co_oto_vao_hem": co_oto_vao_hem, "khoang_cach_ra_duong_chinh": khoang_cach_ra_duong,
        })
    return rows


def _district_weights():
    w = [0.12, 0.10, 0.04, 0.05, 0.06, 0.03, 0.08, 0.06, 0.07, 0.06,
         0.08, 0.05, 0.05, 0.05, 0.05, 0.05]
    return np.array(w) / sum(w)


def main():
    parser = argparse.ArgumentParser(description="Sinh du lieu nha HCMC")
    parser.add_argument("--count", type=int, default=200, help="So mau sinh moi loai")
    parser.add_argument("--append", action="store_true", help="Them vao file CSV co san")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    n = args.count

    print("=== Sinh du lieu nha HCMC ===")
    print(f"So mau moi loai: {n}")
    print(f"Che do: {'Append' if args.append else 'Tao moi'}")

    generators = {
        "Nha pho": generate_nha_pho,
        "Biet thu": generate_biet_thu,
        "Can ho chung cu": generate_can_ho,
        "Nha hem": generate_nha_hem,
    }

    for house_type, gen_func in generators.items():
        csv_path = CSV_FILES[house_type]
        columns = COLUMNS[house_type]

        rows = gen_func(n, rng)
        df_new = pd.DataFrame(rows)
        gia = [r["gia"] for r in rows]

        if args.append and csv_path.exists():
            df_old = pd.read_csv(csv_path)
            df_merged = pd.concat([df_old, df_new], ignore_index=True)
            df_merged = df_merged[columns]
            df_merged.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f"\n{house_type}: {len(df_old)} -> {len(df_merged)} dong (+{len(df_new)})")
        else:
            df_new = df_new[columns]
            df_new.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f"\n{house_type}: tao moi {len(df_new)} dong -> {csv_path}")

        print(f"  Gia TB: {np.mean(gia):.2f} ty, min: {min(gia):.2f}, max: {max(gia):.2f}")

    print("\nHoan thanh!")


if __name__ == "__main__":
    main()
