# TSTS Trade Analyzer Bot
# Upload a chart screenshot → Get trade type, entry, stop loss, take profit
# Based on The Safety Trade System (TSTS) by Kevin Grego

import os
import json
import base64
import subprocess
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

MIMO_API = "/root/.openclaw/skills/mimo-omni/mimo_api.sh"

HTML_TEMPLATE = r"""
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
        .trade-uno { background: #2a1a3a; color: #bc8cff; border: 1px solid #8957e5; }
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

        .raw-toggle {
            margin-top: 15px;
            text-align: center;
        }
        .raw-toggle button {
            background: none;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
        }
        .raw-toggle button:hover { border-color: #58a6ff; color: #58a6ff; }
        #rawResponse {
            display: none;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 0.8rem;
            color: #8b949e;
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>&#x1F4CA; TSTS Trade Analyzer</h1>
        <p class="subtitle">Upload a TradingView chart screenshot &rarr; Get trade type, entry, stop loss, take profit</p>

        <div class="upload-zone" id="uploadZone">
            <div class="icon">&#x1F4F7;</div>
            <p>Drop a chart screenshot here or click to upload</p>
            <p style="font-size: 0.8rem; margin-top: 8px; color: #484f58;">Supports PNG, JPG, JPEG</p>
            <input type="file" id="fileInput" accept="image/*">
        </div>

        <img id="preview" alt="Chart preview">
        <button class="btn-analyze" id="analyzeBtn" onclick="analyzeChart()">&#x1F50D; Analyze Trade</button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing chart indicators...</p>
        </div>

        <div class="result-card" id="resultCard">
            <h2>&#x1F4CB; Trade Analysis</h2>
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
                    <div class="label">&#x1F4CD; Entry</div>
                    <div class="value entry-color" id="entry">-</div>
                </div>
                <div class="detail-box">
                    <div class="label">&#x1F6D1; Stop Loss</div>
                    <div class="value stop-color" id="stopLoss">-</div>
                </div>
                <div class="detail-box" style="grid-column: 1 / -1;">
                    <div class="label">&#x1F3AF; Take Profit</div>
                    <div class="value tp-color" id="takeProfit">-</div>
                </div>
            </div>
            <h2 style="margin-top: 20px;">&#x2705; Indicator Checklist</h2>
            <ul class="checklist" id="checklist"></ul>
            <h2 style="margin-top: 20px;">&#x1F4DD; Analysis Notes</h2>
            <p id="notes" style="color: #8b949e; line-height: 1.6;"></p>
            <div class="raw-toggle">
                <button onclick="toggleRaw()">Show Raw AI Response</button>
            </div>
            <pre id="rawResponse"></pre>
        </div>

        <div class="disclaimer">
            &#x26A0;&#xFE0F; DEMO TRADE ONLY. NOT FINANCIAL ADVICE. This bot analyzes charts based on TSTS indicator patterns.<br>
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
            analyzeBtn.textContent = '\u23F3 Analyzing...';
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
            analyzeBtn.textContent = '\u{1F50D} Analyze Trade';
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
                li.innerHTML = '<span class="icon">' + (item.status === 'check' ? '\u2705' : item.status === 'fail' ? '\u274C' : '\u2B1C') + '</span> ' + item.text;
                checklist.appendChild(li);
            });

            document.getElementById('notes').textContent = data.notes || '';
            document.getElementById('rawResponse').textContent = data.raw_response || '';
        }

        function toggleRaw() {
            const el = document.getElementById('rawResponse');
            el.style.display = el.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>
"""

# ── TSTS Analysis Rules ──────────────────────────────────────────────────

TSTS_SYSTEM_PROMPT = """You are a TSTS (The Safety Trade System) chart analyzer created by Kevin Grego. Analyze the uploaded TradingView chart screenshot and identify which trade setup is present.

CHART LAYOUT: TSTS charts typically show 2-4 timeframes side by side (e.g., 30s, 2m, 15m, 1h). Each panel has candlesticks with moving average lines, a histogram (BS Detector), and oscillator lines at the bottom. Some charts also include the "UNO REVERSE STEROID" dashboard at the top showing signal arrows for US30, NAS100, NQ1!, SPX500, ES1! across timeframes.

LINES ON CHART (top to bottom of each panel):
- Yellow Line = fast EMA (shortest period, closest to price). Conservative entry trigger. If price is above it = bullish, below = bearish.
- Gold Line = medium EMA (sits above/below Yellow). Aggressive entry trigger. Reversal warning when price interacts with it.
- Blue Line = slow EMA / anchor line. Acts as gravity/magnet for price. PRIMARY TARGET for most trades. Price crossing above Blue Line = significant bullish signal. Price below Blue Line on higher TF = macro trend still bearish.
- Pink/Purple Bands = volatility channel around price (like Bollinger Bands). Pink = upper band, Purple = lower band. Price touching Pink = potentially overextended up. Touching Purple = overextended down.

BOTTOM SECTION (Sniper Oscillator):
- Pink Line = fastest momentum line. Oversold pinned low (0-20), overbought pinned high (80-100). LEADS the move.
- Purple Line = "where price will REALLY move with confirmation." Confirms true direction after Pink leads.
- Blue Line (oscillator) = anchor/target. Gravity for price. Primary target.
- Orange Line = ENTRY TRIGGER. Rule: candle closes above Orange Line (long) or below (short) -> enter next candle on Orange Line.
- 10 orange EMA crossing 30 EMA = EXACT ENTRY SIGNAL (bearish: 10 crosses below 30; bullish: 10 crosses above 30).
- Higher TF entry line carries to lower TF UNCHANGED — do not move the line when scaling down.
- Key signals: Pink crosses Purple = momentum shift confirmed. Blue pulling up/down = continuation confirmed.
- On higher TF: Pink moves are big (200+ pts on 1hr). On lower TF: don't wait for Pink, use Purple earlier per Kevin's live update.

MULTI-TIMEFRAME ENTRY FRAMEWORK:
- Logo/SS forms on higher TF, enter on lower TF Blue Line:
  * 4hr/Daily setup -> enter on 15min Blue Line
  * 30min/1hour setup -> enter on 3min Blue Line
  * 1hr/15min setup -> enter on 5min Blue Line
  * 15min/1hour setup -> enter on 1min Blue Line
  * 5min/15min setup -> enter on 30sec Blue Line
- Logo Sell-Off Pattern: price overshoots lower TF Blue Line up -> comes back down -> goes under BL -> taps underside (now resistance) -> sells off = SS entry
- Logo Buy-Off Pattern: price undershoots lower TF Blue Line down -> comes back up -> goes over BL -> taps topside (now support) -> rallies = BS entry

HISTOGRAMS (middle of each panel):
- BS Detector = colored histogram bars. Green bars = bullish momentum. Red bars = bearish momentum. Rising bars = momentum increasing. Falling/shortening bars = momentum fading. Yellow signal line overlay.
- Bokk (Block) = same as histogram. Green and expanding = institutional buying momentum entering. Red and expanding = institutional selling. Tapering/shrinking = momentum exhausting, pullback coming.

DIRECTIONAL BARS / 3LINES:
- Small bars at the very bottom of the panel (or on dashboard).
- Solid GREEN = macro bullish bias (higher timeframes aligned up).
- Solid RED = macro bearish bias (higher timeframes aligned down).
- Mixed/choppy = NO-TRADE ZONE, timeframes disagree.

UNO REVERSE DASHBOARD (if present):
- Matrix of colored arrows: Green UP arrows = price above Blue Line on that timeframe. Red DOWN arrows = price below Blue Line.
- Shows all 5 indices (US30, NAS, NQ1, SPX, ES1) across timeframes.
- Sequential flip pattern: timeframes turn green in ascending order (1s -> 5s -> 10s -> 15s -> ...) during reversals.
- Oreo Cookie pattern: higher TFs green, middle TFs red, lower TFs turning green = reversal loading.

TRADE TYPE IDENTIFICATION:

1. GGG RGG (Safety Trade) - LONG:
   READ BOTTOM-UP:
   - Layer 1: Directional Bars = SOLID GREEN (if mixed, NO TRADE)
   - Layer 2: BS Detector = was RED/dimming (Reset phase), now turning GREEN
   - Layer 3: Bokk/Histogram = Opening/expanding GREEN
   - Layer 4: Candle EMA = GREEN (price above Yellow and Gold lines)
   - Entry: Buy Stop at Gold Line (aggressive) or Yellow Line (conservative)
   - Stop: Below swing low where trend reversed
   - Target: Higher timeframe Blue Line

2. RRR G RR (Safety Trade) - SHORT:
   READ BOTTOM-UP:
   - Layer 1: Directional Bars = SOLID RED
   - Layer 2: BS Detector = was GREEN/dimming (Reset), now turning RED
   - Layer 3: Bokk = Opening/expanding RED
   - Layer 4: Candle EMA = RED (price below Yellow and Gold)
   - Entry: Sell Stop at Gold Line (aggressive) or Yellow Line (conservative)
   - Stop: Above swing high where trend reversed
   - Target: Higher timeframe Blue Line

3. BLUE LINE TRADE:
   - Price has crossed above (long) or below (short) the Blue Line
   - Gap between Yellow Line and BS histogram on middle timeframe
   - Bokk tapering or changing color
   - Lower timeframes already turning green (long) or red (short)
   - Entry: Buy/Sell Stop at Gold Line or Yellow Line
   - Target: Blue Line on execution timeframe

4. LOGO TRADE:
   - V shape on histogram (long) or inverted V/Mountain (short)
   - Directional Bars bright green (long) or bright red (short)
   - BS shows dimming/reset
   - Entry: Buy/Sell Stop at Gold or Yellow Line
   - Stop: Bottom of V (long) or peak of Mountain (short)

5. UNO REVERSE (Keith Bot):
   - Dashboard shows timeframes flipping red to green sequentially
   - Oreo pattern visible: higher TFs green, middle TFs red, lower TFs green
   - Four indices green + one lagging on trigger timeframe
   - Entry: Buy Stop on lagging symbol
   - Target: Blue Line of trigger timeframe

CRITICAL RULES:
- ALWAYS read from bottom up: Directional Bars -> BS Detector -> Bokk -> Candle/Price position
- If Directional Bars are mixed = NO TRADE, set confidence low
- Check ALL visible timeframes: higher TF trend controls lower TF trades
- Counter-trend (fast TF green, slow TF red) = lower confidence, shorter targets
- Full alignment across all TFs = highest confidence
- "When one goes up, they all go up. When one goes down, they all go down."

Return STRICT JSON only:
{
  "trade_type": "GGG RGG (Safety Trade - LONG)" | "RRR G RR (Safety Trade - SHORT)" | "Blue Line Trade" | "Logo Trade" | "Uno Reverse (Keith Bot)" | "Unknown",
  "trade_class": "trade-ggg" | "trade-blueline" | "trade-logo" | "trade-uno" | "trade-unknown",
  "direction": "LONG" | "SHORT" | "-",
  "entry": "specific entry instruction with price level if visible",
  "stop_loss": "specific stop loss instruction",
  "take_profit": "TP1, TP2, TP3 targets if visible",
  "confidence": 0-100,
  "checklist": [{"text": "indicator name + status", "status": "check"|"uncheck"|"fail"}],
  "notes": "observations, warnings, multi-timeframe context"
}

Return ONLY the JSON object. No markdown fences."""


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
    try:
        result = subprocess.run(
            ['bash', MIMO_API, 'image', img_path, TSTS_SYSTEM_PROMPT],
            capture_output=True, text=True, timeout=120,
            env={**os.environ}
        )
        output = result.stdout.strip()
    except subprocess.TimeoutExpired:
        return jsonify({
            'trade_type': 'Analysis Timeout',
            'trade_class': 'trade-unknown',
            'direction': '-',
            'entry': '-',
            'stop_loss': '-',
            'take_profit': '-',
            'confidence': 0,
            'checklist': [],
            'notes': 'Analysis timed out after 120 seconds. Try a smaller or clearer image.'
        })
    except Exception as e:
        return jsonify({
            'trade_type': 'Analysis Error',
            'trade_class': 'trade-unknown',
            'direction': '-',
            'entry': '-',
            'stop_loss': '-',
            'take_profit': '-',
            'confidence': 0,
            'checklist': [],
            'notes': f'Error: {str(e)}'
        })

    # Try to extract JSON from the response
    analysis = None
    try:
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            analysis = json.loads(output[json_start:json_end])
    except (json.JSONDecodeError, ValueError):
        pass

    if not analysis:
        analysis = {
            'trade_type': 'Unknown',
            'trade_class': 'trade-unknown',
            'direction': '-',
            'entry': '-',
            'stop_loss': '-',
            'take_profit': '-',
            'confidence': 0,
            'checklist': [],
            'notes': 'Could not parse AI response. See raw output below.',
            'raw_response': output[:1000]
        }
    else:
        analysis['raw_response'] = output

    return jsonify(analysis)


if __name__ == '__main__':
    print("TSTS Trade Analyzer starting on http://0.0.0.0:7860")
    app.run(host='0.0.0.0', port=7860, debug=False)
