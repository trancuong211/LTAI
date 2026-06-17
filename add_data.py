"""
Script thêm dữ liệu nhà mới vào dataset
Cách dùng: py add_data.py
"""
import pandas as pd
import subprocess

CSV_PATH = "data/raw/house_data.csv"

DISTRICTS = ["Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 7", "Quận 10",
             "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Gò Vấp", "Thủ Đức",
             "Bình Tân", "Tân Phú", "Quận 12", "Bình Chánh", "Nhà Bè"]
HOUSE_TYPES = ["Nhà phố", "Biệt thự", "Căn hộ chung cư", "Nhà hẻm"]
LEGAL_STATUSES = ["Sổ đỏ/Sổ hồng đầy đủ", "Đang chờ sổ", "Giấy tay"]


def prompt_choice(label, options):
    print(f"\n{label}:")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Chọn số: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Vui lòng chọn số hợp lệ.")


def prompt_number(label, cast=float):
    while True:
        value = input(f"{label}: ").strip()
        try:
            return cast(value)
        except ValueError:
            print("Vui lòng nhập số hợp lệ.")


def main():
    print("=== Thêm dữ liệu nhà mới ===")
    area = prompt_number("Diện tích (m2)")
    bedrooms = prompt_number("Số phòng ngủ", int)
    bathrooms = prompt_number("Số phòng tắm", int)
    age = prompt_number("Tuổi nhà (năm)", int)
    district = prompt_choice("Quận/Huyện", DISTRICTS)
    house_type = prompt_choice("Loại nhà", HOUSE_TYPES)
    legal_status = prompt_choice("Pháp lý", LEGAL_STATUSES)
    price = prompt_number("Giá (tỷ VNĐ)")

    new_row = {
        "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms,
        "age": age, "district": district, "house_type": house_type,
        "legal_status": legal_status, "price": price,
    }

    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

    print(f"\nĐã thêm dữ liệu mới. Tổng số dòng hiện tại trong dataset: {len(df)}")

    retrain = input("Train lại model ngay với dữ liệu mới? (y/n): ").strip().lower()
    if retrain == "y":
        subprocess.run(["py", "main.py"])
    else:
        print("Bỏ qua train lại. Bạn có thể chạy 'py main.py' bất cứ lúc nào sau này.")


if __name__ == "__main__":
    main()