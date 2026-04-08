# TSTS Trade Rules Engine
## Structured Parameters from Chapters 3-7
### Machine-Readable Trade Logic

---

## TRADE TYPE 1: GGG RGG (Safety Trade)

### LONG Setup (GGG RGG)

**Read bottom-up. All 4 layers must confirm.**

| Layer | Component | Required State | Visual Cue |
|-------|-----------|---------------|------------|
| 1 | Directional Bars | SOLID GREEN | Small bars at histogram base, all green, no mixed |
| 2 | BS Detector | DIMMING RED (Reset) | Red bars getting shorter/fading, yellow line approaching |
| 3 | Bokk | OPENING GREEN | Upper channel line is green, channel expanding |
| 4 | Price Position | Above Gold/Yellow Lines | Candles above both EMAs |

**Entry:**
- Aggressive: Buy Stop at Gold Line
- Conservative: Buy Stop at Yellow Line

**Stop Loss:** Below the swing low where the trend reversed during the reset

**Take Profit:**
- TP1: Previous local high
- TP2: Higher timeframe Blue Line

---

### SHORT Setup (RRR G RR)

**Read bottom-up. All 4 layers must confirm.**

| Layer | Component | Required State | Visual Cue |
|-------|-----------|---------------|------------|
| 1 | Directional Bars | SOLID RED | Small bars at histogram base, all red, no mixed |
| 2 | BS Detector | DIMMING GREEN (Reset) | Green bars getting shorter/fading, yellow line approaching |
| 3 | Bokk | OPENING RED | Upper channel line is red, channel expanding |
| 4 | Price Position | Below Gold/Yellow Lines | Candles below both EMAs |

**Entry:**
- Aggressive: Sell Stop at Gold Line
- Conservative: Sell Stop at Yellow Line

**Stop Loss:** Above the swing high where the trend reversed during the reset

**Take Profit:**
- TP1: Previous local low
- TP2: Higher timeframe Blue Line

---

## TRADE TYPE 2: Blue Line Trade

### LONG Setup

| Layer | Component | Required State | Visual Cue |
|-------|-----------|---------------|------------|
| 1 | Higher TF (15m) | Trend bullish, Bokk tapering | Bokk channel closing/contracting on 15m |
| 2 | Middle TF (5m) | Gap between Yellow Line and BS | BS far from yellow signal line, Bokk changing color |
| 3 | Lower TF (30s/1m) | Turning Green | Histogram bars switching from red to green |

**Entry:**
- Aggressive: Buy Stop at Gold Line
- Conservative: Buy Stop at Yellow Line

**Stop Loss:** Below swing low where trend reversed

**Take Profit:** Blue Line on the execution timeframe (30s or 1m)

### SHORT Setup

| Layer | Component | Required State | Visual Cue |
|-------|-----------|---------------|------------|
| 1 | Higher TF (15m) | Trend bearish, Bokk tapering | Bokk channel closing on 15m |
| 2 | Middle TF (5m) | Gap between Yellow Line and BS | BS far from yellow signal line, Bokk changing color |
| 3 | Lower TF (30s/1m) | Turning Red | Histogram bars switching from green to red |

**Entry:**
- Aggressive: Sell Stop at Gold Line
- Conservative: Sell Stop at Yellow Line

**Stop Loss:** Above swing high where trend reversed

**Take Profit:** Blue Line on the execution timeframe

---

## TRADE TYPE 3: Logo Trade

### LONG Setup (Clean V Shape)

| Layer | Component | Required State | Visual Cue |
|-------|-----------|---------------|------------|
| 1 | Directional Bars | BRIGHT GREEN | Solid green, macro bullish |
| 2 | Candle/Histogram | Clean V shape | Smooth valley/dip pattern |
| 3 | BS Detector | DIMMING RED (Reset) then returning GREEN | Red fading → green returning |
| 4 | Top Line | Flashing Green | Final confirmation signal |

**Entry:**
- Aggressive: Buy Stop at Gold Line
- Conservative: Buy Stop at Yellow Line

**Stop Loss:** Bottom of the V

**Take Profit:** Momentum loss — exit when BS/candles lose momentum. Watch lower TF for color turn.

### SHORT Setup (Clean Inverted V / Mountain)

| Layer | Component | Required State | Visual Cue |
|-------|-----------|---------------|------------|
| 1 | Directional Bars | BRIGHT RED | Solid red, macro bearish |
| 2 | Candle/Histogram | Clean Inverted V / Mountain | Smooth peak pattern |
| 3 | BS Detector | DIMMING GREEN (Reset) then returning RED | Green fading → red returning |
| 4 | Top Line | Flashing Red | Final confirmation signal |

**Entry:**
- Aggressive: Sell Stop at Gold Line
- Conservative: Sell Stop at Yellow Line

**Stop Loss:** Peak of the Mountain

**Take Profit:** Momentum loss — exit when BS/candles lose momentum. Watch lower TF for color turn.

**SKIP IF:**
- ❌ No BS reset present (no dimming)
- ❌ Shape is messy or sideways (not a clean V or Mountain)

---

## TRADE TYPE 4: Uno Reverse (Keith Bot)

**For candle chart analysis only — dashboard analysis excluded for now.**

### Visual Signs on Candle Charts:

When the overnight reversal is in progress and visible on candle charts:

| Indicator | Reversal Up (Long) | Reversal Down (Short) |
|-----------|-------------------|----------------------|
| Directional Bars | Turning from red to green | Turning from green to red |
| BS Detector | Dimming red → bright green | Dimming green → bright red |
| Bokk | Upper line changing red → green | Upper line changing green → red |
| Price | Crossing above Blue Line | Crossing below Blue Line |
| Sniper Pink | Rising from oversold | Falling from overbought |
| Sniper Purple | Confirming upward | Confirming downward |

**Entry:**
- Long: Buy Stop at Gold Line or Yellow Line
- Short: Sell Stop at Gold Line or Yellow Line

**Stop Loss:** Beyond the swing point where reversal occurred

**Take Profit:** Blue Line of the timeframe where setup confirmed

---

## MULTI-TIMEFRAME ENTRY FRAMEWORK

| Setup Timeframes | Entry TF (Blue Line) |
|-----------------|---------------------|
| 4hr / Daily | 15min Blue Line |
| 30min / 1hour | 3min Blue Line |
| 1hr / 15min | 5min Blue Line |
| 15min / 1hour | 1min Blue Line |
| 5min / 15min | 30sec Blue Line |

### Orange Line Entry Rule:
- Candle closes above Orange Line (long) or below (short) → enter next candle at Orange Line level
- 10-period orange EMA crossing 30 EMA = EXACT ENTRY SIGNAL

### Higher TF Line Rule:
- Entry level set on higher TF carries to lower TF UNCHANGED — do not adjust

---

## CONFIDENCE SCORING

| Condition | Confidence Impact |
|-----------|------------------|
| All 4 layers confirm, all timeframes aligned | +30% |
| Directional Bars solid (not mixed) | +20% |
| BS shows clear Reset/dimming | +15% |
| Bokk opening in trend direction | +15% |
| Price at Gold Line (aggressive) or Yellow Line (conservative) | +10% |
| Higher timeframes aligned with trade direction | +10% |
| Any layer missing | -25% |
| Directional Bars mixed | -40% |
| Counter-trend (fast TF green, slow TF red) | -20% |
| Messy/sideways pattern (not clean V/Mountain) | -15% |

---

## MASTER ENTRY/EXIT TABLE

| Trade | Entry | Stop | Target |
|-------|-------|------|--------|
| GGG RGG | Buy/Sell Stop at Gold (aggressive) or Yellow (conservative) | Beyond swing point | Previous high/low or HTF Blue Line |
| Blue Line | Buy/Sell Stop at Gold or Yellow | Beyond swing point | Blue Line on execution TF |
| Logo Trade | Buy/Sell Stop at Gold or Yellow | Bottom of V or peak of Mountain | Momentum loss (watch lower TF) |
| Uno Reverse | Buy/Sell Stop at Gold or Yellow | Beyond swing point | Blue Line of confirmation TF |
