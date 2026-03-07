# Sunaku Glove80 Keymap -> Kinesis Adv360 Pro Translation Plan

## Source Reference
- Repo: `../glove80-keymaps` (sunaku/glove80-keymaps)
- Website: https://sunaku.github.io/moergo-glove80-keyboard.html
- Version: v52 "Glorious Engrammer"

## Scope

**Full translation** of sunaku's keymap to the Kinesis Advantage 360 Pro
(76 keys), then synced to the Glove80 (80 keys). QWERTY as default base layer.

**Translating everything including:**
- All Miryoku-style layers (Cursor, Number, Function, Symbol, System, Lower)
- All alpha layouts (Dvorak, Colemak, QWERTY) -- QWERTY is layer 0
- Bilateral enforcement layers (8 per-finger layers)
- Per-finger home row mod timing
- Thumb keys as layer-tap access (sunaku's layer assignments, our key assignments)
- All combos (thumb combos + any others)
- Typing layer, Gaming layer
- macOS-specific layers

**NOT translating (hardware limitations):**
- Mouse, Mouse_slow, Mouse_fast, Mouse_warp (no HID pointing on Kinesis)
- Emoji, World (require Unicode firmware features)
- RGB per-key indicators (different hardware)
- Difficulty level system (we use sunaku's exact values directly)
- Space/Shift/Thumb forgiveness (can add later if wanted)

---

## Decisions

1. **Thumb layout**: Sunaku's layer-tap assignments, our thumb key choices
2. **Number layer**: Sunaku-style (replaces our keypad)
3. **Per-finger timing**: Sunaku's exact values (differences documented below)
4. **Symbol layer**: Sunaku's (replaces our nav_symbol)
5. **Lower layer**: Yes, adding it
6. **Base layer**: QWERTY as layer 0 (sunaku has Enthium as 0, QWERTY as 3)

---

## 1. Physical Key Mapping

### Glove80 (80 keys) vs Kinesis Adv360 (76 keys)

```
Glove80 (6 rows):                     Kinesis (5 rows):
Row 0: 5+5 = 10  (F-key row)         (no equivalent)
Row 1: 6+6 = 12  (number row)        Row 0: 6+1+1+6 = 14  (number + inner col)
Row 2: 6+6 = 12  (QWERTY row)        Row 1: 6+1+1+6 = 14  (QWERTY + inner col)
Row 3: 6+6 = 12  (home row)          Row 2: 6+1+2+2+1+6 = 18  (home + middle cluster)
Row 4: 6+3+3+6 = 18  (below home)    Row 3: 6+1+1+6 = 14  (below home + center)
Row 5: 5+3+3+5 = 16  (thumb/bottom)  Row 4: 5+3+3+5 = 16  (thumb/bottom)
```

Key differences:
- Kinesis has NO F-key row (handled by Function layer)
- Kinesis has inner column keys on rows 0-2 (7th key on each side)
- Kinesis rows 0-1 have 14 keys each (vs Glove80's 12)
- Both have identical thumb cluster layout (5+3+3+5 = 16)

### Kinesis Key Positions (76 keys)
```
LEFT HAND                                                    RIGHT HAND
Row 0: [ 0][ 1][ 2][ 3][ 4][ 5]  [ 6]                [ 7]  [ 8][ 9][10][11][12][13]
Row 1: [14][15][16][17][18][19]  [20]                  [21]  [22][23][24][25][26][27]
Row 2: [28][29][30][31][32][33]  [34]  [35][36]  [37][38]  [39]  [40][41][42][43][44][45]
Row 3: [46][47][48][49][50][51]        [52]      [53]        [54][55][56][57][58][59]
Row 4: [60][61][62][63][64]      [65][66][67]  [68][69][70]      [71][72][73][74][75]
```

---

## 2. Layer Architecture

### Sunaku's layers -> Kinesis layers

| Kinesis # | Name | Sunaku # | Sunaku name | Notes |
|-----------|------|----------|-------------|-------|
| 0 | QWERTY | 3 | LAYER_QWERTY | Our default base layer |
| 1 | Dvorak | 1 | LAYER_Dvorak | Alpha layout option |
| 2 | Colemak | 2 | LAYER_Colemak | Alpha layout option |
| 3 | macOS | 4 | LAYER_macOS | OS-specific overrides |
| 4 | Typing | 5 | LAYER_Typing | No home row mods |
| 5 | LeftPinky | 6 | LAYER_LeftPinky | Bilateral enforcement |
| 6 | LeftRingy | 7 | LAYER_LeftRingy | Bilateral enforcement |
| 7 | LeftMiddy | 8 | LAYER_LeftMiddy | Bilateral enforcement |
| 8 | LeftIndex | 9 | LAYER_LeftIndex | Bilateral enforcement |
| 9 | RightIndex | 10 | LAYER_RightIndex | Bilateral enforcement |
| 10 | RightMiddy | 11 | LAYER_RightMiddy | Bilateral enforcement |
| 11 | RightRingy | 12 | LAYER_RightRingy | Bilateral enforcement |
| 12 | RightPinky | 13 | LAYER_RightPinky | Bilateral enforcement |
| 13 | Gaming | 14 | LAYER_Gaming | Gaming mode |
| 14 | Cursor | 15 | LAYER_Cursor | Arrows, navigation |
| 15 | Number | 16 | LAYER_Number | Numpad, hex |
| 16 | Function | 17 | LAYER_Function | F-keys, media |
| 17 | macOS_left | 18 | LAYER_macOS_left | macOS cursor variant |
| 18 | Symbol | 19 | LAYER_Symbol | Programming symbols |
| 19 | System | 21 | LAYER_System | BT, power, boot |
| 20 | macOS_right | 22 | LAYER_macOS_right | macOS symbol variant |
| 21 | Factory | 25 | LAYER_Factory | Factory default fallback |
| 22 | Lower | 26 | LAYER_Lower | Layer toggles, sticky mods |
| 23 | macOS_lower | 27 | LAYER_macOS_lower | macOS lower variant |
| 24 | Mod (BT) | 31 | LAYER_Magic | BT, bootloader, RGB |

**Dropped layers** (hardware limitations):
- Mouse, Mouse_slow, Mouse_fast, Mouse_warp (no HID pointing)
- Emoji, World (require Unicode firmware)

Total: 25 layers (Kinesis Adv360 supports up to 32)

---

## 3. Thumb Cluster Design

### Sunaku's layer-tap assignments applied to our thumb keys

```
Sunaku thumb access:                  Our Kinesis thumb keys:
LT4 = Space / Cursor          ->     [65] Return / Cursor
LT5 = Tab / Number            ->     [66] Tab / Number
LT6 = PgDn (no layer)         ->     [67] Backspace
LT1 = Esc / Function          ->     center key area
LT2 = Insert / Lower          ->     center key area
LT3 = PgUp (no layer)         ->     (bottom row key)

RT4 = R / Symbol              ->     [70] Space / Symbol
RT5 = Backspace / Mouse       ->     [69] Backspace (no mouse, plain key)
RT6 = (no layer)              ->     (bottom row key)
RT1 = Enter / System          ->     [68] Return / System
RT2 = Delete / Lower          ->     center key area
RT3 = (no layer)              ->     (bottom row key)
```

### Final Kinesis thumb mapping

```
Left thumb cluster:                Right thumb cluster:
[65] Return / Cursor layer         [68] Return / System layer
[66] Tab / Number layer            [69] Backspace
[67] Backspace                     [70] Space / Symbol layer

Center keys:
[52] Space / Lower layer (or Esc / Function)
[53] Delete / Lower layer (or similar)
```

**Open**: positions 52/53 need to carry Function and Lower access.
Options:
- `[52] = lt Function ESC`, `[53] = lt Lower DELETE`
- Or use combos on thumb keys for Function/Lower access

Kinesis inner column keys (6, 7, 20, 21, 34, 39) available for:
tog layers, screenshots, lock screen -- same as current layout.

---

## 4. Per-Finger Home Row Mod Timing

### Current values (urob-style, uniform)
```
ALL fingers:
  tapping-term-ms     = 280
  quick-tap-ms        = 175
  require-prior-idle  = 150
  flavor              = balanced
```

### Sunaku's values (per-finger, DIFFICULTY_LEVEL 0)
```
                    tapping-term  quick-tap  require-prior-idle  flavor
Pinky (A, ;):         270           300          150             balanced
Ring  (S, L):         240           300          150             balanced
Middle (D, K):        210           300          150             balanced
Index (F, J):         180           300          150             balanced
```

### What to expect (differences from current)

| Change | Current | New | Effect |
|--------|---------|-----|--------|
| Pinky tapping-term | 280ms | 270ms | Barely noticeable (-10ms). |
| Ring tapping-term | 280ms | 240ms | Moderate speedup (-40ms). Ring mods activate sooner. |
| Middle tapping-term | 280ms | 210ms | Noticeable speedup (-70ms). Cmd on D/K is snappier. |
| **Index tapping-term** | **280ms** | **180ms** | **Biggest change (-100ms).** Shift on F/J activates much faster. More responsive but higher misfire risk during fast typing. The `require-prior-idle-ms=150` guards against this during flow. |
| **quick-tap-ms** | **175ms** | **300ms** | **Much more forgiving for double-taps.** You have nearly twice as long to tap a key twice and get two plain taps. Good for repeat typing (e.g., `ff`, `jj`). |
| require-prior-idle | 150ms | 150ms | Unchanged. Primary misfire guard stays the same. |

**Summary of what you'll feel:**
- **Index (F/J = Shift)**: Noticeably faster hold activation. Watch for accidental shifts when rolling into F/J quickly after a pause.
- **Middle (D/K = Cmd)**: Cmd shortcuts feel snappier.
- **Ring (S/L = Alt)**: Slight speedup, barely noticeable.
- **Pinky (A/; = Ctrl)**: Basically the same.
- **Double-tapping all keys**: More forgiving (300ms vs 175ms window).

**Tuning if needed:**
- Index misfires: raise index tapping-term from 180 to 200-220
- Any finger sluggish: lower its tapping-term by 20-30ms
- Double-tap feels wrong: adjust quick-tap-ms

### Implementation: 8 behaviors instead of 2

Replace `hml`/`hmr` with per-finger variants:
```
hml_pinky / hmr_pinky   (for A, ;)
hml_ring  / hmr_ring    (for S, L)
hml_mid   / hmr_mid     (for D, K)
hml_index / hmr_index   (for F, J)
```

Each with its own `tapping-term-ms` and same `hold-trigger-key-positions`
as current (left positions for right mods, vice versa).

---

## 5. Bilateral Enforcement

Prevents single-handed home row mod activation using 8 per-finger layers.

**How it works:**
1. Hold `A` (left pinky = Ctrl)
2. LeftPinky layer activates momentarily alongside the modifier
3. Right-hand keys pass through (`&trans`) -- Ctrl+J, Ctrl+K work normally
4. Left-hand keys are plain `&kp` taps on LeftPinky layer -- cancels Ctrl
5. Only opposite-hand keys produce modified output

**Trade-off:** Can't do same-hand shortcuts (e.g., Ctrl+A with left hand).
Workaround: Use Lower layer's sticky mods or combos for one-handed shortcuts.

**Implementation:** Each per-finger behavior has two variants:
- `left_pinky` -- standard hold-tap
- `left_pinky_bilateral` -- triggers a macro that presses mod + activates the per-finger layer

Base layer uses `_bilateral` variant. Other layers use standard variant.

---

## 6. Key Position Mapping (Kinesis <-> Glove80)

```
Kinesis -> Glove80 position map:

Glove80 Row 0 (F-keys): G[0-9] = no Kinesis equivalent

Row 0/1 (numbers):
  K[0]->G[10]  K[1]->G[11]  K[2]->G[12]  K[3]->G[13]  K[4]->G[14]  K[5]->G[15]
  K[6]->(drop)  K[7]->(drop)
  K[8]->G[16]  K[9]->G[17]  K[10]->G[18] K[11]->G[19] K[12]->G[20] K[13]->G[21]

Row 1/2 (QWERTY):
  K[14]->G[22] K[15]->G[23] K[16]->G[24] K[17]->G[25] K[18]->G[26] K[19]->G[27]
  K[20]->(drop) K[21]->(drop)
  K[22]->G[28] K[23]->G[29] K[24]->G[30] K[25]->G[31] K[26]->G[32] K[27]->G[33]

Row 2/3 (home):
  K[28]->G[34] K[29]->G[35] K[30]->G[36] K[31]->G[37] K[32]->G[38] K[33]->G[39]
  K[34]->(drop, inner col)  K[39]->(drop, inner col)
  K[35]->G[52] K[36]->G[53]  (center-left -> Glove80 Row4 middle)
  K[37]->G[56] K[38]->G[57]  (center-right -> Glove80 Row4 middle)
  K[40]->G[40] K[41]->G[41] K[42]->G[42] K[43]->G[43] K[44]->G[44] K[45]->G[45]

Row 3/4 (below home):
  K[46]->G[46] K[47]->G[47] K[48]->G[48] K[49]->G[49] K[50]->G[50] K[51]->G[51]
  K[52]->G[54] K[53]->G[55]  (center -> Glove80 Row4 middle)
  K[54]->G[58] K[55]->G[59] K[56]->G[60] K[57]->G[61] K[58]->G[62] K[59]->G[63]

Row 4/5 (thumb/bottom):
  K[60]->G[64] K[61]->G[65] K[62]->G[66] K[63]->G[67] K[64]->G[68]
  K[65]->G[69] K[66]->G[70] K[67]->G[71]
  K[68]->G[72] K[69]->G[73] K[70]->G[74]
  K[71]->G[75] K[72]->G[76] K[73]->G[77] K[74]->G[78] K[75]->G[79]
```

**Inner column keys** (K[6], K[7], K[20], K[21], K[34], K[39]):
These 6 keys exist on Kinesis but not on Glove80's equivalent rows.
- Syncing to Glove80: place on F-key row (G[0-9]) or drop
- Syncing from Glove80: F-key row content goes to these or Function layer

---

## 7. Implementation TODO

### Current layer numbering (compact, will expand)
| # | Layer | Notes |
|---|-------|-------|
| 0 | QWERTY | default base layer |
| 1 | Cursor | arrows, navigation, select word/line |
| 2 | Number | numpad, hex, operators |
| 3 | Mod | BT, bootloader, RGB (kept from original) |
| 4 | Symbol | programming symbols |
| 5 | Function | F-keys, media, brightness |
| 6 | System | RGB, locks, system controls |
| 7 | Lower | layer toggles, sticky mods |

### Phase 1: Foundation
| # | Task | Status |
|---|------|--------|
| 1.1 | Define layer `#define` constants + key positions | Done |
| 1.2 | Create 8 per-finger hold-tap behaviors | Done |
| 1.3 | Port macros (select_word, select_line, mod_tab, etc.) | Done |
| 1.4 | Port helper behaviors (sticky keys) | Done |

### Phase 2: Core layers
| # | Task | Status |
|---|------|--------|
| 2.1 | QWERTY base layer with per-finger HRMs + thumb layer-tap | Done |
| 2.2 | Cursor layer (1) | Done |
| 2.3 | Number layer (2) | Done |
| 2.4 | Function layer (5) | Done |
| 2.5 | Symbol layer (4) | Done |
| 2.6 | System layer (6) | Done |
| 2.7 | Lower layer (7) | Done |

### Phase 3: Infrastructure
| # | Task | Status |
|---|------|--------|
| 3.1 | Implement 8 bilateral enforcement layers | Done |
| 3.2 | Implement sunaku-style thumb combos | Done |
| 3.3 | Update existing combos to use layer defines | Done |

### Phase 4: Extra layers
| # | Task | Status |
|---|------|--------|
| 4.1 | Implement Dvorak base layer | Pending |
| 4.2 | Implement Colemak base layer | Pending |
| 4.3 | Implement macOS overlay layers | Pending |
| 4.4 | Implement Typing layer (no HRMs) | Pending |
| 4.5 | Implement Gaming layer | Pending |
| 4.6 | Implement Factory layer | Pending |

### Phase 5: Sync & tooling
| # | Task | Status |
|---|------|--------|
| 5.1 | Sync all changes to Glove80 config | Pending |
| 5.2 | Build translation script (Kinesis <-> Glove80) -- shell or Swift | Pending |
