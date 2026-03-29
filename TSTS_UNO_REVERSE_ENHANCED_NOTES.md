# THE SAFETY TRADE SYSTEM — UNO REVERSE (KEITH BOT)
## Enhanced Course Definition & Detailed Notes
### Compiled from Course Build + 3 Video Transcripts

---

## DEFINITION

**Uno Reverse (Keith Bot)** — A semi-automatic robot indicator (Pine Script on TradingView) that monitors five major US indices across sequential timeframes, reading whether price is above or below the system's Blue Line (an EMA). Named after the Uno reverse card — it detects when a market reversal is occurring (from bearish red to bullish green, or vice versa). Named in honor of the great late Keith Palmer, the coder who built it. Designed primarily for the overnight reversal trade setup. Also referred to as "the Oreo Cookie Trade" or "the Oreo Sandwich" due to its signature visual pattern on the dashboard.

**Core Philosophy:** "The only trade you need to learn to be consistent with the system." Kevin teaches that if this is the only trade type you ever take, you can become a consistently profitable trader.

---

## THE FIVE MONITORED INDICES

1. **US30** (Dow Jones) — **REQUIRED anchor symbol** (must be included)
2. **NAS100 / NAS** (Nasdaq 100)
3. **NQ1!** (Nasdaq Futures)
4. **SPX500 / SPX** (S&P 500)
5. **ES1!** (E-mini S&P Futures)

**Critical Rule:** US30, NAS, NQ1, SPX, and ES1 all move as one symbol. What happens to one happens to all. If one lags, it will catch up to the others.

---

## WHAT THE DASHBOARD DISPLAYS

The Keith Bot reads the **Sniper** indicator — specifically whether price is **above or below the Blue Line** (an EMA) on each timeframe for each symbol.

- **Green** = Price is ABOVE the Blue Line (bullish)
- **Red** = Price is BELOW the Blue Line (bearish)

The display uses **color-coded triangles/arrows**:
- Green triangles pointing UP = bullish (price above blue line)
- Red triangles pointing DOWN = bearish (price below blue line)

You can see the entire market picture across all timeframes and all symbols at a glance. The Keith Bot is essentially "a big sniper rifle on steroids" — it reads the Sniper indicator and condenses all the information into one dashboard.

---

## THE SEQUENTIAL FLIP ORDER

Safety trades form in a **specific sequential order**. This is a core rule:

| Order | Timeframe |
|-------|-----------|
| 1st | 1-Second |
| 2nd | 5-Second |
| 3rd | 10-Second |
| 4th | 15-Second |
| 5th | 30-Second |
| 6th | 45-Second |
| 7th | 1-Minute |
| 8th | 2-Minute |
| 9th | 5-Minute |
| ... | Continues upward |

During a reversal, timeframes flip from red to green **in ascending order**. Each flip confirms the reversal is gaining strength. It's a domino effect.

---

## THE OREO COOKIE / OREO SANDWICH PATTERN

This is the signature visual pattern on the dashboard that signals a reversal is loading:

- **Top Cookie (Higher Timeframes):** 15-minute, 30-minute, 1-hour, Daily — already green. The macro trend has already turned.
- **Cream Filling (Middle Timeframes):** Still red. Being compressed and overwhelmed from both sides.
- **Bottom Cookie (Lower Timeframes):** 5-second, 10-second, 15-second — turning green. Micro momentum is pushing up.

**What it means:** Momentum is compressing from both sides. The higher timeframes have already turned bullish. The lower timeframes are catching up. The middle timeframes are about to flip. The reversal is loading — the dominoes are falling.

---

## THE OVERNIGHT REVERSAL TRADE — COMPLETE MECHANICS

### Context & Setup
- The market has declined **all day** (or risen all day). Price action was below the Blue Line across all timeframes for hours.
- Everything on the Keith Bot dashboard was **red**.
- Overnight, the reversal begins. Timeframes start flipping sequentially from red to green.

### Step-by-Step Execution

**Step 1: Watch for the First Flip**
- After being red all day, the fastest timeframe (1-second or 5-second) will flip to green first.
- This means price action has moved **above** the system's Blue Line on that timeframe.
- This is your first signal that the reversal is beginning.

**Step 2: Confirm Sequential Flips**
- Wait for the next timeframe in order to flip: 5s → 10s → 15s
- When the 1-second, 5-second, and 10-second are all green on all three indices (US30, NAS, SPX), the 15-second is the **next target**.

**Step 3: Find the Lagging Symbol (THE TRADE)**
- On your selected trigger timeframe (the "fourth timeframe" — typically 15s, 20s, or 30s), watch for **four of the five indices to show green, but one remains red**.

**Example on the 15-second:**
- US30 = Green ✅
- NAS = Green ✅
- NQ1 = Green ✅
- SPX = **Red** ← LAGGING SYMBOL
- ES1 = Green ✅

**Step 4: Execute**
- Place a **Buy Stop on the lagging symbol** (in this example, SPX).
- **Target:** The Blue Line of the timeframe where the signal triggered (the 15-second Blue Line).
- **"When one goes up, they all go up."** The lagging symbol will catch up to the others.

### The Robot Signal
- The Keith Bot sends an **automatic signal** when the setup triggers on the fourth timeframe.
- Signal can be configured to display on screen, send to email, or push to phone (via TradingView alert integration).
- The robot tells you when to enter — you don't have to think about it.

---

## THE LAGGING SYMBOL ENTRY RULE — DETAILED

This is the core trade execution rule:

**Setup Condition:** The trigger happens on the **fourth timeframe** (configurable — could be 15s, 20s, or 30s, or even 30-minute).

**The Rule:**
> When US30 is over its fourth time period AND either NAS or SPX is too — leaving **one symbol lagging** — take the trade on the lagging symbol to its Blue Line.

**How the Robot Triggers:**
1. The robot sees US30 turn green on the fourth timeframe
2. NAS or SPX also turn green
3. One symbol stays red (lags behind)
4. The robot sends a signal: "Buy stop on [lagging symbol] to the Blue Line"

**The Logic:**
> "When one goes up, they all go up. When one goes down, they all go down. If one lags, it will catch up to the other five."

This is the single most important principle of the Uno Reverse trade.

---

## DASHBOARD CONFIGURATION — STEP BY STEP

### Purchasing & Setup Flow
1. **Buy the TSTS system** at thesafetytrade.com
2. **Sign the NDA**
3. **Attend training** (every other Monday at 1:00 PM EST, small group setting)
4. **After training, buy the Sniper** ($250/month) — this includes:
   - The **Sniper** indicator (pink, blue, purple lines — the greatest indicator ever)
   - The **Sniper Rifle** (reads above/below Blue Line across all timeframes)
   - The **Uno Reverse Keith Bot** (free upgrade — no additional charge)
5. **Install and configure the Keith Bot**

### Keith Bot Configuration Settings

| Setting | Requirement |
|---------|-------------|
| **US30** | **Must** be included — acts as the anchor symbol for the entire dashboard |
| **Timeframe 1** | Set to your fastest (e.g., 5-second) |
| **Timeframe 2** | Set to next in sequence (e.g., 10-second) |
| **Timeframe 3** | Set to next (e.g., 15-second) |
| **Timeframe 4** | **Your trigger timeframe** — this is where the signal fires (e.g., 20-second or 30-second) |
| **Symbols** | US30, NAS, NQ1, SPX, ES1 (cannot be changed) |
| **Colors** | Leave defaults alone |

### Timeframe Presets for Different Trading Styles

| Style | Setup |
|-------|-------|
| **Scalping** | 5s, 10s, 15s, 20s or 30s |
| **Day Trading (Intermediate)** | 15s, 30s, 1m, 2m or 5m |
| **Long-Term Trading** | 30m, 1h, 4h, Daily |

Kevin's typical live setup: 5s, 10s, 15s, 20s (the 20-second is his fourth/firing timeframe).

---

## TRADE EXECUTION — DETAILED ENTRY & EXIT

### Entry
- The robot sends the signal on the fourth timeframe
- Place a **Buy Stop** on the lagging symbol
- Entry should be just above current price, targeting the Blue Line of the trigger timeframe

### Take Profit Strategy
Kevin uses **multiple take profit levels**:

| Level | Location |
|-------|----------|
| **TP1** | First Orange Line / resistance level |
| **TP2** | Top of the histogram / next resistance |
| **TP3** | The Blue Line of the trigger timeframe |
| **TP4+** | Higher timeframe Blue Lines (for runners) |

The Blue Line is always the primary target. If momentum continues, it may push to the next timeframe's Blue Line.

### Stop Loss
- Place just beyond the swing point where the trend reversed during the reset
- If price breaks that structure, the momentum alignment is officially invalid
- Kevin's philosophy: trust the system — if the setup is correct, you won't need to worry about the stop

---

## COMPREHENSIVE RULES

### Rule 1: The Sequential Order
Safety trades form in order: 1s → 5s → 10s → 15s → 30s → 45s → 1m → 2m → 5m → ... If the 1s, 5s, and 10s have flipped, the 15s is next. You can predict what's coming.

### Rule 2: All Three Must Move Together
US30, NAS, and SPX (and their futures equivalents NQ1, ES1) all move as one. What happens to one happens to all. If one lags, it will catch up.

### Rule 3: The Lagging Symbol Is Your Trade
When four indices are green and one is red on your trigger timeframe, buy the lagging symbol. Target its Blue Line.

### Rule 4: Higher Timeframe Flow Controls Lower Timeframes
If the 6-month, monthly, weekly, and daily are all bullish (green), you only play the buys. You don't play the sells. "The flow of the river is up — why would you go against it?"

### Rule 5: Gold Only Gets Buys
"You only do buys on gold. That's all you do. You do nothing else on gold but buys. Buy, buy, buy, buy, buy."

### Rule 6: The Overnight Context
This trade works because: if they brought price up all day, they'll bring it down overnight. If they brought it down all day, they'll bring it up overnight. It happens 2-5 times per week.

---

## THE SNIPER + SNIPER RIFLE RELATIONSHIP

These two indicators work hand-in-hand:

### The Sniper (Pink, Blue, Purple Lines)
- **Pink Line:** Faster momentum tracker
- **Blue Line:** The "bullseye" — an EMA that acts as gravity/magnet for price
- **Purple Line:** Coincides with actual candle movement
- When the pink line crosses the blue line, you need to go to the next higher timeframe to see what's happening

### The Sniper Rifle (Dashboard)
- Shows whether price is above or below the Blue Line across all timeframes at a glance
- Red = below, Green = above
- The Keith Bot reads the Sniper Rifle data and condenses it further

### The Broken Bot Pattern
When you see green-green-green-red on the candles with the pink line crossing up through the Blue Line, that's a buy stop setup forming. Kevin calls this the "broken bot" pattern.

---

## THE "SNIPER LINED UP" CONCEPT

For the lower timeframe to trigger, the higher timeframes need to be "Sniper Lined Up":

- **Lowest timeframe:** ALL RED at or near its Blue Line (ready to flip)
- **Middle timeframe:** Classic BS/SS (Buy Stop/Sell Stop) — Sniper Lined Up
- **Highest timeframe:** ALL GREEN or ALL RED — Sniper Lined Up Per Rules

When all three line up, the trade is ready.

---

## TRADE FREQUENCY & TIMING

- The overnight reversal happens **2-5 times per week**
- Typically triggered when the market moves hard in one direction during the day
- Best observed: market drops/rises all day → overnight reversal begins
- Kevin usually catches it in the early morning (pre-market)

---

## LIVE EXAMPLE FROM TRANSCRIPT (3/13/25)

Kevin called out the following live, resulting in 330+ pips before market open:

1. Got up in the morning, checked charts
2. Saw 1-second flipped to green on SPX, NAS, and US30
3. Saw 5-second had also flipped to green on all three
4. Saw 10-second had also flipped to green on all three
5. Sent email alert: "Signal Alert: 15s, 30s buy stops to the Blue Line"
6. US30: 175 pips captured (from buy stop entry to the 1-minute Blue Line)
7. NAS: 127 pips captured (same setup)
8. Total: 330+ pips across three indices, zero drawdown

---

## PSYCHOLOGY NOTES (FROM TRANSCRIPT 2)

Kevin emphasizes the mental side of trading:

### Alpha vs Beta Brain Waves
- **Beta (bad):** Stress response, cortisol spiked, fight-or-flight, can't think clearly, can't trade properly
- **Alpha (good):** Calm, healing, parasympathetic mode, releases serotonin/dopamine, can make clear decisions

### How to Get to Alpha
- **Breathing techniques** (Wim Hof, box breathing) — the fastest way
- **Cold therapy** (dunk face in ice water, cold showers)
- **Grounding** (walking barefoot outside, hugging a tree)
- **Binaural beats** at 8-12 Hz (use headphones)
- **Sunshine and walks** (90% of serotonin is made in the gut)
- **Affirmations/Mantras:**
  - "Now I am the voice"
  - "I am in control, not a victim"
  - "I am happy, not sad"
  - "I lead, not follow"
  - "I create, not destroy"
  - "I see every profitable trade easily, not lose trades"
  - "But the truth is I easily see when to enter and exit every trade for the most profit possible"

### Key Trading Psychology Rules
1. You can't trade properly in beta brain waves
2. Stop losses are about fear — trust the system
3. Don't revenge trade when you're in alpha
4. The market is manipulated — they know where it's going. So do we, thanks to the system.
5. All traditional trading education (Fibonacci, VWAP, RSI, volume) is wrong — 97%+ of traders lose money using them

---

## PRINTABLE QUICK REFERENCE CARD

### What It Is
Multi-timeframe convergence dashboard monitoring US30, NAS100, NQ1!, SPX500, ES1!

### How It Works
- Timeframes flip red to green in ascending order (5s → 10s → 15s → 30s...)
- Four indices green + one red on your trigger timeframe = **SETUP**

### The Oreo Sandwich
- **Top cookie:** Higher TFs (15m, 30m, 1H, Daily) already green
- **Cream filling:** Middle TFs still red
- **Bottom cookie:** Lower TFs (5s, 10s, 15s) turning green

### Entry Rule
- Buy Stop on the **lagging symbol**
- Target: Blue Line of trigger timeframe
- Stop: Just beyond swing point

### The Golden Rule
> "When one goes up, they all go up. When one goes down, they all go down. If one lags, it will catch up to the others."

### Setup Required
1. Buy TSTS system → 2. Get trained → 3. Buy Sniper ($250/mo) → 4. Get Keith Bot free → 5. Configure with US30 as anchor → 6. Set your fourth timeframe → 7. Trade when robot signals

### Critical Warning
- Miss the 15s entry → the 30s turn = move already complete = missed entry
- This trade moves FAST. Be watching. Be ready. The sequence does not wait for you.

---

## KEY TERMINOLOGY GLOSSARY

| Term | Definition |
|------|-----------|
| **Blue Line** | An EMA (Exponential Moving Average) that acts as gravity/magnet for price. The target for most trades. |
| **Sniper** | The pink/blue/purple line indicator showing momentum and trend direction |
| **Sniper Rifle** | Dashboard showing above/below Blue Line status across all timeframes |
| **Keith Bot** | The Uno Reverse robot indicator — sends automatic trade signals |
| **Broken Bot** | Pattern of green-green-green-red on candles with pink crossing Blue Line |
| **Lagging Symbol** | The one index still red when four others are green — your trade target |
| **Fourth Timeframe** | The trigger point where the robot sends its signal (configurable) |
| **Safety Trade** | Any trade confirmed by bottom-up confluence of all indicators |
| **Pip** | Percentage in point — unit of price movement |
| **BS (Buy Stop)** | Order placed above current price, triggers buy on reach |
| **SS (Sell Stop)** | Order placed below current price, triggers sell on reach |

---

*Document compiled from:*
- *TSTS Final Course Build (original 7-chapter framework)*
- *"The Safest Trade in the World — The Uno Overnight Reversal — Live Demo Trading 3/13/25" (transcript)*
- *"Mental Side of Trading — The Uno Reverse Indicator & Other Stuff — Great Training Video" (transcript)*
- *"This is the 1 Trade You All Need — Here Is How to Do It! The Overnight Reversal Trade 2/6/26" (transcript)*
