let metaData = null;

const TYPE_NAMES = {
  nha_pho: "Nha pho",
  biet_thu: "Biet thu",
  can_ho: "Can ho chung cu",
  nha_hem: "Nha hem",
};

function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

async function loadMeta() {
  try {
    const res = await fetch("/meta");
    metaData = await res.json();
    populateSelects();
  } catch (e) {
    console.error("Failed to load meta:", e);
  }
}

function populateSelects() {
  if (!metaData) return;

<<<<<<< HEAD
  const quanSelect = document.getElementById("quan");
  quanSelect.innerHTML = metaData.districts
    .map((d) => `<option value="${d}">${d}</option>`)
    .join("");

  const huongSelect = document.getElementById("huong_nha");
  huongSelect.innerHTML = metaData.huong
    .map((h) => `<option value="${h}">${h}</option>`)
    .join("");

  const phapLySelect = document.getElementById("phap_ly");
  phapLySelect.innerHTML = metaData.phap_ly
    .map((p) => `<option value="${p}">${p}</option>`)
    .join("");

  const vtmtSelect = document.getElementById("vi_tri_mat_tien");
  vtmtSelect.innerHTML = metaData.vi_tri_mat_tien
    .map((v) => `<option value="${v}">${v}</option>`)
    .join("");

  const clxdsSelect = document.getElementById("chat_luong_xay_dung");
  clxdsSelect.innerHTML = metaData.chat_luong_xay_dung
    .map((c) => `<option value="${c}">${c}</option>`)
    .join("");

  const clxdsBtSelect = document.getElementById("chat_luong_xay_dung_bt");
  clxdsBtSelect.innerHTML = metaData.chat_luong_xay_dung
    .map((c) => `<option value="${c}">${c}</option>`)
    .join("");

  const clxdsChSelect = document.getElementById("chat_luong_xay_dung_ch");
  clxdsChSelect.innerHTML = metaData.chat_luong_xay_dung
    .map((c) => `<option value="${c}">${c}</option>`)
    .join("");

  const lbtSelect = document.getElementById("loai_biet_thu");
  lbtSelect.innerHTML = metaData.loai_biet_thu
    .map((l) => `<option value="${l}">${l}</option>`)
    .join("");

  const viewBtSelect = document.getElementById("view_bt");
  viewBtSelect.innerHTML = metaData.view
    .map((v) => `<option value="${v}">${v}</option>`)
    .join("");

  const viewChSelect = document.getElementById("view_ch");
  viewChSelect.innerHTML = metaData.view
    .map((v) => `<option value="${v}">${v}</option>`)
    .join("");

  const daSelect = document.getElementById("ten_du_an");
  daSelect.innerHTML = metaData.du_an_can_ho
    .map((d, i) => `<option value="${i}">${d}</option>`)
    .join("");
=======
    // Quan
    const quanSelect = document.getElementById('quan');
    quanSelect.innerHTML = metaData.districts.map(d => `<option value="${escapeHtml(d)}">${escapeHtml(d)}</option>`).join('');

    // Huong
    const huongSelect = document.getElementById('huong_nha');
    huongSelect.innerHTML = metaData.huong.map(h => `<option value="${escapeHtml(h)}">${escapeHtml(h)}</option>`).join('');

    // Phap ly
    const phapLySelect = document.getElementById('phap_ly');
    phapLySelect.innerHTML = metaData.phap_ly.map(p => `<option value="${escapeHtml(p)}">${escapeHtml(p)}</option>`).join('');

    // Vi tri mat tien
    const vtmtSelect = document.getElementById('vi_tri_mat_tien');
    vtmtSelect.innerHTML = metaData.vi_tri_mat_tien.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join('');

    // Chat luong (for nha pho)
    const clxdsSelect = document.getElementById('chat_luong_xay_dung');
    clxdsSelect.innerHTML = metaData.chat_luong_xay_dung.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');

    // Chat luong (for biet thu)
    const clxdsBtSelect = document.getElementById('chat_luong_xay_dung_bt');
    clxdsBtSelect.innerHTML = metaData.chat_luong_xay_dung.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');

    // Loai biet thu
    const lbtSelect = document.getElementById('loai_biet_thu');
    lbtSelect.innerHTML = metaData.loai_biet_thu.map(l => `<option value="${escapeHtml(l)}">${escapeHtml(l)}</option>`).join('');

    // View (biet thu)
    const viewBtSelect = document.getElementById('view_bt');
    viewBtSelect.innerHTML = metaData.view.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join('');

    // View (can ho)
    const viewChSelect = document.getElementById('view_ch');
    viewChSelect.innerHTML = metaData.view.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join('');

    // Du an can ho
    const daSelect = document.getElementById('ten_du_an');
    daSelect.innerHTML = metaData.du_an_can_ho.map((d, i) => `<option value="${i}">${escapeHtml(d)}</option>`).join('');

    // Vi tri hem
    const vthSelect = document.getElementById('vi_tri_hem');
    vthSelect.innerHTML = metaData.vi_tri_hem.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join('');
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743

  const vthSelect = document.getElementById("vi_tri_hem");
  vthSelect.innerHTML = metaData.vi_tri_hem
    .map((v) => `<option value="${v}">${v}</option>`)
    .join("");

  updateWards();
}

function updateWards() {
<<<<<<< HEAD
  if (!metaData) return;
  const quan = document.getElementById("quan").value;
  const phuongSelect = document.getElementById("phuong");
  const wards = metaData.wards[quan] || [];
  phuongSelect.innerHTML = wards
    .map((w) => `<option value="${w}">${w}</option>`)
    .join("");
=======
    if (!metaData) return;
    const quan = document.getElementById('quan').value;
    const phuongSelect = document.getElementById('phuong');
    const wards = metaData.wards[quan] || [];
    phuongSelect.innerHTML = wards.map(w => `<option value="${escapeHtml(w)}">${escapeHtml(w)}</option>`).join('');
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743
}

// Common fields shown/hidden per house type: each type only uses a
// subset of the "Thong so ky thuat" block.
const COMMON_FIELD_VISIBILITY = {
  nha_pho: { fg_dien_tich: true, fg_so_tang: true, fg_mat_tien: true, fg_khoang_cach_trung_tam: true },
  biet_thu: { fg_dien_tich: false, fg_so_tang: true, fg_mat_tien: true, fg_khoang_cach_trung_tam: true },
  can_ho: { fg_dien_tich: true, fg_so_tang: false, fg_mat_tien: false, fg_khoang_cach_trung_tam: false },
  nha_hem: { fg_dien_tich: true, fg_so_tang: true, fg_mat_tien: true, fg_khoang_cach_trung_tam: true },
};

function updateForm() {
  const type = document.getElementById("house_type").value;

<<<<<<< HEAD
  document
    .querySelectorAll(".type-fields")
    .forEach((el) => el.classList.add("hidden"));

  const typeFieldsEl = document.getElementById(`${type}_fields`);
  if (typeFieldsEl) typeFieldsEl.classList.remove("hidden");

  const visibility = COMMON_FIELD_VISIBILITY[type] || {};
  Object.entries(visibility).forEach(([fgId, visible]) => {
    const el = document.getElementById(fgId);
    if (!el) return;
    el.classList.toggle("hidden", !visible);
  });
}

function computeTuoiNha(namXayDung) {
  const currentYear = new Date().getFullYear();
  return currentYear - namXayDung;
=======
    document.querySelectorAll('.type-fields').forEach(el => {
        el.classList.add('hidden');
        el.style.display = '';
    });

    const target = document.getElementById(type + '_fields');
    if (target) {
        target.classList.remove('hidden');
        target.style.display = 'block';
    }
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743
}

function safeParseFloat(id, defaultVal) {
    const val = parseFloat(document.getElementById(id).value);
    return isNaN(val) ? defaultVal : val;
}

function safeParseInt(id, defaultVal) {
    const val = parseInt(document.getElementById(id).value);
    return isNaN(val) ? defaultVal : val;
}

function getFormData() {
<<<<<<< HEAD
  const type = document.getElementById("house_type").value;

  const data = {
    house_type: type,
    quan: document.getElementById("quan").value,
    phuong: document.getElementById("phuong").value,
    so_phong_ngu: parseInt(document.getElementById("so_phong_ngu").value),
    so_phong_tam: parseInt(document.getElementById("so_phong_tam").value),
    huong_nha: document.getElementById("huong_nha").value,
    nam_xay_dung: parseInt(document.getElementById("nam_xay_dung").value),
    phap_ly: document.getElementById("phap_ly").value,
  };
=======
    const type = document.getElementById('house_type').value;
    const data = {
        house_type: type,
        dien_tich: safeParseFloat('dien_tich', 80),
        quan: document.getElementById('quan').value,
        phuong: document.getElementById('phuong').value,
        so_phong_ngu: safeParseInt('so_phong_ngu', 3),
        so_phong_tam: safeParseInt('so_phong_tam', 2),
        so_tang: safeParseInt('so_tang', 3),
        huong_nha: document.getElementById('huong_nha').value,
        nam_xay_dung: safeParseInt('nam_xay_dung', 2020),
        phap_ly: document.getElementById('phap_ly').value,
        mat_tien: safeParseFloat('mat_tien', 5),
        khoang_cach_trung_tam: safeParseFloat('khoang_cach_trung_tam', 5),
    };

    if (type === 'nha_pho') {
        data.do_sau = safeParseFloat('do_sau', 12);
        data.do_rong_duong = safeParseFloat('do_rong_duong', 10);
        data.vi_tri_mat_tien = document.getElementById('vi_tri_mat_tien').value;
        data.chat_luong_xay_dung = document.getElementById('chat_luong_xay_dung').value;
        data.co_kinh_doanh = document.getElementById('co_kinh_doanh').checked ? 1 : 0;
        data.co_san_thuong = document.getElementById('co_san_thuong').checked ? 1 : 0;
    } else if (type === 'biet_thu') {
        data.dien_tich_san_vuon = safeParseFloat('dien_tich_san_vuon', 50);
        data.loai_biet_thu = document.getElementById('loai_biet_thu').value;
        data.view = document.getElementById('view_bt').value;
        data.chat_luong_xay_dung = document.getElementById('chat_luong_xay_dung_bt').value;
        data.co_be_boi = document.getElementById('co_be_boi').checked ? 1 : 0;
        data.co_gara = document.getElementById('co_gara').checked ? 1 : 0;
    } else if (type === 'can_ho') {
        data.tang = safeParseInt('tang', 10);
        data.tong_so_tang_toa_nha = safeParseInt('tong_so_tang_toa_nha', 25);
        data.view = document.getElementById('view_ch').value;
        data.ten_du_an = safeParseInt('ten_du_an', 0);
        data.nam_ban_giao = safeParseInt('nam_ban_giao', 2024);
        data.phi_quan_ly = safeParseFloat('phi_quan_ly', 15);
        data.co_thang_may = document.getElementById('co_thang_may').checked ? 1 : 0;
        data.co_ham = document.getElementById('co_ham').checked ? 1 : 0;
    } else if (type === 'nha_hem') {
        data.do_rong_hem = safeParseFloat('do_rong_hem', 3.5);
        data.vi_tri_hem = document.getElementById('vi_tri_hem').value;
        data.do_rong_duong_chinh = safeParseFloat('do_rong_duong_chinh', 8);
        data.khoang_cach_ra_duong_chinh = safeParseFloat('khoang_cach_ra_duong_chinh', 50);
        data.co_oto_vao_hem = document.getElementById('co_oto_vao_hem').checked ? 1 : 0;
    }
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743

  const tuoiNha = computeTuoiNha(data.nam_xay_dung);

  if (type === "nha_pho") {
    data.dien_tich = parseFloat(document.getElementById("dien_tich").value);
    data.so_tang = parseInt(document.getElementById("so_tang").value);
    data.mat_tien = parseFloat(document.getElementById("mat_tien").value);
    data.khoang_cach_trung_tam = parseFloat(
      document.getElementById("khoang_cach_trung_tam").value,
    );
    data.do_sau = parseFloat(document.getElementById("do_sau").value);
    data.do_rong_duong = parseFloat(
      document.getElementById("do_rong_duong").value,
    );
    data.vi_tri_mat_tien = document.getElementById("vi_tri_mat_tien").value;
    data.co_kinh_doanh = document.getElementById("co_kinh_doanh").checked
      ? 1
      : 0;
    data.chat_luong_xay_dung = document.getElementById(
      "chat_luong_xay_dung",
    ).value;
    data.tuoi_nha = tuoiNha;
    data.co_san_thuong = document.getElementById("co_san_thuong").checked
      ? 1
      : 0;
  } else if (type === "biet_thu") {
    data.dien_tich_dat = parseFloat(
      document.getElementById("dien_tich_dat").value,
    );
    data.so_tang = parseInt(document.getElementById("so_tang").value);
    data.mat_tien = parseFloat(document.getElementById("mat_tien").value);
    data.khoang_cach_trung_tam = parseFloat(
      document.getElementById("khoang_cach_trung_tam").value,
    );
    data.dien_tich_san_vuon = parseFloat(
      document.getElementById("dien_tich_san_vuon").value,
    );
    data.co_be_boi = document.getElementById("co_be_boi").checked ? 1 : 0;
    data.co_gara = document.getElementById("co_gara").checked ? 1 : 0;
    data.loai_biet_thu = document.getElementById("loai_biet_thu").value;
    data.view = document.getElementById("view_bt").value;
    data.chat_luong_xay_dung = document.getElementById(
      "chat_luong_xay_dung_bt",
    ).value;
    data.tuoi_nha = tuoiNha;
  } else if (type === "can_ho") {
    data.dien_tich = parseFloat(document.getElementById("dien_tich").value);
    data.tang = parseInt(document.getElementById("tang").value);
    data.tong_so_tang_toa_nha = parseInt(
      document.getElementById("tong_so_tang_toa_nha").value,
    );
    data.view = document.getElementById("view_ch").value;
    data.ten_du_an = parseInt(document.getElementById("ten_du_an").value);
    data.nam_ban_giao = parseInt(document.getElementById("nam_ban_giao").value);
    data.phi_quan_ly = parseFloat(document.getElementById("phi_quan_ly").value);
    data.co_thang_may = document.getElementById("co_thang_may").checked ? 1 : 0;
    data.co_ham = document.getElementById("co_ham").checked ? 1 : 0;
    data.chat_luong_xay_dung = document.getElementById(
      "chat_luong_xay_dung_ch",
    ).value;
  } else if (type === "nha_hem") {
    data.dien_tich = parseFloat(document.getElementById("dien_tich").value);
    data.so_tang = parseInt(document.getElementById("so_tang").value);
    data.mat_tien = parseFloat(document.getElementById("mat_tien").value);
    data.khoang_cach_trung_tam = parseFloat(
      document.getElementById("khoang_cach_trung_tam").value,
    );
    data.do_rong_hem = parseFloat(document.getElementById("do_rong_hem").value);
    data.vi_tri_hem = document.getElementById("vi_tri_hem").value;
    data.do_rong_duong_chinh = parseFloat(
      document.getElementById("do_rong_duong_chinh").value,
    );
    data.khoang_cach_ra_duong_chinh = parseFloat(
      document.getElementById("khoang_cach_ra_duong_chinh").value,
    );
    data.co_oto_vao_hem = document.getElementById("co_oto_vao_hem").checked
      ? 1
      : 0;
  }

  return data;
}

function validateFormData(data) {
    const errors = [];
    if (data.dien_tich <= 0 || data.dien_tich > 10000) errors.push('Dien tich phai tu 1 den 10000 m2');
    if (data.so_phong_ngu < 1 || data.so_phong_ngu > 20) errors.push('So phong ngu phai tu 1 den 20');
    if (data.so_phong_tam < 1 || data.so_phong_tam > 15) errors.push('So phong tam phai tu 1 den 15');
    if (data.so_tang < 1 || data.so_tang > 50) errors.push('So tang phai tu 1 den 50');
    if (data.nam_xay_dung < 1900 || data.nam_xay_dung > new Date().getFullYear()) errors.push('Nam xay dung khong hop le');
    if (data.khoang_cach_trung_tam < 0 || data.khoang_cach_trung_tam > 100) errors.push('Khoang cach trung tam phai tu 0 den 100 km');
    return errors;
}

async function predict() {
  const btn = document.getElementById("predictBtn");
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");
  const resultSection = document.querySelector(".result-section");
  const formSection = document.querySelector(".form-section");

  try {
    if (!btn.dataset.orig) btn.dataset.orig = btn.innerHTML;
    btn.classList.add("loading");
    btn.innerHTML = `<span class="btn-text">Đang dự đoán...</span><span class="btn-spinner"></span>`;
  } catch (err) {
    // ignore if DOM manipulation fails
  }
  btn.disabled = true;
  const formInputs = document.querySelectorAll(
    ".form-section input, .form-section select, .form-section button, .form-section textarea",
  );
  formInputs.forEach((el) => (el.disabled = true));
  const resultSkeleton = document.getElementById("resultSkeleton");
  const placeholder = resultDiv.querySelector(".placeholder");
  if (resultSkeleton) resultSkeleton.classList.add("active");
  if (placeholder) placeholder.classList.add("visually-hidden");
  loadingDiv.classList.remove("hidden");

  let backBtn = document.getElementById("backBtn");

  try {
    const data = getFormData();

    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    let result;
    try {
      result = await res.json();
    } catch (err) {
      throw new Error("Invalid response from server");
    }

<<<<<<< HEAD
    if (!res.ok) {
      const errMsg =
        result?.error ||
        result?.detail ||
        result?.message ||
        "Loi khong xac dinh";
      throw new Error(errMsg);
    }
=======
        const validationErrors = validateFormData(data);
        if (validationErrors.length > 0) {
            throw new Error(validationErrors.join('. '));
        }

        const res = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743

    const priceVndNum =
      result.price_vnd != null
        ? Number(result.price_vnd)
        : result.price_billion != null
          ? Math.round(Number(result.price_billion) * 1e9)
          : null;
    const priceBillion =
      result.price_billion != null
        ? Number(result.price_billion)
        : priceVndNum != null
          ? priceVndNum / 1e9
          : null;

<<<<<<< HEAD
    const priceVnd =
      priceVndNum != null ? priceVndNum.toLocaleString("vi-VN") : "N/A";
    const priceBillionDisplay =
      priceBillion != null
        ? Number(priceBillion).toLocaleString("vi-VN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })
        : "N/A";
=======
        if (!res.ok) {
            const errMsg = result?.error || 'Loi khong xac dinh';
            const detail = result?.detail ? ` (${result.detail.trim().split('\n').pop()})` : '';
            throw new Error(errMsg + detail);
        }
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743

    // area for gia/m2 calc: nha_pho/can_ho/nha_hem -> dien_tich; biet_thu -> dien_tich_dat
    const areaForCalc = data.dien_tich ?? data.dien_tich_dat ?? null;

    const giaPerM2 =
      priceBillion != null && areaForCalc > 0
        ? ((priceBillion * 1000) / areaForCalc).toLocaleString("vi-VN", {
            minimumFractionDigits: 1,
            maximumFractionDigits: 1,
          })
        : "N/A";

    const modelName = result.model_used
      ? result.model_used.replace("_model.pkl", "").replace(/_/g, " ")
      : "N/A";
    const type = data.house_type;

    const detailItems = [
      ["Quan", data.quan],
      ["Phuong", data.phuong],
      ["Phong ngu", data.so_phong_ngu],
      ["Phong tam", data.so_phong_tam],
      ["Huong nha", data.huong_nha],
      ["Nam xay dung", data.nam_xay_dung],
      ["Phap ly", data.phap_ly],
    ];

    if (type === "nha_pho") {
      detailItems.push(
        ["Dien tich", data.dien_tich + " m2"],
        ["So tang", data.so_tang],
        ["Mat tien", data.mat_tien + " m"],
        ["Khoang cach TT", data.khoang_cach_trung_tam + " km"],
        ["Do sau", data.do_sau + " m"],
        ["Do rong duong", data.do_rong_duong + " m"],
        ["Vi tri mat tien", data.vi_tri_mat_tien],
        ["Kinh doanh", data.co_kinh_doanh ? "Co" : "Khong"],
        ["Chat luong xay dung", data.chat_luong_xay_dung],
        ["Tuoi nha", data.tuoi_nha + " nam"],
        ["San thuong", data.co_san_thuong ? "Co" : "Khong"],
      );
    } else if (type === "biet_thu") {
      detailItems.push(
        ["Dien tich dat", data.dien_tich_dat + " m2"],
        ["So tang", data.so_tang],
        ["Mat tien", data.mat_tien + " m"],
        ["Khoang cach TT", data.khoang_cach_trung_tam + " km"],
        ["Dien tich san vuon", data.dien_tich_san_vuon + " m2"],
        ["Be boi", data.co_be_boi ? "Co" : "Khong"],
        ["Gara", data.co_gara ? "Co" : "Khong"],
        ["Loai biet thu", data.loai_biet_thu],
        ["View", data.view],
        ["Chat luong xay dung", data.chat_luong_xay_dung],
        ["Tuoi nha", data.tuoi_nha + " nam"],
      );
    } else if (type === "can_ho") {
      const duAnEl = document.getElementById("ten_du_an");
      const duAnName = duAnEl.options[duAnEl.selectedIndex]?.text || "N/A";
      detailItems.push(
        ["Dien tich", data.dien_tich + " m2"],
        ["Tang hien tai", data.tang],
        ["Tong so tang", data.tong_so_tang_toa_nha],
        ["View", data.view],
        ["Du an", duAnName],
        ["Nam ban giao", data.nam_ban_giao],
        ["Phi quan ly", data.phi_quan_ly + " nghin/m2/thang"],
        ["Thang may", data.co_thang_may ? "Co" : "Khong"],
        ["Ham", data.co_ham ? "Co" : "Khong"],
        ["Chat luong xay dung", data.chat_luong_xay_dung],
      );
    } else if (type === "nha_hem") {
      detailItems.push(
        ["Dien tich", data.dien_tich + " m2"],
        ["So tang", data.so_tang],
        ["Mat tien", data.mat_tien + " m"],
        ["Khoang cach TT", data.khoang_cach_trung_tam + " km"],
        ["Do rong hem", data.do_rong_hem + " m"],
        ["Vi tri hem", data.vi_tri_hem],
        ["Do rong duong chinh", data.do_rong_duong_chinh + " m"],
        ["Khoang cach ra duong", data.khoang_cach_ra_duong_chinh + " m"],
        ["O to vao hem", data.co_oto_vao_hem ? "Duoc" : "Khong"],
      );
    }

    const detailRows = detailItems
      .map(
        ([label, value], index) =>
          `<div class="drow" style="animation-delay:${0.05 + index * 0.05}s"><span class="k">${label}</span><span class="v">${value}</span></div>`,
      )
      .join("");

<<<<<<< HEAD
    resultDiv.innerHTML = `
            <div class="result-top">
                <span class="badge on">${TYPE_NAMES[result.house_type || data.house_type]}</span>
                <span class="badge">Model: ${modelName}</span>
            </div>
            <div class="seal-zone">
                <div class="seal">THẨM ĐỊNH<br>BỞI AI</div>
                <div class="price-label">Giá dự đoán</div>
                <p class="price"><span>${priceBillionDisplay}</span> tỷ VND</p>
                <div class="price-vnd">${priceVnd} VND</div>
                <div class="price-m2">Giá / m²: ${giaPerM2} triệu</div>
            </div>
            <div class="details">
                ${detailRows}
            </div>
        `;
    if (resultSection) {
      resultSection.classList.remove("panel-hidden");
      resultSection.classList.add("panel-visible");
=======
        const detailRows = detailItems.map(([label, value]) =>
            `<div class="detail-row"><span class="detail-label">${escapeHtml(label)}</span><span class="detail-value">${escapeHtml(value)}</span></div>`
        ).join('');

        resultDiv.innerHTML = `
            <div class="result-content">
                <div class="result-header">
                    <span class="result-type-badge">${escapeHtml(TYPE_NAMES[result.house_type || data.house_type])}</span>
                    <span class="result-model-badge">Model: ${escapeHtml(modelName)}</span>
                </div>
                <div class="result-price">${priceBillionDisplay} ty VND</div>
                <div class="result-vnd">${priceVnd} VND</div>
                <div class="result-price-m2">Gia / m2: ${giaPerM2} trieu</div>
                <div class="result-divider"></div>
                <h3 class="result-section-title">Thong tin da chon</h3>
                <div class="result-details-grid">
                    ${detailRows}
                </div>
            </div>
        `;
        resultDiv.classList.remove('hidden');
    } catch (e) {
        resultDiv.innerHTML = `<div class="error"><p>Loi: ${escapeHtml(e.message)}</p></div>`;
        resultDiv.classList.remove('hidden');
    } finally {
        btn.disabled = false;
        loadingDiv.classList.add('hidden');
>>>>>>> 518445034424bf6a098414a00d1bc305eb391743
    }
    if (formSection) {
      formSection.classList.add("panel-hidden");
      formSection.classList.remove("panel-visible");
    }
    backBtn = document.getElementById("backBtn");
    if (backBtn) {
      backBtn.onclick = () => {
        if (formSection) {
          formSection.classList.remove("panel-hidden");
          formSection.classList.add("panel-visible");
        }
        if (resultSection) {
          resultSection.classList.remove("panel-visible");
          resultSection.classList.add("panel-hidden");
        }
      };
    }
  } catch (e) {
    resultDiv.innerHTML = `<div class="error"><p>Loi: ${e.message}</p></div>`;
    if (resultSection) {
      resultSection.classList.remove("panel-hidden");
      resultSection.classList.add("panel-visible");
    }
    if (formSection) {
      formSection.classList.add("panel-hidden");
      formSection.classList.remove("panel-visible");
    }
    const backBtnErr = document.getElementById("backBtn");
    if (backBtnErr) backBtnErr.onclick = backBtn?.onclick;
  } finally {
    if (document.getElementById("resultSkeleton")) {
      document.getElementById("resultSkeleton").classList.remove("active");
    }
    if (placeholder) placeholder.classList.remove("visually-hidden");
    try {
      if (btn.dataset.orig) btn.innerHTML = btn.dataset.orig;
      btn.classList.remove("loading");
    } catch (err) {}
    btn.disabled = false;
    formInputs.forEach((el) => (el.disabled = false));
    loadingDiv.classList.add("hidden");
  }
}

// Init
window.onload = function () {
  loadMeta();
  updateForm();
};
