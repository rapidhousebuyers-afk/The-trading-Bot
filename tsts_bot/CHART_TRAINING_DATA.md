# TSTS Chart Image Analysis — Training Data
## Compiled from real chart screenshots analyzed on 3/30/2026

---

## Image 1: `chart_sample_1.png` — MNQ1! Multi-Timeframe (30s, 2m, 15m, 1h)

### Layout
- Four timeframes displayed: 30 seconds, 2 minutes, 15 minutes, 1 hour
- Top section: "UNO REVERSE STEROID" dashboard showing signal matrix for US30, NAS100, NQ1!, SPX500, ES1!
- Each timeframe panel has: candlesticks with MA ribbons, histogram (BS Detector), directional bars

### Indicators Identified
- **Yellow Line**: Fast MA, closest to price, acting as dynamic support on 30s and 2m
- **Gold Line**: Medium MA, sitting below Yellow
- **Blue Line**: Slow MA / major trend line. On 2m chart, price JUST crossed above it (Blue Line Breakout). On 15m and 1h, price is still BELOW the Blue Line (macro trend still down)
- **Pink/Purple Bands**: Volatility channel (like Bollinger Bands). On 30s, price pushing toward upper Pink band

### What Each Timeframe Shows
- **30s**: GGG setup — Green histogram rising, green directional bars, green arrows on dashboard. Strong short-term buying momentum
- **2m**: Blue Line Trade potential — Price crossed above Blue Line, histogram turned green. W-pattern (double bottom) formed earlier then broke out
- **15m**: Histogram still RED, price below Blue Line. Macro trend bearish
- **1h**: RRR setup — Red histogram, consistent lower highs and lower lows (downtrend)

### Dashboard (Uno Reverse Steroid)
- Short timeframes (1s-5m): Green Up Arrows on MNQ1!
- Long timeframes (15m-1D): Red Down Arrows
- **Interpretation**: Counter-trend scalp opportunity. Short-term bullish vs long-term bearish.

### Key Learning
This chart shows a **counter-trend pullback buy** — fast TFs are green while slow TFs are still red. NOT a full alignment trade. The 2m Blue Line breakout is the trigger, but higher timeframes haven't confirmed.

---

## Image 2: `chart_sample_2.png` — MNQ1! Multi-Timeframe (30s, 5m, 15m)

### Layout
- Three timeframes: 30 seconds, 5 minutes, 15 minutes
- Each panel has candlesticks with MAs, BS Detector histogram, Sniper oscillator at bottom

### Indicators Identified
- **Yellow Line**: Short-term MA (9 EMA), closely follows price
- **Gold Line**: Medium-term MA (21 EMA), smoother
- **Blue Line**: Longer-term MA / support-resistance. Price is ABOVE it — bullish
- **Pink/Purple Lines (Sniper)**: Oscillator lines (like Stochastic), 0-100 scale
  - Overbought > 80, Oversold < 20
  - Currently above 50 = bullish territory, not overbought
- **Blue Line (Sniper)**: Signal line confirming oscillator direction

### What Each Timeframe Shows
- **30s**: Bullish continuation — green candles after red pullback, breaking above Yellow MA. GGG R GG pattern visible
- **5m**: Mostly green candles (uptrend) with minor red pullback
- **15m**: Bullish reversal — red candles turned green, forming "morning star"-like pattern

### BS Detector
- Green bars dominant (bullish momentum)
- Yellow signal line above zero
- Confirming upward pressure across all timeframes

### Sniper Oscillator (Bottom Panes)
- Pink/purple lines above 50 (bullish, not overbought)
- Blue signal line confirms bullish trend direction

### Key Learning
This is a **bullish alignment** across all timeframes. Price above Blue Line, MAs bullish, BS green, Sniper in bullish territory. This is closer to a confirmed GGG RGG Safety Trade — the pullback (R) already happened and price is continuing up (GG).

---

## Patterns Summary for Bot Training

### GGG RGG (Long Safety Trade) Visual Markers
1. Directional bars at bottom: SOLID GREEN
2. BS Detector histogram: Was RED (dimming/reset), now turning GREEN
3. Bokk/histogram: Opening GREEN / expanding
4. Candle EMA: GREEN (price above Yellow/Gold)
5. Price should be approaching or above the Blue Line

### Blue Line Trade Visual Markers
1. Price crossing above (long) or below (short) the Blue Line
2. Gap between Yellow Line and BS Detector on middle timeframe
3. Bokk tapering or changing color
4. Lower timeframe already turning green (for long)

### RRR G RR (Short Safety Trade) Visual Markers
1. Directional bars at bottom: SOLID RED
2. BS Detector: Was GREEN (dimming/reset), now turning RED
3. Bokk/histogram: Opening RED / expanding downward
4. Candle EMA: RED (price below Yellow/Gold)

### Multi-Timeframe Context
- Always check higher timeframes for trend direction
- Higher TF flow controls lower TF trades
- Counter-trend setups (fast TF green, slow TF red) = riskier, shorter targets
- Full alignment across TFs = highest confidence setups
