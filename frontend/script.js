let metaData = null;

const TYPE_NAMES = {
    nha_pho: "Nha pho",
    biet_thu: "Biet thu",
    can_ho: "Can ho chung cu",
    nha_hem: "Nha hem"
};

async function loadMeta() {
    try {
        const res = await fetch('/meta');
        metaData = await res.json();
        populateSelects();
    } catch (e) {
        console.error('Failed to load meta:', e);
    }
}

function populateSelects() {
    if (!metaData) return;

    // Quan
    const quanSelect = document.getElementById('quan');
    quanSelect.innerHTML = metaData.districts.map(d => `<option value="${d}">${d}</option>`).join('');

    // Huong
    const huongSelect = document.getElementById('huong_nha');
    huongSelect.innerHTML = metaData.huong.map(h => `<option value="${h}">${h}</option>`).join('');

    // Phap ly
    const phapLySelect = document.getElementById('phap_ly');
    phapLySelect.innerHTML = metaData.phap_ly.map(p => `<option value="${p}">${p}</option>`).join('');

    // Vi tri mat tien
    const vtmtSelect = document.getElementById('vi_tri_mat_tien');
    vtmtSelect.innerHTML = metaData.vi_tri_mat_tien.map(v => `<option value="${v}">${v}</option>`).join('');

    // Chat luong (for nha pho)
    const clxdsSelect = document.getElementById('chat_luong_xay_dung');
    clxdsSelect.innerHTML = metaData.chat_luong_xay_dung.map(c => `<option value="${c}">${c}</option>`).join('');

    // Chat luong (for biet thu)
    const clxdsBtSelect = document.getElementById('chat_luong_xay_dung_bt');
    clxdsBtSelect.innerHTML = metaData.chat_luong_xay_dung.map(c => `<option value="${c}">${c}</option>`).join('');

    // Loai biet thu
    const lbtSelect = document.getElementById('loai_biet_thu');
    lbtSelect.innerHTML = metaData.loai_biet_thu.map(l => `<option value="${l}">${l}</option>`).join('');

    // View (biet thu)
    const viewBtSelect = document.getElementById('view_bt');
    viewBtSelect.innerHTML = metaData.view.map(v => `<option value="${v}">${v}</option>`).join('');

    // View (can ho)
    const viewChSelect = document.getElementById('view_ch');
    viewChSelect.innerHTML = metaData.view.map(v => `<option value="${v}">${v}</option>`).join('');

    // Du an can ho
    const daSelect = document.getElementById('ten_du_an');
    daSelect.innerHTML = metaData.du_an_can_ho.map((d, i) => `<option value="${i}">${d}</option>`).join('');

    // Vi tri hem
    const vthSelect = document.getElementById('vi_tri_hem');
    vthSelect.innerHTML = metaData.vi_tri_hem.map(v => `<option value="${v}">${v}</option>`).join('');

    // Wards
    updateWards();
}

function updateWards() {
    if (!metaData) return;
    const quan = document.getElementById('quan').value;
    const phuongSelect = document.getElementById('phuong');
    const wards = metaData.wards[quan] || [];
    phuongSelect.innerHTML = wards.map(w => `<option value="${w}">${w}</option>`).join('');
}

function updateForm() {
    const type = document.getElementById('house_type').value;

    document.querySelectorAll('.type-fields').forEach(el => el.style.display = 'none');

    if (type === 'nha_pho') {
        document.getElementById('nha_pho_fields').style.display = 'block';
    } else if (type === 'biet_thu') {
        document.getElementById('biet_thu_fields').style.display = 'block';
    } else if (type === 'can_ho') {
        document.getElementById('can_ho_fields').style.display = 'block';
    } else if (type === 'nha_hem') {
        document.getElementById('nha_hem_fields').style.display = 'block';
    }
}

function getFormData() {
    const type = document.getElementById('house_type').value;
    const data = {
        house_type: type,
        dien_tich: parseFloat(document.getElementById('dien_tich').value),
        quan: document.getElementById('quan').value,
        phuong: document.getElementById('phuong').value,
        so_phong_ngu: parseInt(document.getElementById('so_phong_ngu').value),
        so_phong_tam: parseInt(document.getElementById('so_phong_tam').value),
        so_tang: parseInt(document.getElementById('so_tang').value),
        huong_nha: document.getElementById('huong_nha').value,
        nam_xay_dung: parseInt(document.getElementById('nam_xay_dung').value),
        phap_ly: document.getElementById('phap_ly').value,
        mat_tien: parseFloat(document.getElementById('mat_tien').value),
        khoang_cach_trung_tam: parseFloat(document.getElementById('khoang_cach_trung_tam').value),
    };

    if (type === 'nha_pho') {
        data.do_sau = parseFloat(document.getElementById('do_sau').value);
        data.do_rong_duong = parseFloat(document.getElementById('do_rong_duong').value);
        data.vi_tri_mat_tien = document.getElementById('vi_tri_mat_tien').value;
        data.chat_luong_xay_dung = document.getElementById('chat_luong_xay_dung').value;
        data.co_kinh_doanh = document.getElementById('co_kinh_doanh').checked ? 1 : 0;
        data.co_san_thuong = document.getElementById('co_san_thuong').checked ? 1 : 0;
    } else if (type === 'biet_thu') {
        data.dien_tich_san_vuon = parseFloat(document.getElementById('dien_tich_san_vuon').value);
        data.loai_biet_thu = document.getElementById('loai_biet_thu').value;
        data.view = document.getElementById('view_bt').value;
        data.chat_luong_xay_dung = document.getElementById('chat_luong_xay_dung_bt').value;
        data.co_be_boi = document.getElementById('co_be_boi').checked ? 1 : 0;
        data.co_gara = document.getElementById('co_gara').checked ? 1 : 0;
    } else if (type === 'can_ho') {
        data.tang = parseInt(document.getElementById('tang').value);
        data.tong_so_tang_toa_nha = parseInt(document.getElementById('tong_so_tang_toa_nha').value);
        data.view = document.getElementById('view_ch').value;
        data.ten_du_an = parseInt(document.getElementById('ten_du_an').value);
        data.nam_ban_giao = parseInt(document.getElementById('nam_ban_giao').value);
        data.phi_quan_ly = parseFloat(document.getElementById('phi_quan_ly').value);
        data.co_thang_may = document.getElementById('co_thang_may').checked ? 1 : 0;
        data.co_ham = document.getElementById('co_ham').checked ? 1 : 0;
    } else if (type === 'nha_hem') {
        data.do_rong_hem = parseFloat(document.getElementById('do_rong_hem').value);
        data.vi_tri_hem = document.getElementById('vi_tri_hem').value;
        data.do_rong_duong_chinh = parseFloat(document.getElementById('do_rong_duong_chinh').value);
        data.khoang_cach_ra_duong_chinh = parseFloat(document.getElementById('khoang_cach_ra_duong_chinh').value);
        data.co_oto_vao_hem = document.getElementById('co_oto_vao_hem').checked ? 1 : 0;
    }

    return data;
}

async function predict() {
    const btn = document.getElementById('predictBtn');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');

    btn.disabled = true;
    resultDiv.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        const data = getFormData();

        const res = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        let result;
        try {
            result = await res.json();
        } catch (err) {
            throw new Error('Invalid response from server');
        }

        if (!res.ok) {
            const errMsg = result?.error || result?.detail || result?.message || 'Loi khong xac dinh';
            throw new Error(errMsg);
        }

        const priceVndNum = result.price_vnd != null ? Number(result.price_vnd) : (result.price_billion != null ? Math.round(Number(result.price_billion) * 1e9) : null);
        const priceBillion = result.price_billion != null ? Number(result.price_billion) : (priceVndNum != null ? priceVndNum / 1e9 : null);

        const priceVnd = priceVndNum != null ? priceVndNum.toLocaleString('vi-VN') : 'N/A';
        const priceBillionDisplay = priceBillion != null ? Number(priceBillion).toLocaleString('vi-VN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : 'N/A';

        const giaPerM2 = (priceBillion != null && data.dien_tich > 0) ? (priceBillion * 1000 / data.dien_tich).toLocaleString('vi-VN', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) : 'N/A';

        const modelName = result.model_used ? result.model_used.replace('_model.pkl', '').replace(/_/g, ' ') : 'N/A';
        const type = data.house_type;

        const detailItems = [
            ['Dien tich', data.dien_tich + ' m2'],
            ['Quan', data.quan],
            ['Phuong', data.phuong],
            ['Phong ngu', data.so_phong_ngu],
            ['Phong tam', data.so_phong_tam],
            ['So tang', data.so_tang],
            ['Huong nha', data.huong_nha],
            ['Nam xay dung', data.nam_xay_dung],
            ['Phap ly', data.phap_ly],
            ['Mat tien', data.mat_tien + ' m'],
            ['Khoang cach TT', data.khoang_cach_trung_tam + ' km'],
        ];

        if (type === 'nha_pho') {
            detailItems.push(
                ['Do sau', data.do_sau + ' m'],
                ['Do rong duong', data.do_rong_duong + ' m'],
                ['Vi tri mat tien', data.vi_tri_mat_tien],
                ['Chat luong xay dung', data.chat_luong_xay_dung],
                ['Kinh doanh', data.co_kinh_doanh ? 'Co' : 'Khong'],
                ['San thuong', data.co_san_thuong ? 'Co' : 'Khong'],
            );
        } else if (type === 'biet_thu') {
            detailItems.push(
                ['Dien tich san vuon', data.dien_tich_san_vuon + ' m2'],
                ['Loai biet thu', data.loai_biet_thu],
                ['View', data.view],
                ['Chat luong xay dung', data.chat_luong_xay_dung],
                ['Be boi', data.co_be_boi ? 'Co' : 'Khong'],
                ['Gara', data.co_gara ? 'Co' : 'Khong'],
            );
        } else if (type === 'can_ho') {
            const duAnEl = document.getElementById('ten_du_an');
            const duAnName = duAnEl.options[duAnEl.selectedIndex]?.text || 'N/A';
            detailItems.push(
                ['Tang hien tai', data.tang],
                ['Tong so tang', data.tong_so_tang_toa_nha],
                ['View', data.view],
                ['Du an', duAnName],
                ['Nam ban giao', data.nam_ban_giao],
                ['Phi quan ly', data.phi_quan_ly + ' nghin/m2/thang'],
                ['Thang may', data.co_thang_may ? 'Co' : 'Khong'],
                ['Ham', data.co_ham ? 'Co' : 'Khong'],
            );
        } else if (type === 'nha_hem') {
            detailItems.push(
                ['Do rong hem', data.do_rong_hem + ' m'],
                ['Vi tri hem', data.vi_tri_hem],
                ['Do rong duong chinh', data.do_rong_duong_chinh + ' m'],
                ['Khoang cach ra duong', data.khoang_cach_ra_duong_chinh + ' m'],
                ['O to vao hem', data.co_oto_vao_hem ? 'Duoc' : 'Khong'],
            );
        }

        const detailRows = detailItems.map(([label, value]) =>
            `<div class="detail-row"><span class="detail-label">${label}</span><span class="detail-value">${value}</span></div>`
        ).join('');

        resultDiv.innerHTML = `
            <div class="result-content">
                <div class="result-header">
                    <span class="result-type-badge">${TYPE_NAMES[result.house_type || data.house_type]}</span>
                    <span class="result-model-badge">Model: ${modelName}</span>
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
        resultDiv.innerHTML = `<div class="error"><p>Loi: ${e.message}</p></div>`;
        resultDiv.classList.remove('hidden');
    } finally {
        btn.disabled = false;
        loadingDiv.classList.add('hidden');
    }
}

// Init
window.onload = function() {
    loadMeta();
    updateForm();
};
