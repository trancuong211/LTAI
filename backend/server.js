/**
 * Node.js Server - AI Du Doan Gia Nha HCM
 * Su dung Express + goi Python predict qua subprocess
 */
const express = require('express');
const cors = require('cors');
const path = require('path');
const { execFile } = require('child_process');
const { preprocessInput } = require('./preprocessing');

const app = express();
// Default to 8001 to avoid common port conflicts; can be overridden with PORT env var
const PORT = process.env.PORT || 8001;

app.use(cors());
app.use(express.json());

// Serve frontend
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// Meta data
app.get('/meta', (req, res) => {
    const { DISTRICTS, HUONG, PHAP_LY, VI_TRI_MAT_TIEN, CHAT_LUONG_XAY_DUNG,
            LOAI_BIET_THU, VIEW_TYPES, VI_TRI_HEM, WARDS } = require('./preprocessing');

    const DU_AN_CAN_HO = [
        "Vinhomes Grand Park", "Sunrise City", "The Estella", "Masteri Thao Dien",
        "Saigon Pearl", "Vinci Grand Plaza", "The Sun Avenue", "Icon 56",
        "Saigon Royal", "D'Edge", "City Garden", "Midtown", "Charmington",
        "SC VivoCity", "Centre Mall", "Happy Valley", "Millennium"
    ];

    res.json({
        districts: DISTRICTS,
        wards: Object.fromEntries(
            Object.entries(WARDS).map(([k, v]) => [k, v.slice(0, 3).concat(['...'])])
        ),
        huong: HUONG,
        phap_ly: PHAP_LY,
        vi_tri_mat_tien: VI_TRI_MAT_TIEN,
        chat_luong_xay_dung: CHAT_LUONG_XAY_DUNG,
        loai_biet_thu: LOAI_BIET_THU,
        view: VIEW_TYPES,
        vi_tri_hem: VI_TRI_HEM,
        du_an_can_ho: DU_AN_CAN_HO,
    });
});

// Predict endpoint
app.post('/predict', (req, res) => {
    try {
        const { house_type } = req.body;

        if (!house_type || !['nha_pho', 'biet_thu', 'can_ho', 'nha_hem'].includes(house_type)) {
            return res.status(400).json({ error: 'Invalid house_type' });
        }

        // Preprocess input
        const features = preprocessInput(req.body, house_type);

        // Goi Python predict script
        const scriptPath = path.join(__dirname, '..', 'predict_cli.py');
        const args = [scriptPath, house_type, JSON.stringify(features)];

        execFile('python', args, { timeout: 30000 }, (error, stdout, stderr) => {
            if (error) {
                console.error('Python error:', stderr);
                return res.status(500).json({ error: 'Prediction failed', detail: stderr });
            }

            try {
                const result = JSON.parse(stdout);
                if (result.error) {
                    return res.status(500).json({ error: result.error });
                }
                res.json(result);
            } catch (e) {
                // Parse output manually
                const lines = stdout.trim().split('\n');
                const priceMatch = lines.find(l => l.includes('ty VND'));
                const price = priceMatch ? parseFloat(priceMatch.match(/[\d.]+/)[0]) : 0;

                res.json({
                    price_billion: price,
                    price_vnd: Math.round(price * 1e9),
                    model_used: `${house_type}_model.pkl`,
                    house_type: house_type
                });
            }
        });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', version: '2.0.0' });
});

// Start server
app.listen(PORT, () => {
    console.log(`\n  AI Du Doan Gia Nha HCM - Node.js Server`);
    console.log(`  http://localhost:${PORT}\n`);
});
