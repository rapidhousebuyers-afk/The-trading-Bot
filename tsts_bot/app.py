# TSTS Trade Analyzer Bot
# Upload a chart screenshot → Get trade type, entry, stop loss, take profit

import os
import json
import base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TSTS Trade Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0d1117;
            color: #e6edf3;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 5px;
            color: #58a6ff;
        }
        .subtitle {
            text-align: center;
            color: #8b949e;
            margin-bottom: 30px;
            font-size: 0.9rem;
        }
        .upload-zone {
            border: 2px dashed #30363d;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #161b22;
            margin-bottom: 20px;
        }
        .upload-zone:hover, .upload-zone.dragover {
            border-color: #58a6ff;
            background: #1c2333;
        }
        .upload-zone p { color: #8b949e; font-size: 1rem; }
        .upload-zone .icon { font-size: 3rem; margin-bottom: 10px; }
        #fileInput { display: none; }
        #preview {
            max-width: 100%;
            max-height: 400px;
            border-radius: 8px;
            margin: 15px auto;
            display: none;
        }
        .btn-analyze {
            display: none;
            width: 100%;
            padding: 14px;
            background: #238636;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
            margin-bottom: 20px;
        }
        .btn-analyze:hover { background: #2ea043; }
        .btn-analyze:disabled { background: #21262d; color: #484f58; cursor: wait; }

        .result-card {
            display: none;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .result-card h2 {
            color: #58a6ff;
            font-size: 1.3rem;
            margin-bottom: 15px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
        }
        .trade-type {
            font-size: 1.6rem;
            font-weight: 700;
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .trade-ggg { background: #1a3a2a; color: #3fb950; border: 1px solid #238636; }
        .trade-blueline { background: #1a2a3a; color: #58a6ff; border: 1px solid #1f6feb; }
        .trade-logo { background: #3a2a1a; color: #d29922; border: 1px solid #9e6a03; }
        .trade-unknown { background: #2d1a1a; color: #f85149; border: 1px solid #da3633; }

        .detail-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        @media (max-width: 600px) {
            .detail-grid { grid-template-columns: 1fr; }
        }
        .detail-box {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
        }
        .detail-box .label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #8b949e;
            margin-bottom: 5px;
        }
        .detail-box .value {
            font-size: 1.2rem;
            font-weight: 600;
        }
        .entry-color { color: #3fb950; }
        .stop-color { color: #f85149; }
        .tp-color { color: #58a6ff; }
        .direction-color { color: #d29922; }

        .checklist { list-style: none; margin-top: 15px; }
        .checklist li {
            padding: 8px 0;
            border-bottom: 1px solid #21262d;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .checklist li:last-child { border: none; }
        .check .icon { color: #3fb950; }
        .uncheck .icon { color: #484f58; }
        .fail .icon { color: #f85149; }

        .confidence-bar {
            height: 6px;
            background: #21262d;
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }
        .confidence-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.5s;
        }
        .conf-high { background: #3fb950; }
        .conf-med { background: #d29922; }
        .conf-low { background: #f85149; }

        .disclaimer {
            text-align: center;
            color: #484f58;
            font-size: 0.75rem;
            margin-top: 30px;
            padding: 15px;
            border-top: 1px solid #21262d;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }
        .spinner {
            border: 3px solid #30363d;
            border-top: 3px solid #58a6ff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 TSTS Trade Analyzer</h1>
        <p class="subtitle">Upload a chart screenshot → Get trade type, entry, stop loss, take profit</p>

        <div class="upload-zone" id="uploadZone">
            <div class="icon">📷</div>
            <p>Drop a chart screenshot here or click to upload</p>
            <p style="font-size: 0.8rem; margin-top: 8px; color: #484f58;">Supports PNG, JPG, JPEG</p>
            <input type="file" id="fileInput" accept="image/*">
        </div>

        <img id="preview" alt="Chart preview">
        <button class="btn-analyze" id="analyzeBtn" onclick="analyzeChart()">🔍 Analyze Trade</button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing chart indicators...</p>
        </div>

        <div class="result-card" id="resultCard">
            <h2>📋 Trade Analysis</h2>
            <div id="tradeTypeBox" class="trade-type"></div>
            <div class="detail-grid">
                <div class="detail-box">
                    <div class="label">Direction</div>
                    <div class="value direction-color" id="direction">-</div>
                </div>
                <div class="detail-box">
                    <div class="label">Confidence</div>
                    <div class="value" id="confidence">-</div>
                    <div class="confidence-bar"><div class="confidence-fill" id="confBar"></div></div>
                </div>
                <div class="detail-box">
                    <div class="label">📍 Entry</div>
                    <div class="value entry-color" id="entry">-</div>
                </div>
                <div class="detail-box">
                    <div class="label">🛑 Stop Loss</div>
                    <div class="value stop-color" id="stopLoss">-</div>
                </div>
                <div class="detail-box" style="grid-column: 1 / -1;">
                    <div class="label">🎯 Take Profit</div>
                    <div class="value tp-color" id="takeProfit">-</div>
                </div>
            </div>
            <h2 style="margin-top: 20px;">✅ Indicator Checklist</h2>
            <ul class="checklist" id="checklist"></ul>
            <h2 style="margin-top: 20px;">📝 Analysis Notes</h2>
            <p id="notes" style="color: #8b949e; line-height: 1.6;"></p>
        </div>

        <div class="disclaimer">
            ⚠️ DEMO TRADE ONLY. NOT FINANCIAL ADVICE. This bot analyzes charts based on TSTS indicator patterns.<br>
            Always verify signals manually before placing real trades.
        </div>
    </div>

    <script>
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const preview = document.getElementById('preview');
        const analyzeBtn = document.getElementById('analyzeBtn');

        uploadZone.addEventListener('click', () => fileInput.click());
        uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragover'); });
        uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', (e) => { if (e.target.files.length) handleFile(e.target.files[0]); });

        function handleFile(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                preview.style.display = 'block';
                analyzeBtn.style.display = 'block';
                document.getElementById('resultCard').style.display = 'none';
            };
            reader.readAsDataURL(file);
        }

        async function analyzeChart() {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '⏳ Analyzing...';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('resultCard').style.display = 'none';

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: preview.src })
                });
                const data = await response.json();
                displayResult(data);
            } catch (err) {
                alert('Error analyzing chart: ' + err.message);
            }

            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '🔍 Analyze Trade';
            document.getElementById('loading').style.display = 'none';
        }

        function displayResult(data) {
            const card = document.getElementById('resultCard');
            card.style.display = 'block';

            const typeBox = document.getElementById('tradeTypeBox');
            typeBox.textContent = data.trade_type || 'Unknown';
            typeBox.className = 'trade-type ' + (data.trade_class || 'trade-unknown');

            document.getElementById('direction').textContent = data.direction || '-';
            document.getElementById('entry').textContent = data.entry || '-';
            document.getElementById('stopLoss').textContent = data.stop_loss || '-';
            document.getElementById('takeProfit').textContent = data.take_profit || '-';

            const conf = data.confidence || 0;
            document.getElementById('confidence').textContent = conf + '%';
            const bar = document.getElementById('confBar');
            bar.style.width = conf + '%';
            bar.className = 'confidence-fill ' + (conf >= 70 ? 'conf-high' : conf >= 40 ? 'conf-med' : 'conf-low');

            const checklist = document.getElementById('checklist');
            checklist.innerHTML = '';
            (data.checklist || []).forEach(item => {
                const li = document.createElement('li');
                li.className = item.status;
                li.innerHTML = `<span class="icon">${item.status === 'check' ? '✅' : item.status === 'fail' ? '❌' : '⬜'}</span> ${item.text}`;
                checklist.appendChild(li);
            });

            document.getElementById('notes').textContent = data.notes || '';
        }
    </script>
</body>
</html>
"""

# TSTS Analysis Rules
TSTS_RULES = """
You are a TSTS (The Safety Trade System) chart analyzer. Analyze the uploaded TradingView chart screenshot and identify which trade setup is present.

TRADE TYPES TO IDENTIFY:

1. GGG RGG (Safety Trade) — LONG:
   - Directional Bars (3Lines at bottom): Solid GREEN
   - BS Detector: RED and Dimming (Reset phase)
   - Bokk: Opening GREEN
   - Candle EMA: GREEN
   - Entry: Buy Stop at Gold Line (aggressive) or Yellow Line (conservative)
   - Stop: Just below the swing low where trend reversed
   - Target: Previous local high or higher timeframe Blue Line

2. RRR G RR (Safety Trade) — SHORT:
   - Directional Bars: Solid RED
   - BS Detector: GREEN and Dimming (Reset phase)
   - Bokk: Opening RED
   - Candle EMA: RED
   - Entry: Sell Stop at Gold Line (aggressive) or Yellow Line (conservative)
   - Stop: Just above the swing high where trend reversed
   - Target: Previous local low or higher timeframe Blue Line

3. BLUE LINE TRADE:
   - Multi-timeframe strength visible
   - Gap between Yellow Line and BS on middle timeframe
   - Bokk tapering or changing color
   - Lower timeframe turning green (long) or red (short)
   - Entry: Buy/Sell Stop at Gold Line or Yellow Line
   - Stop: Beyond swing point
   - Target: Blue Line on execution timeframe

4. LOGO TRADE:
   - Clean V shape (long) or Inverted V / Mountain shape (short) on candle indicators
   - Directional Bars bright green (long) or bright red (short)
   - BS shows Dimming (Reset)
   - Entry: Buy/Sell Stop at Gold Line or Yellow Line
   - Stop: Bottom of V (long) or Peak of Mountain (short)
   - Target: Momentum loss — watch lower TF for color turn

KEY VISUAL INDICATORS ON CHART:
- Lines: Yellow (conservative entry), Gold (aggressive entry), Blue (target/gravity)
- BS Detector: Shows as colored bars/line — bright = momentum alive, dimming = reset
- Bokk: Cloud/bar that expands (opening) or tapers (closing)
- Histo3: Histogram bars — V or Mountain patterns
- 3Lines/Directional Bars: Bars at very bottom — solid green or red
- Pink Lines: Fast momentum — pinned at extremes = overextended
- Orange Lines: Take profit targets

If you cannot clearly identify the setup, say so. Be specific about what you see and what's missing.

Return your analysis as JSON with these fields:
- trade_type: "GGG RGG (Safety Trade - LONG)" or "RRR G RR (Safety Trade - SHORT)" or "Blue Line Trade" or "Logo Trade" or "Unknown"
- trade_class: "trade-ggg" or "trade-blueline" or "trade-logo" or "trade-unknown"
- direction: "LONG" or "SHORT"
- entry: specific entry instruction (e.g., "Buy Stop at Gold Line — 42,180" or "Sell Stop at Yellow Line")
- stop_loss: specific stop loss instruction
- take_profit: specific take profit targets (TP1, TP2, TP3 if visible)
- confidence: 0-100
- checklist: array of {text, status} where status is "check", "uncheck", or "fail"
- notes: any additional observations or warnings
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data.get('image', '')

    # Extract base64 image data
    if ',' in image_data:
        image_b64 = image_data.split(',')[1]
    else:
        image_b64 = image_data

    # Save image temporarily
    img_path = '/tmp/tsts_chart.png'
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(image_b64))

    # Call mimo-omni for analysis
    import subprocess
    result = subprocess.run(
        ['bash', '/root/.mi/.openclaw/skills/mimo-omni/mimo_api.sh',
         'image', img_path,
         TSTS_RULES + '\n\nAnalyze this chart and return ONLY valid JSON.'],
        capture_output=True, text=True, timeout=120,
        env={**os.environ}
    )

    output = result.stdout.strip()

    # Try to extract JSON from the response
    try:
        # Find JSON in the response
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            analysis = json.loads(output[json_start:json_end])
        else:
            raise ValueError("No JSON found in response")
    except (json.JSONDecodeError, ValueError):
        # Fallback: return raw analysis
        analysis = {
            'trade_type': 'Analysis Error',
            'trade_class': 'trade-unknown',
            'direction': '-',
            'entry': '-',
            'stop_loss': '-',
            'take_profit': '-',
            'confidence': 0,
            'checklist': [],
            'notes': f'Raw response: {output[:500]}'
        }

    return jsonify(analysis)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False)
