/**
 * Preprocessing - Xu ly input giong hau het luc training
 * Chuyen raw input thanh feature dict
 */

const DISTRICTS = [
    "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 7", "Quận 10",
    "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Gò Vấp", "Thủ Đức",
    "Bình Tân", "Tân Phú", "Quận 12", "Bình Chánh", "Nhà Bè"
];

const HUONG = ["Đông", "Tây", "Nam", "Bắc", "Đông Nam", "Đông Bắc", "Tây Nam", "Tây Bắc"];
const PHAP_LY = ["Sổ hồng", "Sổ đỏ", "Giấy tờ tay", "Đang chờ sổ"];
const VI_TRI_MAT_TIEN = ["Mặt tiền đường lớn", "Mặt tiền hẻm", "Mặt tiền ngã tư"];
const CHAT_LUONG_XAY_DUNG = ["Cao cấp", "Trung bình", "Thô"];
const LOAI_BIET_THU = ["Đơn lập", "Song lập", "Hàng kề"];
const VIEW_TYPES = ["Sông", "Thành phố", "Nội khu", "Không view"];
const VI_TRI_HEM = ["Hẻm thông", "Hẻm cụt"];

const WARDS = {
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
    "Nhà Bè": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
};

function buildWardMapping() {
    const mapping = {};
    let idx = 0;
    for (const [quan, phuongs] of Object.entries(WARDS)) {
        for (const phuong of phuongs) {
            const key = `${quan}_${phuong}`;
            if (!(key in mapping)) {
                mapping[key] = idx++;
            }
        }
    }
    return mapping;
}

const WARD_MAPPING = buildWardMapping();

function safeIndex(arr, val, defaultVal = 0) {
    const idx = arr.indexOf(val);
    return idx >= 0 ? idx : defaultVal;
}

function preprocessInput(data, houseType) {
    const quan = data.quan || "Quận 7";
    const phuong = data.phuong || "1";
    const huongNha = data.huong_nha || "Nam";
    const phapLy = data.phap_ly || "Sổ hồng";
    const namXayDung = data.nam_xay_dung || 2020;
    const tuoiNha = new Date().getFullYear() - namXayDung;

    const quanIdx = safeIndex(DISTRICTS, quan);
    const huongIdx = safeIndex(HUONG, huongNha, 2);
    const phapLyIdx = safeIndex(PHAP_LY, phapLy);
    const phuongIdx = WARD_MAPPING[`${quan}_${phuong}`] || 0;

    const features = {};

    if (houseType === "nha_pho") {
        Object.assign(features, {
            dien_tich: data.dien_tich || 80,
            quan: quanIdx,
            phuong: phuongIdx,
            so_phong_ngu: data.so_phong_ngu || 3,
            so_phong_tam: data.so_phong_tam || 2,
            so_tang: data.so_tang || 3,
            huong_nha: huongIdx,
            nam_xay_dung: namXayDung,
            mat_tien: data.mat_tien || 5,
            khoang_cach_trung_tam: data.khoang_cach_trung_tam || 5,
            phap_ly: phapLyIdx,
            do_sau: data.do_sau || 12,
            do_rong_duong: data.do_rong_duong || 10,
            vi_tri_mat_tien: safeIndex(VI_TRI_MAT_TIEN, data.vi_tri_mat_tien, 1),
            co_kinh_doanh: data.co_kinh_doanh || 0,
            chat_luong_xay_dung: safeIndex(CHAT_LUONG_XAY_DUNG, data.chat_luong_xay_dung, 1),
            tuoi_nha: tuoiNha,
            co_san_thuong: data.co_san_thuong || 0,
        });
    } else if (houseType === "biet_thu") {
        Object.assign(features, {
            dien_tich_dat: data.dien_tich || 250,
            quan: quanIdx,
            phuong: phuongIdx,
            so_phong_ngu: data.so_phong_ngu || 4,
            so_phong_tam: data.so_phong_tam || 3,
            so_tang: data.so_tang || 2,
            huong_nha: huongIdx,
            nam_xay_dung: namXayDung,
            mat_tien: data.mat_tien || 10,
            khoang_cach_trung_tam: data.khoang_cach_trung_tam || 5,
            phap_ly: phapLyIdx,
            dien_tich_san_vuon: data.dien_tich_san_vuon || 50,
            co_be_boi: data.co_be_boi || 0,
            co_gara: data.co_gara || 1,
            loai_biet_thu: safeIndex(LOAI_BIET_THU, data.loai_biet_thu),
            view: safeIndex(VIEW_TYPES, data.view, 3),
            chat_luong_xay_dung: safeIndex(CHAT_LUONG_XAY_DUNG, data.chat_luong_xay_dung, 1),
            tuoi_nha: tuoiNha,
        });
    } else if (houseType === "can_ho") {
        Object.assign(features, {
            dien_tich: data.dien_tich || 75,
            quan: quanIdx,
            phuong: phuongIdx,
            so_phong_ngu: data.so_phong_ngu || 2,
            so_phong_tam: data.so_phong_tam || 2,
            tang: data.tang || 10,
            tong_so_tang_toa_nha: data.tong_so_tang_toa_nha || 25,
            huong_nha: huongIdx,
            nam_xay_dung: namXayDung,
            view: safeIndex(VIEW_TYPES, data.view, 3),
            ten_du_an: parseInt(data.ten_du_an) || 0,
            nam_ban_giao: data.nam_ban_giao || 2024,
            phi_quan_ly: data.phi_quan_ly || 15,
            co_thang_may: data.co_thang_may || 1,
            co_ham: data.co_ham || 0,
            phap_ly: phapLyIdx,
            chat_luong_xay_dung: safeIndex(CHAT_LUONG_XAY_DUNG, data.chat_luong_xay_dung, 1),
        });
    } else if (houseType === "nha_hem") {
        Object.assign(features, {
            dien_tich: data.dien_tich || 55,
            quan: quanIdx,
            phuong: phuongIdx,
            so_phong_ngu: data.so_phong_ngu || 3,
            so_phong_tam: data.so_phong_tam || 2,
            so_tang: data.so_tang || 2,
            huong_nha: huongIdx,
            nam_xay_dung: namXayDung,
            mat_tien: 0,
            khoang_cach_trung_tam: data.khoang_cach_trung_tam || 5,
            phap_ly: phapLyIdx,
            do_rong_hem: data.do_rong_hem || 3.5,
            vi_tri_hem: safeIndex(VI_TRI_HEM, data.vi_tri_hem),
            do_rong_duong_chinh: data.do_rong_duong_chinh || 8,
            co_oto_vao_hem: data.co_oto_vao_hem || 1,
            khoang_cach_ra_duong_chinh: data.khoang_cach_ra_duong_chinh || 50,
        });
    }

    return features;
}

module.exports = {
    preprocessInput,
    DISTRICTS,
    HUONG,
    PHAP_LY,
    VI_TRI_MAT_TIEN,
    CHAT_LUONG_XAY_DUNG,
    LOAI_BIET_THU,
    VIEW_TYPES,
    VI_TRI_HEM,
    WARDS,
    WARD_MAPPING
};
