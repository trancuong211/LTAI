"""
Script them du lieu nha moi vao dataset
Moi loai nha co 1 file CSV rieng

Cach dung: py add_data.py
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path
import subprocess

DATA_DIR = Path("data/raw")

CSV_FILES = {
    "Nha pho": DATA_DIR / "nha_pho.csv",
    "Biet thu": DATA_DIR / "biet_thu.csv",
    "Can ho chung cu": DATA_DIR / "can_ho_chung_cu.csv",
    "Nha hem": DATA_DIR / "nha_hem.csv",
}

COLUMNS = [
    "dien_tich", "quan", "phuong", "so_phong_ngu", "so_phong_tam", "so_tang",
    "huong_nha", "nam_xay_dung", "mat_tien", "do_rong_hem",
    "khoang_cach_trung_tam", "phap_ly", "gia"
]

DISTRICTS = ["Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 7", "Quận 10",
             "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Gò Vấp", "Thủ Đức",
             "Bình Tân", "Tân Phú", "Quận 12", "Bình Chánh", "Nhà Bè"]
HOUSE_TYPES = ["Nha pho", "Biet thu", "Can ho chung cu", "Nha hem"]
HUONG = ["Đông", "Tây", "Nam", "Bắc", "Đông Nam", "Đông Tây", "Tây Nam", "Tây Bắc"]
PHAP_LY = ["Sổ hồng", "Sổ đỏ", "Giấy tờ tay", "Đang chờ sổ"]


def prompt_choice(label, options):
    print(f"\n{label}:")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Chon so: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Vui long chon so hop le.")


def prompt_number(label, cast=float, default=None):
    hint = f" [mac dinh: {default}]" if default is not None else ""
    while True:
        value = input(f"{label}{hint}: ").strip()
        if value == "" and default is not None:
            return default
        try:
            return cast(value)
        except ValueError:
            print("Vui long nhap so hop le.")


def main():
    print("=== THEM DU LIEU NHA MOI ===")

    house_type = prompt_choice("Loai nha", HOUSE_TYPES)

    dien_tich = prompt_number("Dien tich (m2)")
    so_phong_ngu = prompt_number("So phong ngu", int)
    so_phong_tam = prompt_number("So phong tam", int)
    so_tang = prompt_number("So tang", int)
    quan = prompt_choice("Quan/Huyen", DISTRICTS)
    phuong = input("Phuong: ").strip() or "1"
    huong_nha = prompt_choice("Huong nha", HUONG)
    nam_xay_dung = prompt_number("Nam xay dung", int, default=2020)
    phap_ly = prompt_choice("Phap ly", PHAP_LY)
    gia = prompt_number("Gia (ty VND)")

    # Features tuy loai nha
    if house_type == "Nha pho":
        mat_tien = prompt_number("Mat tien (m)")
        do_rong_hem = prompt_number("Do rong duong truoc nha (m)")
    elif house_type == "Biet thu":
        mat_tien = prompt_number("Mat tien (m)")
        do_rong_hem = prompt_number("Do rong duong (m)")
    elif house_type == "Can ho chung cu":
        mat_tien = 0
        do_rong_hem = 0
    else:  # Nha hem
        mat_tien = 0
        do_rong_hem = prompt_number("Do rong hem (m)")

    khoang_cach = prompt_number("Khoang cach den trung tam (km)", default=5)

    new_row = {
        "dien_tich": dien_tich, "quan": quan, "phuong": phuong,
        "so_phong_ngu": so_phong_ngu, "so_phong_tam": so_phong_tam,
        "so_tang": so_tang, "huong_nha": huong_nha,
        "nam_xay_dung": nam_xay_dung, "mat_tien": mat_tien,
        "do_rong_hem": do_rong_hem, "khoang_cach_trung_tam": khoang_cach,
        "phap_ly": phap_ly, "gia": gia,
    }

    csv_path = CSV_FILES[house_type]

    df = pd.read_csv(csv_path) if csv_path.exists() else pd.DataFrame(columns=COLUMNS)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df = df[COLUMNS]
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"\nDa them vao {csv_path}. Tong so dong: {len(df)}")

    retrain = input("Train lai model ngay? (y/n): ").strip().lower()
    if retrain == "y":
        subprocess.run(["python", "train_advanced.py"])
    else:
        print("Bo qua train lai. Chay 'python train_advanced.py' bat cu luc nao.")


if __name__ == "__main__":
    main()
