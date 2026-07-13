"""
Script du doan gia nha - 4 model rieng cho tung loai nha

Nha pho:    18 features
Biet thu:   18 features
Can ho:     17 features
Nha hem:    16 features
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import argparse
import numpy as np
import pandas as pd
import joblib

from constants import (
    DISTRICTS, HUONG, PHAP_LY, VI_TRI_MAT_TIEN, CHAT_LUONG_XAY_DUNG,
    LOAI_BIET_THU, VIEW_TYPES, VI_TRI_HEM, DU_AN_CAN_HO,
    WARD_MAPPING, MODEL_DIR
)

TYPE_NAMES = {
    "nha_pho": "Nhà phố",
    "biet_thu": "Biệt thự",
    "can_ho": "Căn hộ chung cư",
    "nha_hem": "Nhà hẻm",
}


def du_doan_gia(model_key, dien_tich, quan, so_phong_ngu, so_phong_tam,
                phap_ly, so_tang=1, huong_nha="Nam", nam_xay_dung=2020,
                mat_tien=0, khoang_cach_trung_tam=5, phuong="1",
                # Nha pho
                do_sau=12, do_rong_duong=10, vi_tri_mat_tien="Mặt tiền hẻm",
                co_kinh_doanh=0, chat_luong_xay_dung="Trung bình",
                co_san_thuong=0,
                # Biet thu
                dien_tich_san_vuon=0, co_be_boi=0, co_gara=0,
                loai_biet_thu="Đơn lập", view_bt="Không view",
                # Can ho
                tong_so_tang_toa_nha=20, tang=10, view_ch="Không view",
                ten_du_an=0, nam_ban_giao=2024, co_thang_may=1, phi_quan_ly=15,
                co_ham=0,
                # Nha hem
                do_rong_hem=3, vi_tri_hem="Hẻm thông", do_rong_duong_chinh=8,
                co_oto_vao_hem=1, khoang_cach_ra_duong_chinh=50):
    """Du doan gia nha"""
    model_path = MODEL_DIR / f"{model_key}_model.pkl"
    if not model_path.exists():
        print(f"Loai nha '{model_key}' khong hop le. Chon: {list(TYPE_NAMES.keys())}")
        return None

    data = joblib.load(model_path)
    model = data['model']
    feature_names = data['feature_names']

    quan_idx = DISTRICTS.index(quan) if quan in DISTRICTS else 0
    huong_idx = HUONG.index(huong_nha) if huong_nha in HUONG else 2
    phap_ly_idx = PHAP_LY.index(phap_ly) if phap_ly in PHAP_LY else 0
    tuoi_nha = 2026 - nam_xay_dung
    phuong_idx = WARD_MAPPING.get(f"{quan}_{phuong}", 0)

    features = {}

    if model_key == "nha_pho":
        features = {
            "dien_tich": dien_tich,
            "quan": quan_idx,
            "phuong": phuong_idx,
            "so_phong_ngu": so_phong_ngu,
            "so_phong_tam": so_phong_tam,
            "so_tang": so_tang,
            "huong_nha": huong_idx,
            "nam_xay_dung": nam_xay_dung,
            "mat_tien": mat_tien,
            "khoang_cach_trung_tam": khoang_cach_trung_tam,
            "phap_ly": phap_ly_idx,
            "do_sau": do_sau,
            "do_rong_duong": do_rong_duong,
            "vi_tri_mat_tien": VI_TRI_MAT_TIEN.index(vi_tri_mat_tien) if vi_tri_mat_tien in VI_TRI_MAT_TIEN else 1,
            "co_kinh_doanh": co_kinh_doanh,
            "chat_luong_xay_dung": CHAT_LUONG_XAY_DUNG.index(chat_luong_xay_dung) if chat_luong_xay_dung in CHAT_LUONG_XAY_DUNG else 1,
            "tuoi_nha": tuoi_nha,
            "co_san_thuong": co_san_thuong,
        }
    elif model_key == "biet_thu":
        features = {
            "dien_tich_dat": dien_tich,
            "quan": quan_idx,
            "phuong": phuong_idx,
            "so_phong_ngu": so_phong_ngu,
            "so_phong_tam": so_phong_tam,
            "so_tang": so_tang,
            "huong_nha": huong_idx,
            "nam_xay_dung": nam_xay_dung,
            "mat_tien": mat_tien,
            "khoang_cach_trung_tam": khoang_cach_trung_tam,
            "phap_ly": phap_ly_idx,
            "dien_tich_san_vuon": dien_tich_san_vuon,
            "co_be_boi": co_be_boi,
            "co_gara": co_gara,
            "loai_biet_thu": LOAI_BIET_THU.index(loai_biet_thu) if loai_biet_thu in LOAI_BIET_THU else 0,
            "view": VIEW_TYPES.index(view_bt) if view_bt in VIEW_TYPES else 3,
            "chat_luong_xay_dung": CHAT_LUONG_XAY_DUNG.index(chat_luong_xay_dung) if chat_luong_xay_dung in CHAT_LUONG_XAY_DUNG else 1,
            "tuoi_nha": tuoi_nha,
        }
    elif model_key == "can_ho":
        features = {
            "dien_tich": dien_tich,
            "quan": quan_idx,
            "phuong": phuong_idx,
            "so_phong_ngu": so_phong_ngu,
            "so_phong_tam": so_phong_tam,
            "tang": tang,
            "tong_so_tang_toa_nha": tong_so_tang_toa_nha,
            "huong_nha": huong_idx,
            "nam_xay_dung": nam_xay_dung,
            "view": VIEW_TYPES.index(view_ch) if view_ch in VIEW_TYPES else 3,
            "ten_du_an": ten_du_an,
            "nam_ban_giao": nam_ban_giao,
            "phi_quan_ly": phi_quan_ly,
            "co_thang_may": co_thang_may,
            "co_ham": co_ham,
            "phap_ly": phap_ly_idx,
            "chat_luong_xay_dung": CHAT_LUONG_XAY_DUNG.index(chat_luong_xay_dung) if chat_luong_xay_dung in CHAT_LUONG_XAY_DUNG else 1,
        }
    elif model_key == "nha_hem":
        features = {
            "dien_tich": dien_tich,
            "quan": quan_idx,
            "phuong": phuong_idx,
            "so_phong_ngu": so_phong_ngu,
            "so_phong_tam": so_phong_tam,
            "so_tang": so_tang,
            "huong_nha": huong_idx,
            "nam_xay_dung": nam_xay_dung,
            "mat_tien": mat_tien,
            "khoang_cach_trung_tam": khoang_cach_trung_tam,
            "phap_ly": phap_ly_idx,
            "do_rong_hem": do_rong_hem,
            "vi_tri_hem": VI_TRI_HEM.index(vi_tri_hem) if vi_tri_hem in VI_TRI_HEM else 0,
            "do_rong_duong_chinh": do_rong_duong_chinh,
            "co_oto_vao_hem": co_oto_vao_hem,
            "khoang_cach_ra_duong_chinh": khoang_cach_ra_duong_chinh,
        }

    feat_df = pd.DataFrame([{f: features.get(f, 0) for f in feature_names}])

    log_pred = model.predict(feat_df)[0]
    gia = np.expm1(log_pred)

    return round(gia, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Du doan gia nha HCM")
    parser.add_argument("model_key", type=str, help="nha_pho, biet_thu, can_ho, nha_hem")
    parser.add_argument("dien_tich", type=float, help="Dien tich (m2)")
    parser.add_argument("so_phong_ngu", type=int, help="So phong ngu")
    parser.add_argument("so_phong_tam", type=int, help="So phong tam")
    parser.add_argument("so_tang", type=int, help="So tang")
    parser.add_argument("quan", type=str, help="Quan/Huyen")
    parser.add_argument("phap_ly", type=str, help="Phap ly")

    parser.add_argument("--phuong", type=str, default="1", help="Phuong")
    parser.add_argument("--huong-nha", type=str, default="Nam")
    parser.add_argument("--nam-xay-dung", type=int, default=2020)
    parser.add_argument("--mat-tien", type=float, default=0)
    parser.add_argument("--khoang-cach", type=float, default=5)

    # Nha pho
    parser.add_argument("--do-sau", type=float, default=12)
    parser.add_argument("--do-rong-duong", type=float, default=10)
    parser.add_argument("--vi-tri-mat-tien", type=str, default="Mặt tiền hẻm")
    parser.add_argument("--co-kinh-doanh", type=int, default=0)
    parser.add_argument("--chat-luong-xay-dung", type=str, default="Trung bình")
    parser.add_argument("--co-san-thuong", type=int, default=0)

    # Biet thu
    parser.add_argument("--dien-tich-san-vuon", type=float, default=0)
    parser.add_argument("--co-be-boi", type=int, default=0)
    parser.add_argument("--co-gara", type=int, default=0)
    parser.add_argument("--loai-biet-thu", type=str, default="Đơn lập")
    parser.add_argument("--view", type=str, default="Không view")

    # Can ho
    parser.add_argument("--tong-so-tang", type=int, default=20)
    parser.add_argument("--tang", type=int, default=10)
    parser.add_argument("--view-ch", type=str, default="Không view")
    parser.add_argument("--ten-du-an", type=int, default=0)
    parser.add_argument("--nam-ban-giao", type=int, default=2024)
    parser.add_argument("--co-thang-may", type=int, default=1)
    parser.add_argument("--phi-quan-ly", type=float, default=15)
    parser.add_argument("--co-ham", type=int, default=0)

    # Nha hem
    parser.add_argument("--do-rong-hem", type=float, default=3)
    parser.add_argument("--vi-tri-hem", type=str, default="Hẻm thông")
    parser.add_argument("--do-rong-duong-chinh", type=float, default=8)
    parser.add_argument("--co-oto", type=int, default=1)
    parser.add_argument("--khoang-cach-ra-duong", type=float, default=50)

    args = parser.parse_args()

    gia = du_doan_gia(
        model_key=args.model_key,
        dien_tich=args.dien_tich,
        quan=args.quan,
        so_phong_ngu=args.so_phong_ngu,
        so_phong_tam=args.so_phong_tam,
        phap_ly=args.phap_ly,
        so_tang=args.so_tang,
        huong_nha=args.huong_nha,
        nam_xay_dung=args.nam_xay_dung,
        mat_tien=args.mat_tien,
        khoang_cach_trung_tam=args.khoang_cach,
        phuong=args.phuong,
        do_sau=args.do_sau,
        do_rong_duong=args.do_rong_duong,
        vi_tri_mat_tien=args.vi_tri_mat_tien,
        co_kinh_doanh=args.co_kinh_doanh,
        chat_luong_xay_dung=args.chat_luong_xay_dung,
        co_san_thuong=args.co_san_thuong,
        dien_tich_san_vuon=args.dien_tich_san_vuon,
        co_be_boi=args.co_be_boi,
        co_gara=args.co_gara,
        loai_biet_thu=args.loai_biet_thu,
        view_bt=args.view,
        tong_so_tang_toa_nha=args.tong_so_tang,
        tang=args.tang,
        view_ch=args.view_ch,
        ten_du_an=args.ten_du_an,
        nam_ban_giao=args.nam_ban_giao,
        co_thang_may=args.co_thang_may,
        phi_quan_ly=args.phi_quan_ly,
        co_ham=args.co_ham,
        do_rong_hem=args.do_rong_hem,
        vi_tri_hem=args.vi_tri_hem,
        do_rong_duong_chinh=args.do_rong_duong_chinh,
        co_oto_vao_hem=args.co_oto,
        khoang_cach_ra_duong_chinh=args.khoang_cach_ra_duong,
    )

    if gia is not None:
        print(f"\n=== DU DOAN GIA NHA ===")
        print(f"Loai nha: {TYPE_NAMES.get(args.model_key, args.model_key)}")
        print(f"Dien tich: {args.dien_tich} m2")
        print(f"Phong ngu: {args.so_phong_ngu}, Phong tam: {args.so_phong_tam}")
        print(f"So tang: {args.so_tang}")
        print(f"Quan: {args.quan}")
        print(f"Huong: {args.huong_nha}")
        print(f"Nam xay dung: {args.nam_xay_dung}")
        print(f"Phap ly: {args.phap_ly}")
        if args.model_key == "nha_pho":
            print(f"Do sau: {args.do_sau}m")
            print(f"Rong duong: {args.do_rong_duong}m")
            print(f"Vi tri: {args.vi_tri_mat_tien}")
            print(f"Kinh doanh: {'Co' if args.co_kinh_doanh else 'Khong'}")
            print(f"San thuong: {'Co' if args.co_san_thuong else 'Khong'}")
            print(f"Chat luong: {args.chat_luong_xay_dung}")
            print(f"Tuoi nha: {2026 - args.nam_xay_dung} nam")
        elif args.model_key == "biet_thu":
            print(f"San vuon: {args.dien_tich_san_vuon} m2")
            print(f"Be boi: {'Co' if args.co_be_boi else 'Khong'}")
            print(f"Gara: {'Co' if args.co_gara else 'Khong'}")
            print(f"Loai: {args.loai_biet_thu}")
            print(f"View: {args.view}")
            print(f"Chat luong: {args.chat_luong_xay_dung}")
            print(f"Tuoi nha: {2026 - args.nam_xay_dung} nam")
        elif args.model_key == "can_ho":
            print(f"Tang: {args.tang}/{args.tong_so_tang}")
            print(f"View: {args.view_ch}")
            print(f"Du an: {DU_AN_CAN_HO[args.ten_du_an] if args.ten_du_an < len(DU_AN_CAN_HO) else args.ten_du_an}")
            print(f"Nam ban giao: {args.nam_ban_giao}")
            print(f"Thang may: {'Co' if args.co_thang_may else 'Khong'}")
            print(f"Ham: {'Co' if args.co_ham else 'Khong'}")
            print(f"Chat luong: {args.chat_luong_xay_dung}")
            print(f"Phi quan ly: {args.phi_quan_ly} nghin/m2/thang")
        elif args.model_key == "nha_hem":
            print(f"Vi tri hem: {args.vi_tri_hem}")
            print(f"Rong duong chinh: {args.do_rong_duong_chinh}m")
            print(f"O to vao hem: {'Co' if args.co_oto else 'Khong'}")
            print(f"Khoang cach ra duong: {args.khoang_cach_ra_duong}m")
        print(f"---")
        print(f"Gia du doan: {gia} ty VND")
        print(f"Tuong duong: {gia * 1_000_000_000:,.0f} VND")
