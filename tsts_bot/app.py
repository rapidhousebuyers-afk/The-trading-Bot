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
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 5px; color: #58a6ff; }
        .subtitle { text-align: center; color: #8b949e; margin-bottom: 30px; font-size: 0.9rem; }
        .upload-zone {
            border: 2px dashed #30363d; border-radius: 12px; padding: 40px;
            text-align: center; cursor: pointer; transition: all 0.3s;
            background: #161b22; margin-bottom: 20px;
        }
        .upload-zone:hover, .upload-zone.dragover { border-color: #58a6ff; background: #1c2333; }
        .upload-zone p { color: #8b949e; font-size: 1rem; }
        .upload-zone .icon { font-size: 3rem; margin-bottom: 10px; }
        #fileInput { display: none; }
        #preview { max-width: 100%; max-height: 400px; border-radius: 8px; margin: 15px auto; display: none; }
        .btn-analyze {
            display: none; width: 100%; padding: 14px; background: #238636; color: white;
            border: none; border-radius: 8px; font-size: 1.1rem; font-weight: 600;
            cursor: pointer; transition: background 0.3s; margin-bottom: 20px;
        }
        .btn-analyze:hover { background: #2ea043; }
        .btn-analyze:disabled { background: #21262d; color: #484f58; cursor: wait; }
        .result-card {
            display: none; background: #161b22; border: 1px solid #30363d;
            border-radius: 12px; padding: 25px; margin-bottom: 20px;
        }
        .result-card h2 { color: #58a6ff; font-size: 1.3rem; margin-bottom: 15px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
        .trade-type { font-size: 1.6rem; font-weight: 700; text-align: center; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .trade-ggg { background: #1a3a2a; color: #3fb950; border: 1px solid #238636; }
        .trade-blueline { background: #1a2a3a; color: #58a6ff; border: 1px solid #1f6feb; }
        .trade-logo { background: #3a2a1a; color: #d29922; border: 1px solid #9e6a03; }
        .trade-uno { background: #2a1a3a; color: #bc8cff; border: 1px solid #8957e5; }
        .trade-unknown { background: #2d1a1a; color: #f85149; border: 1px solid #da3633; }
        .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        @media (max-width: 600px) { .detail-grid { grid-template-columns: 1fr; } }
        .detail-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; }
        .detail-box .label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #8b949e; margin-bottom: 5px; }
        .detail-box .value { font-size: 1.2rem; font-weight: 600; }
        .entry-color { color: #3fb950; }
        .stop-color { color: #f85149; }
        .tp-color { color: #58a6ff; }
        .direction-color { color: #d29922; }
        .checklist { list-style: none; margin-top: 15px; }
        .checklist li { padding: 8px 0; border-bottom: 1px solid #21262d; display: flex; align-items: center; gap: 10px; }
        .checklist li:last-child { border: none; }
        .check .icon { color: #3fb950; }
        .uncheck .icon { color: #484f58; }
        .fail .icon { color: #f85149; }
        .confidence-bar { height: 6px; background: #21262d; border-radius: 3px; margin-top: 8px; overflow: hidden; }
        .confidence-fill { height: 100%; border-radius: 3px; transition: width 0.5s; }
        .conf-high { background: #3fb950; }
        .conf-med { background: #d29922; }
        .conf-low { background: #f85149; }
        .disclaimer { text-align: center; color: #484f58; font-size: 0.75rem; margin-top: 30px; padding: 15px; border-top: 1px solid #21262d; }
        .loading { display: none; text-align: center; padding: 30px; }
        .spinner { border: 3px solid #30363d; border-top: 3px solid #58a6ff; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .raw-toggle { margin-top: 15px; text-align: center; }
        .raw-toggle button { background: none; border: 1px solid #30363d; color: #8b949e; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; }
        .raw-toggle button:hover { border-color: #58a6ff; color: #58a6ff; }
        #rawResponse { display: none; background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-top: 10px; white-space: pre-wrap; font-family: monospace; font-size: 0.8rem; color: #8b949e; max-height: 300px; overflow-y: auto; }
        .all-trades { margin-top: 20px; }
        .all-trades h3 { color: #8b949e; font-size: 0.9rem; margin-bottom: 10px; }
        .other-trade { background: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
        .other-trade .name { font-weight: 600; color: #c9d1d9; }
        .other-trade .conf { color: #8b949e; font-size: 0.85rem; }
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
            <h2>&#x1F3AF; Highest Probability Trade</h2>
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
            <div class="all-trades" id="allTradesSection" style="display:none;">
                <h3>All Trades Detected</h3>
                <div id="allTrades"></div>
            </div>
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
            // Show other detected trades
            const allTradesSection = document.getElementById('allTradesSection');
            const allTradesDiv = document.getElementById('allTrades');
            allTradesDiv.innerHTML = '';
            if (data.all_trades && data.all_trades.length > 0) {
                allTradesSection.style.display = 'block';
                data.all_trades.forEach(t => {
                    const div = document.createElement('div');
                    div.className = 'other-trade';
                    div.innerHTML = '<span class="name">' + t.trade_type + '</span> <span class="conf">— ' + t.confidence + '% confidence — ' + t.direction + '</span>';
                    allTradesDiv.appendChild(div);
                });
            } else {
                allTradesSection.style.display = 'none';
            }
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

# ── TSTS Analysis System Prompt ──────────────────────────────────────────

TSTS_SYSTEM_PROMPT = """You are a TSTS (The Safety Trade System) chart analyzer created by Kevin Grego. You analyze TradingView chart screenshots and identify trade setups with precision.

IMPORTANT: The Bokk is NOT the histogram. The Bokk is a CHANNEL on the candle pane — two lines (upper and lower) that wrap around the candles. They change color (green/red), expand (open) when institutional momentum enters, and contract (close) when momentum fades. The upper Bokk line turns green in uptrends and red in downtrends.

CHART LAYOUT: TSTS charts show 2-4 timeframes side by side (e.g., 30s, 2m, 15m, 1h). Each panel has three sections stacked vertically.

CANDLE PANE (top of each panel):
- Candlesticks (green/red)
- Gold Line: fast EMA (orange/gold), closest to price. AGGRESSIVE entry trigger.
- Yellow Line: slower EMA (yellow), sits further from price. CONSERVATIVE entry trigger.
- Blue Line: slowest EMA (cyan/light blue), nearly horizontal. PRIMARY TARGET — price is always drawn to it.
- BOKK CHANNEL: Two lines forming an envelope around candles. Upper line = green (bullish) or red (bearish). Lower line = red. Lines expand (open) when institutional momentum builds. Lines contract (close/taper) when momentum fades. Lines cross when trend shifts. THIS IS ON THE CANDLE PANE, NOT THE HISTOGRAM.

HISTOGRAM PANEL (middle of each panel):
- Green/Red histogram bars showing momentum strength and direction
- Yellow signal line overlaid on the bars
- BS DETECTOR: Read the bars like a MACD. Bright green = strong bullish momentum. Dim green = fading bullish (Reset). Bright red = strong bearish. Dim red = fading bearish (Reset). The "R" in GGG RGG = the dimming/reset.
- DIRECTIONAL BARS (3Lines): Small colored bars at the base of histogram. Solid green = macro bullish locked. Solid red = macro bearish locked. Mixed/choppy = NO-TRADE ZONE. IMPORTANT: On fast timeframes (30s, 1m), the Directional Bars are compressed and may appear as a SINGLE BAR instead of three. If it looks like one solid bar, read its color: one solid green bar = bullish, one solid red bar = bearish, mixed colors in one bar = no trade zone. Do not dismiss single-bar Directional Bars — they still carry the same meaning.

SNIPER OSCILLATOR (bottom of each panel):
- Pink Line: fastest momentum, leads the move, shows overbought/oversold (pinned 80-100 = overbought, 0-20 = oversold)
- Purple Line: confirms true direction. Pink crossing Purple = momentum shift confirmed.
- Blue Line: oscillator anchor/target, same gravity concept as candle Blue Line
- Orange Line: entry trigger. Candle closes above = enter long next candle. 10-orange EMA crossing 30 EMA = EXACT ENTRY SIGNAL.

TRADE TYPE IDENTIFICATION RULES:

1. GGG RGG (Safety Trade) — LONG:
   Read BOTTOM-UP:
   - Layer 1: Directional Bars = SOLID GREEN (mixed = NO TRADE)
   - Layer 2: BS Detector = was RED/dimming (Reset), now turning GREEN
   - Layer 3: Bokk = upper channel line turning green, channel opening/expanding
   - Layer 4: Price = above Gold and Yellow Lines
   Entry: Buy Stop at Gold Line (aggressive) or Yellow Line (conservative)
   Stop: Below swing low where trend reversed
   Target: Higher timeframe Blue Line

2. RRR G RR (Safety Trade) — SHORT:
   Read BOTTOM-UP:
   - Layer 1: Directional Bars = SOLID RED
   - Layer 2: BS Detector = was GREEN/dimming (Reset), now turning RED
   - Layer 3: Bokk = upper channel line turning red, channel opening/expanding
   - Layer 4: Price = below Gold and Yellow Lines
   Entry: Sell Stop at Gold Line (aggressive) or Yellow Line (conservative)
   Stop: Above swing high where trend reversed
   Target: Higher timeframe Blue Line

3. BLUE LINE TRADE — LONG:
   - Higher TF: trend bullish, Bokk tapering/closing
   - Middle TF: Gap between Yellow Line and BS histogram, Bokk changing color
   - Lower TF: histogram turning green
   Entry: Buy Stop at Gold or Yellow Line
   Stop: Beyond swing point
   Target: Blue Line on execution timeframe

4. BLUE LINE TRADE — SHORT:
   - Higher TF: trend bearish, Bokk tapering/closing
   - Middle TF: Gap between Yellow Line and BS, Bokk changing color
   - Lower TF: histogram turning red
   Entry: Sell Stop at Gold or Yellow Line
   Stop: Beyond swing point
   Target: Blue Line on execution timeframe

5. LOGO TRADE — LONG (Clean V):
   - Directional Bars = Bright Green
   - Histogram/candles form a CLEAN V shape (smooth valley)
   - BS shows dimming red (Reset) then returns green
   Entry: Buy Stop at Gold or Yellow Line
   Stop: Bottom of V
   Target: Momentum loss — exit when BS/candles lose momentum, watch lower TF color turn
   SKIP if: no Reset present, or shape is messy/sideways

6. LOGO TRADE — SHORT (Clean Inverted V / Mountain):
   - Directional Bars = Bright Red
   - Histogram/candles form a CLEAN Inverted V / Mountain shape
   - BS shows dimming green (Reset) then returns red
   Entry: Sell Stop at Gold or Yellow Line
   Stop: Peak of Mountain
   Target: Momentum loss — watch lower TF color turn
   SKIP if: no Reset present, or shape is messy/sideways

7. UNO REVERSE (Keith Bot) — visible on candle charts during reversal:
   - Directional Bars turning from red to green (long) or green to red (short)
   - BS flipping dimming → bright in opposite direction
   - Bokk upper line changing color
   - Price crossing above (long) or below (short) Blue Line
   Entry: Buy/Sell Stop at Gold or Yellow Line
   Stop: Beyond swing point where reversal occurred
   Target: Blue Line of confirmation timeframe

CRITICAL RULES:
- ALWAYS read from bottom up: Directional Bars → BS Detector → Bokk → Price position
- If Directional Bars are mixed = NO TRADE, confidence very low
- Counter-trend (fast TF green, slow TF red) = lower confidence, shorter targets
- Full alignment across all TFs = highest confidence
- Output ALL trades you see, identify the HIGHEST PROBABILITY one as primary
- Include actual price levels when visible on the chart
- "When one goes up, they all go up. When one goes down, they all go down."

Return STRICT JSON:
{
  "trade_type": "name of highest probability trade",
  "trade_class": "trade-ggg|trade-blueline|trade-logo|trade-uno|trade-unknown",
  "direction": "LONG|SHORT|-",
  "entry": "specific entry instruction with price level if visible",
  "stop_loss": "specific stop loss instruction with price level if visible",
  "take_profit": "TP1: [level], TP2: [level], TP3: [level] with price levels if visible",
  "confidence": 0-100,
  "checklist": [{"text": "indicator name + what you see", "status": "check|uncheck|fail"}],
  "all_trades": [{"trade_type": "name", "direction": "LONG|SHORT", "confidence": 0-100}],
  "notes": "observations, warnings, multi-timeframe context, which layers confirm/deny"
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
            'all_trades': [],
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
            'all_trades': [],
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
            'all_trades': [],
            'notes': 'Could not parse AI response. See raw output below.',
            'raw_response': output[:1000]
        }
    else:
        analysis['raw_response'] = output
        if 'all_trades' not in analysis:
            analysis['all_trades'] = []

    return jsonify(analysis)


if __name__ == '__main__':
    print("TSTS Trade Analyzer starting on http://0.0.0.0:7860")
    app.run(host='0.0.0.0', port=7860, debug=False)
