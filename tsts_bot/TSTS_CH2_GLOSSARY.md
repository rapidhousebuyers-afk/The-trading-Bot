# TSTS Chapter 2 — The Language of TSTS
## Indicator Glossary & Visual Identification Guide
### Structured Reference for Bot Integration

---

## HOW TO READ EACH TSTS CHART PANEL

Every TSTS chart has the same layout on each timeframe panel. Read from **top to bottom**:

```
┌─────────────────────────────────────────────┐
│  CANDLE PANE                                │
│  ┌─────────────────────────────────────┐    │
│  │ Candlesticks (Green/Red)            │    │
│  │ Gold Line (fast EMA)                │    │
│  │ Yellow Line (slower EMA)            │    │
│  │ Blue Line (anchor EMA — THE TARGET) │    │
│  │ BOKK Channel (green/red lines that  │    │
│  │   open, close, and cross)           │    │
│  └─────────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│  HISTOGRAM PANEL = BS DETECTOR              │
│  ┌─────────────────────────────────────┐    │
│  │ Green/Red histogram bars            │    │
│  │ Yellow signal line overlaid         │    │
│  │ Directional Bars (3Lines) at base   │    │
│  └─────────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│  SNIPER OSCILLATOR PANEL                    │
│  ┌─────────────────────────────────────┐    │
│  │ Pink, Purple, Blue, Orange lines    │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## SECTION 1 — CANDLE PANE ELEMENTS

### Gold Line (Fast EMA — Aggressive Entry)
- **What it is:** The fastest Exponential Moving Average on the candle chart
- **Visual:** Orange/gold colored line, follows price candles tightly
- **Job:** Aggressive entry trigger. When price interacts with the Gold Line, you get an earlier entry with more risk but more reward.
- **For the bot:** Price above Gold = bullish. Below = bearish. Buy Stop / Sell Stop at Gold Line = **aggressive entry**.

### Yellow Line (Slower EMA — Conservative Entry)
- **What it is:** A smoother, slower EMA that lags behind the Gold Line
- **Visual:** Yellow colored line, sits slightly further from price than Gold
- **Job:** Conservative entry trigger. In GGG RGG, the Reset must touch or interact with this line.
- **For the bot:** Buy Stop / Sell Stop at Yellow Line = **conservative entry**. Less reward, less risk.

### Blue Line (Anchor EMA — THE TARGET)
- **What it is:** The slowest EMA, nearly horizontal compared to volatility. The gravity/magnet for price.
- **Visual:** Cyan/light blue line across the chart
- **Job:** Price is always drawn toward the Blue Line. It's the bullseye. Almost every trade targets the Blue Line.
- **For the bot:** PRIMARY TARGET for most trades. Price crossing above Blue Line = significant bullish signal. Price below Blue Line on higher TF = macro trend still bearish.

### BOKK (Institutional Flow Channel — On the Candle Pane)
- **What it is:** A pair of lines forming a channel/envelope around the candles. THIS IS NOT THE HISTOGRAM.
- **Visual:** Two lines — an upper line and a lower line — that wrap around the candlesticks. They change color (green/red) and expand/contract.
  - **Upper line:** Green when bullish, turns Red when bearish
  - **Lower line:** Red (remains red through both trends)
  - The lines **open** (expand apart) when institutional momentum enters
  - The lines **close** (contract together) when momentum exhausts
  - Lines cross each other when trend shifts (green upper crosses below = bearish, crosses above = bullish)
- **Job:** Shows institutional momentum flow
  - **Bokk Opening Green** = upper line is green, channel expanding = institutional buying entering
  - **Bokk Opening Red** = upper line is red, channel expanding = institutional selling entering
  - **Bokk Tapering/Closing** = channel contracting = momentum exhausting, pullback coming
  - **Bokk changing color** = trend shift occurring
- **For the bot:** This is **Layer 3** in the bottom-up reading. "Bokk Opening [color]" confirms institutional momentum is re-entering in the trend direction.

---

## SECTION 2 — HISTOGRAM PANEL (BS Detector)

The histogram sits below the candle pane. It has two components:

### Histogram Bars (Momentum Visualization)
- **Visual:** Green bars (bullish momentum) and Red bars (bearish momentum)
- **Job:** Shows the strength and direction of the immediate move
  - Bars rising/growing = momentum increasing
  - Bars falling/shrinking = momentum fading
  - Bars switching color = trend change

### BS Detector (Bull/Sell — Brightness + Yellow Signal Line)
- **What it is:** Read the histogram bars like a MACD. Brightness matters. The yellow line overlaid on the histogram is the signal line.
- **Visual:**
  - **Bright Green** bars = strong active bullish momentum, the move is alive
  - **Dim Green** bars = bullish momentum fading, Reset phase starting
  - **Bright Red** bars = strong active bearish momentum
  - **Dim Red** bars = bearish momentum fading, Reset phase starting
  - **Yellow signal line** crossing through the bars
  - **Gap** between bars and yellow line = momentum exhaustion
- **Job:** Early warning system for resets and momentum shifts.
  - The "R" in GGG RGG = the Reset = the dimming
  - If no dimming/Reset is visible, the trade LACKS the safety component — skip it
- **For the bot:** This is **Layer 2** in the bottom-up reading. BS must show dimming/reset before a trade is valid.

---

## SECTION 3 — DIRECTIONAL BARS (3Lines)

- **What they are:** Small colored bars at the base of the histogram panel
- **Visual:** Can be solid green, solid red, or mixed/choppy
- **Job:** Shows the **higher timeframe trend lock**
  - **Solid Green** = macro bullish bias. Higher timeframes aligned up. Foundation set for longs.
  - **Solid Red** = macro bearish bias. Higher timeframes aligned down. Foundation set for shorts.
  - **Mixed/Choppy** = NO-TRADE ZONE. Timeframes disagree. Do not trade.
- **For the bot:** This is **Layer 1** (the foundation). If Directional Bars are mixed, confidence drops to near zero. If they don't match the trade direction, skip.

---

## SECTION 4 — SNIPER (Oscillator Panel at Bottom)

The Sniper is a separate oscillator panel at the very bottom. It contains four lines.

### Pink Line (Fastest Momentum — Leads the Move)
- **Visual:** Pink colored, moves aggressively
- **Job:** Leads price action. Shows overbought/oversold extremes.
  - Pinned at top (80-100) = overbought, pullback coming
  - Pinned at bottom (0-20) = oversold, bounce coming
  - Rising from oversold = bullish momentum building
- **For the bot:** On higher timeframes, Pink moves are big. On lower timeframes, don't wait for Pink — use Purple earlier.

### Purple Line (True Direction — Confirmation)
- **Visual:** Purple colored, follows price more closely than Pink
- **Job:** Confirms where price will REALLY go
  - Pink crosses Purple upward = bullish momentum shift confirmed
  - Pink crosses Purple downward = bearish momentum shift confirmed
- **For the bot:** Wait for Purple to confirm Pink's lead before acting.

### Blue Line (Oscillator Anchor — Target)
- **Visual:** Blue colored, slower moving
- **Job:** Gravity for price in the oscillator. Blue pulling up = continuation confirmed (long). Blue pulling down = continuation confirmed (short).
- **For the bot:** Same as the candle Blue Line — price is drawn to it.

### Orange Line (Entry Trigger)
- **Visual:** Orange colored
- **Job:** Exact entry trigger
  - Candle closes above Orange Line (long) or below (short) → enter next candle at Orange Line level
  - **10-period orange EMA crossing the 30 EMA = EXACT ENTRY SIGNAL**
  - 10 crosses above 30 = bullish entry
  - 10 crosses below 30 = bearish entry
- **For the bot:** This is the mechanical trigger for EXACT timing.

---

## SECTION 5 — ORDER TYPES

### Buy Stop (BS)
- Order placed ABOVE current price, triggers buy when price reaches it
- For the bot: Use for long entries at Gold Line (aggressive) or Yellow Line (conservative)

### Sell Stop (SS)
- Order placed BELOW current price, triggers sell when price reaches it
- For the bot: Use for short entries at Gold Line (aggressive) or Yellow Line (conservative)

---

## QUICK REFERENCE TABLE

| Component | Location | Visual | Job |
|-----------|----------|--------|-----|
| **Gold Line** | Candle pane | Orange/gold EMA, closest to price | Aggressive entry trigger |
| **Yellow Line** | Candle pane | Yellow EMA, slower than Gold | Conservative entry trigger |
| **Blue Line** | Candle pane | Cyan/light blue EMA | PRIMARY TARGET — gravity/magnet |
| **Bokk** | Candle pane | Green/red channel lines that open/close | Institutional flow indicator |
| **BS Detector** | Histogram | Bright/dim green/red bars + yellow line | Momentum bias / Reset detection |
| **Directional Bars** | Base of histogram | Small solid bars | Higher TF trend lock (Layer 1) |
| **Pink Line** | Sniper panel | Pink line | Fastest momentum, leads |
| **Purple Line** | Sniper panel | Purple line | True direction confirmation |
| **Blue Line** | Sniper panel | Blue line | Oscillator anchor/target |
| **Orange Line** | Sniper panel | Orange line | Entry trigger (close above/below) |

---

## BOTTOM-UP READING METHOD

Always read from bottom to top:

```
Step 1 (Foundation):  Directional Bars — solid green or solid red?
Step 2 (Reset):       BS Detector — showing dimming/reset?
Step 3 (Momentum):    Bokk — channel opening in trend direction?
Step 4 (Trigger):     Price position — above/below Gold/Yellow lines?
```

If ANY step fails → no trade. If ALL steps confirm → setup confirmed → proceed to Chapter 7 for entry execution.
