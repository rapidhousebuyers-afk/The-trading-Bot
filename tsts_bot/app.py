# TSTS Trade Analyzer Bot
# Upload a chart screenshot → Get trade type, entry, stop loss, take profit
# Based on The Safety Trade System (TSTS) by Kevin Grego

import os
import json
import base64
import subprocess
import shutil
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

MIMO_API = "/root/.openclaw/skills/mimo-omni/mimo_api.sh"
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

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
        <div style="margin-top: 30px;">
            <h2 style="color: #58a6ff; font-size: 1.3rem; margin-bottom: 15px;">&#x1F4CB; Analysis History</h2>
            <button onclick="loadHistory()" style="background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-bottom: 15px;">Load History</button>
            <div id="historyList"></div>
        </div>
    </div>
    <script>
        async function loadHistory() {
            const res = await fetch('/results');
            const data = await res.json();
            const div = document.getElementById('historyList');
            if (data.results.length === 0) { div.innerHTML = '<p style="color:#484f58;">No saved analyses yet.</p>'; return; }
            div.innerHTML = data.results.map(r => `
                <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong style="color:#c9d1d9;">${r.trade_type}</strong>
                        <span style="color:${r.direction==='LONG'?'#3fb950':r.direction==='SHORT'?'#f85149':'#8b949e'}; margin-left:8px;">${r.direction}</span>
                        <span style="color:#8b949e; margin-left:8px;">${r.confidence}%</span>
                    </div>
                    <div style="color:#484f58; font-size:0.8rem;">${r.saved_at}</div>
                </div>
            `).join('');
        }
    </script>
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

TSTS_SYSTEM_PROMPT = """You are a TSTS (The Safety Trade System) chart analyzer created by Kevin Grego. You analyze TradingView chart screenshots and TSTS mobile app screenshots to identify trade setups with precision.

YOU MUST RESPOND IN ENGLISH ONLY. All JSON values — trade_type, entry, stop_loss, take_profit, checklist text, notes — must be written in English. Never use Chinese or any other language.

═══════════════════════════════════════════════════
STEP 0: IMAGE CLASSIFICATION (DO THIS FIRST)
═══════════════════════════════════════════════════
Before analyzing indicators, determine what type of image this is:

A) LIVE TRADING CHART (TradingView desktop/web): Dark background, candlesticks, indicators, no large text blocks or chapter headings. PROCEED with full analysis.
B) TSTS MOBILE APP: Shows asset name (e.g. "NQ 06-25"), countdown timer ("Wait | HH:MM:SS" or "Up/Down (HH:MM:SS)"), P/L panel, colored signal box (Green/Red/Orange), timeframe tabs at bottom. PROCEED but use mobile layout rules below.
C) CURRICULUM/EDUCATIONAL SLIDE: Contains chapter headings ("Chapter 5", "Identifying BOKK"), bullet points, textbook layout, or training content overlaid on charts. If detected, set confidence to 0, trade_type to "Curriculum Slide (Not a Live Chart)", and explain what educational content the slide covers. DO NOT generate trade signals from educational slides.

═══════════════════════════════════════════════════
CHART LAYOUT TYPES
═══════════════════════════════════════════════════

TRADINGVIEW DESKTOP LAYOUT:
- 2-4 timeframes displayed side by side (e.g., 30s, 2m, 15m, 1h)
- Each panel has three sections stacked vertically (candle, histogram, sniper)

TSTS MOBILE APP LAYOUT:
- Each timeframe is a FULL-WIDTH panel stacked vertically (not side by side)
- Asset name and price displayed at top of each panel
- Timeframe tabs at bottom (30s, 2m, 15m, 1h)
- Signal status box at top of each panel (Green = bullish active, Red = bearish active, Orange = wait/pending)
- ACTIVE POSITION PANEL: If a trade is open, you will see a box showing: direction (LONG/SHORT), entry price, P/L in dollars, P/L percentage, and a countdown timer like "Down (05:21:32)" or "Up (03:43:00)". "Down" = SHORT position. "Up" = LONG position. This is CRITICAL — always detect and report this.
- Directional Bars on mobile: On the mobile app, the Directional Bars appear as ONE OR TWO WIDE BARS at the base of the histogram, not three thin bars like TradingView. Read the OVERALL COLOR of the bar(s): if the bar is predominantly solid green with no red stripes = bullish. Predominantly solid red with no green stripes = bearish. If you see BOTH green and red stripes or segments within the bar = mixed/no-trade. Do NOT call a solid-colored bar "mixed" just because it's a single wide bar — that's the normal mobile format.
- Indicators carry the same meaning as TradingView — do not change interpretation, only adapt to the layout

═══════════════════════════════════════════════════
INDICATOR GUIDE
═══════════════════════════════════════════════════

IMPORTANT: The Bokk is NOT the histogram. The Bokk is a CHANNEL on the candle pane — two lines (upper and lower) that wrap around the candles. They change color (green/red), expand (open) when institutional momentum enters, and contract (close) when momentum fades.

CANDLE PANE (top of each panel):
- Gold Line: fast EMA (orange/gold), closest to price. AGGRESSIVE entry trigger.
- Yellow Line: slower EMA (yellow). CONSERVATIVE entry trigger.
- Blue Line: slowest EMA (cyan/light blue), nearly horizontal. PRIMARY TARGET — price is always drawn to it.
- BOKK CHANNEL: Two lines forming envelope around candles. Upper line = green (bullish) or red (bearish). Lower line = red.
  * WIDENING/EXPANDING = institutional momentum entering (strong signal)
  * CLOSING/CONTRACTING = momentum exhausting, pullback or reversal coming
  * UPPER LINE COLOR: green = bullish, red = bearish
  * "Slightly closing" on a higher TF while lower TF Bokk is widening = the higher TF is exhausting current trend while lower TF is already building new momentum in opposite direction. This is a LEADING SIGNAL for the flip.

HISTOGRAM PANEL (middle):
- Green/Red histogram bars + yellow signal line
- BS DETECTOR: Bright green = strong bullish momentum. Dim green = fading bullish (Reset beginning). Bright red = strong bearish momentum. Dim red = fading bearish (Reset beginning).

THE RESET IS THE SETUP, NOT THE TRADE: When you see DIMMING bars (red getting shorter/fading, or green getting shorter/fading), this is the RESET phase — it means the current momentum is exhausting and a flip is coming. A GGG RGG LONG forms when: higher TFs show dimming RED (bearish exhaustion) while lower TFs are already turning GREEN. A RRR G RR SHORT forms when: higher TFs show dimming GREEN (bullish exhaustion) while lower TFs are already turning RED. Dimming is NOT bearish or bullish on its own — it's the TRANSITION. Always check: is the dimming happening on the higher TF while the lower TF has already flipped? That's the setup.
- DIRECTIONAL BARS (3Lines): Small bars at histogram base. Solid green = macro bullish locked. Solid red = macro bearish locked. Mixed/choppy = NO-TRADE ZONE.

SNIPER OSCILLATOR (bottom):
- Pink: fastest momentum. Pinned 80-100 = overbought. 0-20 = oversold.
- Purple: confirms direction. Pink crossing Purple = momentum shift.
- Blue: oscillator anchor/target.
- Orange: entry trigger. Close above = long. 10-orange EMA crossing 30 EMA = EXACT ENTRY.

═══════════════════════════════════════════════════
TRADE TYPE RULES
═══════════════════════════════════════════════════

1. GGG RGG (Safety Trade) — LONG:
   Bottom-up: Dir Bars solid GREEN → BS was dimming RED now GREEN → Bokk opening GREEN → Price above Gold/Yellow
   Entry: Buy Stop at Gold (aggressive) or Yellow (conservative)
   Stop: Below swing low
   Target: Higher TF Blue Line (MUST be above entry price)

2. RRR G RR (Safety Trade) — SHORT:
   Bottom-up: Dir Bars solid RED → BS was dimming GREEN now RED → Bokk opening RED → Price below Gold/Yellow
   Entry: Sell Stop at Gold (aggressive) or Yellow (conservative)
   Stop: Above swing high
   Target: Higher TF Blue Line (MUST be below entry price)

3. BLUE LINE TRADE — LONG:
   Higher TF bullish, Bokk tapering. Middle TF gap Yellow/BS. Lower TF histogram turning green.
   Target: Blue Line on execution TF (must be above entry)

4. BLUE LINE TRADE — SHORT:
   Higher TF bearish, Bokk tapering. Middle TF gap Yellow/BS. Lower TF histogram turning red.
   Target: Blue Line on execution TF (must be below entry)

5. LOGO TRADE — LONG (Clean V):
   Dir Bars bright green. Clean V shape. BS dimming red then green.
   Stop: Bottom of V. Target: Momentum loss.

6. LOGO TRADE — SHORT (Clean Inverted V):
   Dir Bars bright red. Clean inverted V. BS dimming green then red.
   Stop: Peak. Target: Momentum loss.

MULTI-TIMEFRAME SEQUENCING (CRITICAL FOR EARLY DETECTION):
Trades don't form all at once — they build from the bottom up:
- STEP 1: Higher TF (15m) shows dimming/reset first — momentum exhausting
- STEP 2: Middle TF (5m) follows — also dimming, Bokk may start closing
- STEP 3: Lower TF (30s) confirms — Directional Bars turn solid, BS goes bright, Bokk opens
When you see Steps 1-2 happening but Step 3 not complete, the trade is FORMING — report it as a setup with reduced confidence. Don't dismiss it as "no trade" just because it's not fully confirmed yet.
Example: 15m BS dimming red + 5m BS dimming red + 30s already green = GGG RGG LONG building. The 15m and 5m are in Reset, 30s has already flipped. This is a HIGH VALUE setup forming.

7. UNO REVERSE:
   Dir Bars flipping color. BS flipping. Bokk changing. Price crossing Blue Line.
   Target: Blue Line of confirmation TF.

CONFIDENCE SCORING GUIDE:
- 30s fully confirmed (all layers green/red) = +25%
- 5m in Reset (BS dimming, gap visible) = +20% — this is the setup, not a weakness
- 15m in Reset with early flip signs (pink turning, Bokk changing) = +20%
- Directional Bars transitioning on higher TFs = +10% (trend is building)
- Bokk widening on execution TF = +10%
- All layers locked across all TFs = 85-95%
- Execution TF confirmed + higher TFs in Reset = 70-90% (this IS the high-probability entry window)
- Mixed dir bars with no clear trend color = -30%
- No Reset visible on any TF = -20% (no setup phase detected)
- True counter-trend (all higher TFs locked opposite) = cap at 50%

═══════════════════════════════════════════════════
CRITICAL RULES (VIOLATIONS = ANALYSIS FAILURE)
═══════════════════════════════════════════════════

- NEVER say "assumed", "estimated", or "not clearly visible but" for indicator states. If you cannot read an indicator clearly, set its checklist status to "uncheck" and reduce confidence. DO NOT fabricate readings.
- ALWAYS read from bottom up: Directional Bars → BS Detector → Bokk → Price position
- If Directional Bars are mixed = NO TRADE, confidence ≤ 20
- DIRECTION VALIDATION: For LONG trades, ALL take profit levels MUST be above the entry price. For SHORT trades, ALL take profit levels MUST be below the entry price. EXCEPTION: On multi-timeframe setups where higher TF Blue Line is on the wrong side BUT the execution (lowest) TF Blue Line is on the correct side, use the execution TF Blue Line as TP1 and note the higher TF as a "stretch target once trend confirms." Do NOT penalize for this — it's normal during trend transitions.
- DIRECTIONAL BARS TRANSITION RULE: When Directional Bars show the OPPOSITE color at the base but the new trend color is appearing/turning at the top, this is "TRANSITIONING" — NOT "locked bearish/bullish." Transitioning bars on higher TFs while lower TFs are already confirmed = HIGH VALUE setup, not a fail. Only call bars "locked" if they are solidly one color with NO traces of the opposite color. "Turning red" or "turning green" is a POSITIVE signal for the forming trade direction.
- Counter-trend (fast TF green, slow TF red) = cap confidence at 50, use lower TF Blue Line as target instead of higher TF
- Full alignment across all TFs = highest confidence (80+)
- Output ALL trades you see, identify HIGHEST PROBABILITY one as primary
- Include actual price levels when visible on chart
- MOBILE APP — ACTIVE POSITION DETECTION: The TSTS mobile app displays active positions in a panel showing: direction (LONG/SHORT), entry price, current P/L ($ and %), and a countdown timer. If you see this panel, you MUST: (1) report the shown position in your notes, (2) compare your indicator reading to the shown position direction. If they CONTRADICT (e.g., shown LONG but indicators read bearish), this means the trade was entered earlier and conditions may have shifted. In this case, set your primary trade direction to MATCH the shown position if the P/L is positive (the trade is winning — trust the entry), or flag the conflict if P/L is negative. A winning position is strong evidence the original read was correct.
- "When one goes up, they all go up. When one goes down, they all go down."

Return STRICT JSON:
{
  "trade_type": "name of highest probability trade",
  "trade_class": "trade-ggg|trade-blueline|trade-logo|trade-uno|trade-unknown",
  "direction": "LONG|SHORT|-",
  "entry": "specific entry instruction with price level if visible",
  "stop_loss": "specific stop loss instruction with price level if visible",
  "take_profit": "TP1: [level], TP2: [level], TP3: [level] with price levels if visible. MUST match direction.",
  "confidence": 0-100,
  "checklist": [{"text": "indicator name + what you READ (not assumed)", "status": "check|uncheck|fail"}],
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
            ['bash', MIMO_API, 'image', img_path,
             "FIRST: Read all text visible on this image. Report: (1) Asset/instrument name, "
             "(2) Current price shown, (3) All timeframe labels visible (e.g. 30s, 2m, 15m, 1h, 4h), "
             "(4) If an active position panel is visible, report its direction, entry price, and P/L. "
             "Use these GROUND TRUTH values in your analysis. Do not guess or use different numbers.\n\n"
             + TSTS_SYSTEM_PROMPT],
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

    # Auto-save analysis result
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    trade_type_safe = analysis.get('trade_type', 'unknown').replace(' ', '_').replace('/', '-')[:40]
    save_name = f"{timestamp}_{trade_type_safe}"
    
    # Save chart image
    img_save_path = os.path.join(RESULTS_DIR, f"{save_name}.png")
    with open(img_save_path, 'wb') as f:
        f.write(base64.b64decode(image_b64))
    
    # Save analysis JSON
    analysis_save = {**analysis}
    analysis_save['saved_at'] = datetime.now().isoformat()
    analysis_save['chart_image'] = f"{save_name}.png"
    json_save_path = os.path.join(RESULTS_DIR, f"{save_name}.json")
    with open(json_save_path, 'w') as f:
        json.dump(analysis_save, f, indent=2)
    
    analysis['saved_to'] = f"{save_name}.json"
    
    # Auto-commit and push to GitHub
    try:
        subprocess.run(
            ['git', 'add', f'tsts_bot/results/{save_name}.json', f'tsts_bot/results/{save_name}.png'],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True, timeout=10
        )
        subprocess.run(
            ['git', 'commit', '-m', f'Analysis: {analysis.get("trade_type", "unknown")} {analysis.get("direction", "")} {analysis.get("confidence", 0)}%'],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True, timeout=10
        )
        subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True, timeout=30
        )
    except Exception:
        pass  # Push failure shouldn't block the response
    
    return jsonify(analysis)


@app.route('/results')
def list_results():
    """List all saved analysis results."""
    files = sorted([f for f in os.listdir(RESULTS_DIR) if f.endswith('.json')], reverse=True)
    results = []
    for f in files:
        try:
            with open(os.path.join(RESULTS_DIR, f)) as fh:
                data = json.load(fh)
            results.append({
                'filename': f,
                'trade_type': data.get('trade_type', '-'),
                'direction': data.get('direction', '-'),
                'confidence': data.get('confidence', 0),
                'saved_at': data.get('saved_at', '-'),
                'chart_image': data.get('chart_image', ''),
                'entry': data.get('entry', '-'),
                'stop_loss': data.get('stop_loss', '-'),
                'take_profit': data.get('take_profit', '-')
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return jsonify({'results': results, 'total': len(results)})


@app.route('/results/<filename>')
def get_result(filename):
    """Get a specific saved analysis result."""
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'Not found'}), 404
    with open(path) as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    print("TSTS Trade Analyzer starting on http://0.0.0.0:7860")
    app.run(host='0.0.0.0', port=7860, debug=False)
