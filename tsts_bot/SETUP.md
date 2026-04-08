# TSTS Trade Analyzer Bot — Setup Guide

## How It Works

The bot uses a **vision AI model** (via OpenClaw's `mimo-omni` skill) to analyze TradingView chart screenshots. The AI sees the chart image and identifies TSTS indicators, trade setups, entry/exit points, and confidence levels — all from a single screenshot.

### Architecture

```
User uploads chart image
        ↓
Flask app (app.py) receives image
        ↓
Saves to /tmp/tsts_chart.png
        ↓
Calls mimo_api.sh (OpenClaw mimo-omni skill)
        ↓
Vision AI reads the chart image + TSTS rules from system prompt
        ↓
Returns structured JSON with trade type, entry, stop, TP, confidence
        ↓
Flask renders result in dark-themed web UI
```

### The Key: The System Prompt

The `TSTS_SYSTEM_PROMPT` in `app.py` contains ALL the TSTS rules in plain text. The vision AI reads this prompt and applies the rules to whatever it sees in the chart image. This is what makes the bot work — it's not running code logic, it's an AI that understands the TSTS system visually.

When testing reveals errors, update the system prompt with corrections. The AI learns from the prompt, not from training data.

---

## Requirements

1. **OpenClaw** installed and running
2. **mimo-omni skill** installed at `/root/.openclaw/skills/mimo-omni/`
3. **Python 3** with Flask installed
4. Port **7860** available

---

## Installation

### Step 1: Clone the repo

```bash
git clone https://github.com/rapidhousebuyers-afk/The-trading-Bot.git
cd The-trading-Bot
```

### Step 2: Install Flask

```bash
# Option A: System install (may need --break-system-packages on newer Debian/Ubuntu)
pip install --break-system-packages flask

# Option B: Virtual environment
python3 -m venv venv
source venv/bin/activate
pip install flask
```

### Step 3: Verify mimo-omni is installed

```bash
ls /root/.openclaw/skills/mimo-omni/mimo_api.sh
```

If this file doesn't exist, install the mimo-omni skill in OpenClaw first.

### Step 4: Start the bot

```bash
cd tsts_bot
python3 app.py
```

The bot will start on `http://0.0.0.0:7860`

---

## How to Test

1. Open `http://your-server-ip:7860` in a browser
2. Upload a TradingView chart screenshot (PNG, JPG)
3. Click "Analyze Trade"
4. Wait 30-120 seconds for the AI to read the chart
5. Review the results: trade type, entry, stop loss, take profit, confidence, checklist

### Or test via command line:

```bash
python3 -c "
import base64, json, urllib.request
with open('path/to/your/chart.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()
payload = json.dumps({'image': 'data:image/png;base64,' + img_b64}).encode()
req = urllib.request.Request('http://127.0.0.1:7860/analyze', data=payload, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=180)
print(json.dumps(json.loads(resp.read()), indent=2))
"
```

---

## How the AI Reads Charts

The vision AI sees the chart image and identifies these elements:

### Candle Pane (top section of each panel)
- **Gold Line** — orange/gold EMA, closest to price → aggressive entry
- **Yellow Line** — yellow EMA, slower → conservative entry
- **Blue Line** — cyan/light blue EMA, slowest → PRIMARY TARGET
- **Bokk Channel** — two lines wrapping candles that open/close, change green/red (upper line = green bullish, red bearish)

### Histogram Panel (middle section)
- **BS Detector** — the green/red histogram bars (read bright/dim like MACD)
- **Yellow signal line** — overlaid on the histogram
- **Directional Bars (3Lines)** — small solid bars at the very base (solid green = bullish locked, solid red = bearish locked, mixed = NO TRADE)

### Sniper Oscillator (bottom section)
- **Pink Line** — fastest momentum, leads the move
- **Purple Line** — confirms true direction
- **Blue Line** — oscillator anchor/target
- **Orange Line** — entry trigger (close above = buy, close below = sell)

---

## Improving Accuracy

When the bot gives a wrong reading:

1. Note what it got wrong (wrong trade type, wrong confidence, missed indicator)
2. Update the `TSTS_SYSTEM_PROMPT` in `app.py` to add clarification
3. Restart the server
4. Retest the same image
5. Commit and push the fix

Every correction makes the bot better. The system prompt is the brain — edit it directly.

---

## File Structure

```
The-trading-Bot/
├── tsts_bot/
│   ├── app.py                    # Flask web app + AI system prompt
│   ├── TSTS_CH2_GLOSSARY.md      # Chapter 2: indicator definitions
│   ├── TSTS_TRADE_RULES.md       # Chapters 3-7: structured trade rules
│   └── SETUP.md                  # This file
├── tsts_images/                   # Sample chart images for testing
├── TSTS_COMPLETE_CURRICULUM.md    # Full 7-chapter course
├── TSTS_CH6_UNO_REVERSE_ENHANCED.md
└── TSTS_UNO_REVERSE_ENHANCED_NOTES.md
```

---

## Notes

- Analysis takes 30-120 seconds per image (the AI model needs time to read the chart)
- Dark background TradingView charts work best
- Multi-timeframe charts (2-4 panels side by side) give the most accurate reads
- The bot reads the chart AS IT APPEARS IN THE IMAGE — live market changes after the screenshot are not captured
- Always verify signals manually before placing real trades
