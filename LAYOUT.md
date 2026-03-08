# Advantage 360 Pro — Layout Documentation

## Overview

Custom layout for the Kinesis Advantage 360 Pro (76 keys), inspired by
[sunaku/glove80-keymaps](https://github.com/sunaku/glove80-keymaps) v52.
Optimized for macOS with QWERTY base.

Design principles:
- **Home row mods on the row BELOW home** (ZXCV / M,./) with per-finger timing
- **Hyper on index fingers** (F/J hold) for global shortcuts
- **Layer access via thumb hold** — 6 layers on thumb keys
- **Combos** on alpha row (cut/copy/paste) and thumb keys (sticky shift, caps, alt-tab)

OS Input Source: **ABC** (no dead keys)


## ZMK Version

Defined in `config/west.yml`. Currently using the **ReFil/Kinesis fork** of ZMK:

```yaml
remote: refil                  # github.com/refil/zmk
revision: adv360-z3.5          # Zephyr 3.5 based branch
```

Kinesis is winding down support. Options for staying current:
- **Mainline ZMK** (`zmkfirmware/zmk`) — most future-proof, loses RGB indicator LEDs
- **Community fork** ([craftyguy/Adv360-Pro-ZMK](https://git.sr.ht/~craftyguy/Adv360-Pro-ZMK)) — tracks closer to mainline with Adv360 support


## Physical Key Positions

```
LEFT HAND                                                    RIGHT HAND
Row 0: [ 0][ 1][ 2][ 3][ 4][ 5]  [ 6]                [ 7]  [ 8][ 9][10][11][12][13]
Row 1: [14][15][16][17][18][19]  [20]                  [21]  [22][23][24][25][26][27]
Row 2: [28][29][30][31][32][33]  [34]  [35][36]  [37][38]  [39]  [40][41][42][43][44][45]
Row 3: [46][47][48][49][50][51]        [52]      [53]        [54][55][56][57][58][59]
Row 4: [60][61][62][63][64]      [65][66][67]  [68][69][70]      [71][72][73][74][75]
```


---


## Layer 0 — Default (QWERTY)

### What You Type (tap)

Left and right hand shown separately for readability. Center/inner keys listed below.

```
LEFT HAND                          RIGHT HAND
 =    1    2    3    4    5         6    7    8    9    0    -
 @    Q    W    E    R    T         Y    U    I    O    P    \
ESC   A    S    D    F    G         H    J    K    L    ;    '
LSh   Z    X    C    V    B         N    M    ,    .    /   RSh
Mod  End  PgUp PgDn Home           Left Down  Up  Right   Mod
```

### What You Get When You Hold

Only keys with hold behavior are listed. Everything else is tap-only.

```
LEFT HAND (hold)                   RIGHT HAND (hold)
 .    .    .    .    .    .         .    .    .    .    .    .
 .    .    .    .    .    .         .    .    .    .    .    .
 .    .    .    .   HYP   .         .   HYP   .    .    .    .
 .   Ctrl  Alt  Cmd  Shft .         .   Shft Cmd  Alt  Ctrl  .
 .    .    .    .    .              .    .    .    .    .
```

`.` = no hold behavior (tap only)

### Inner Column + Center Keys

These are the keys between the two hands (positions 6-7, 20-21, 34-39, 52-53):

```
         LEFT INNER    CENTER CLUSTER    RIGHT INNER
Row 0:     [Mod]                           [Mod]
Row 1:     [Scr3]                          [Scr5]
Row 2:     [Scr4]      `  [#|Scr4]  =  [^|Scr5]  [Lock]
Row 3:            [Esc|Fn]  [Del|Low]
```

| Pos | Tap | Hold/Shift | Notes |
|-----|-----|------------|-------|
| 6, 7 | — | `mo Mod` | BT/bootloader layer |
| 20 | `Cmd+Shift+3` | — | macOS full screenshot |
| 21 | `Cmd+Shift+5` | — | macOS screen recording |
| 34 | `Cmd+Shift+4` | — | macOS area screenshot |
| 35 | `` ` `` | — | Backtick |
| 36 | `#` | Shift: `Cmd+Shift+4` | Mod-morph |
| 37 | `=` | — | Equals |
| 38 | `^` | Shift: `Cmd+Shift+5` | Mod-morph |
| 39 | `Ctrl+Cmd+Q` | — | macOS lock screen |
| 52 | **Escape** | **`mo Function`** | Center thumb left |
| 53 | **Delete** | **`mo Lower`** | Center thumb right |

### Thumb Cluster

```
LEFT THUMB                         RIGHT THUMB
  [Ret|Cursor] [Tab|Number] [Bksp]    [Ret|System] [Bksp] [Spc|Symbol]
       65           66        67           68         69        70
```

| Pos | Tap | Hold (layer) | Notes |
|-----|-----|-------------|-------|
| **65** | **Return** | **Cursor** | Primary left thumb |
| **66** | **Tab** | **Number** | |
| 67 | Backspace | — | |
| **68** | **Return** | **System** | Primary right thumb |
| 69 | Backspace | — | |
| **70** | **Space** | **Symbol** | Primary right thumb |

Thumb layer-tap: `balanced` flavor, 200ms tapping-term, 300ms quick-tap.


### Home Row Mods Detail

Mods live on Row 3 (below home row). Per-finger timing — faster fingers get shorter
tapping-terms. Modifier order (pinky to index): **Ctrl, Alt, Cmd, Shift**.

```
LEFT:   Z=Ctrl  X=Alt  C=Cmd  V=Shift
RIGHT:  /=Ctrl  .=Alt  ,=Cmd  M=Shift
```

| Finger | Keys | Mod | Tapping-term |
|--------|------|-----|-------------|
| Pinky | Z, / | Ctrl | 270ms |
| Ring | X, . | Alt | 240ms |
| Middle | C, , | Cmd | 210ms |
| Index | V, M | Shift | 180ms |

**Misfire prevention:**
1. `require-prior-idle-ms = 150` — during typing flow, hold-tap always resolves as tap
2. Positional hold-trigger — same-hand keys always produce tap; only opposite-hand triggers hold
3. `hold-trigger-on-release` — allows deliberately chording two mods on the same hand
4. `quick-tap-ms = 300` — double-tapping always produces two taps

**Bilateral enforcement** (optional, currently disabled via `ENFORCE_BILATERAL`):
When enabled, holding a mod activates a per-finger layer that cancels the modifier
for same-hand keys, ensuring only cross-hand mod+key combinations work.


---


## Layers

| # | Name | Access | Purpose |
|---|------|--------|---------|
| 0 | QWERTY | default | Base typing layer |
| 1 | Cursor | hold 65 (Return) | Arrows, select word/line, cut/copy/paste, find |
| 2 | Number | hold 66 (Tab) | Numpad, hex digits, operators |
| 3 | Mod | hold 6/7/60/75 | BT profiles, bootloader, RGB |
| 4 | Symbol | hold 70 (Space) | Programming symbols, code macros |
| 5 | Function | hold 52 (Esc) | F-keys, media, brightness |
| 6 | System | hold 68 (Return) | RGB, locks, power, system controls |
| 7 | Lower | hold 53 (Delete) | Layer toggles, sticky mods |
| 8-15 | Bilateral | auto (HRM hold) | Per-finger enforcement layers (8 total) |
| 16 | Typing | toggle via Lower | No home row mods (pure typing) |
| 17 | Gaming | toggle via Lower | WASD-optimized, no hold-taps |
| 18 | Dvorak | toggle via System | Alternative alpha layout |
| 19 | Colemak | toggle via System | Alternative alpha layout |
| 20 | Factory | toggle via System | Fallback QWERTY, no behaviors |


## Combos

### Alpha Row (QWER / UIOP)

Mirrored on both hands. All use `timeout-ms = 50`, `require-prior-idle-ms = 150`.

```
LEFT:   Q --- W --- E --- R           RIGHT:  U --- I --- O --- P
         cut  copy paste                       paste copy  cut
              undo                                   undo
         redo                                        redo
        select all                            select all
```

| Action | Left | Right |
|--------|------|-------|
| Cut | Q+W | O+P |
| Copy | W+E | I+O |
| Paste | E+R | U+I |
| Undo | W+R | U+O |
| Redo | Q+E | I+P |
| Select All | Q+R | U+P |

### Home Row

| Action | Keys |
|--------|------|
| Caps Word | F+J (32+41) |
| Caps Lock | V+M (50+55) |

### Thumb Combos

Two-thumb chords. All use `timeout-ms = 50`.

```
LEFT THUMB:   [Esc|Fn=52] [Del|Low=53]     [Ret|Cur=65] [Tab|Num=66] [Bksp=67]
RIGHT THUMB:  [Ret|Sys=68] [Bksp=69] [Spc|Sym=70]
```

| Combo | Left hand | Right hand | Action |
|-------|-----------|------------|--------|
| 52+53 | Esc + Del | — | Sticky AltGr |
| 52+65 | Esc + Ret | — | Alt-Tab switcher |
| 68+70 | — | Ret + Spc | Hyper |
| 53+66 | Del + Tab | — | Ctrl-Tab switcher |
| 52+66 | Esc + Tab | 68+69 (Ret + Bksp) | Sticky Shift (one-shot) |
| 65+66 | Ret + Tab | 70+69 (Spc + Bksp) | Caps Word |
| 53+67 | Del + Bksp | — | Caps Lock |
| 52+53+65 | Esc+Del+Ret | 68+70+69 | Base layer reset (3-key safety) |


## Configuration Reference

### Timing Constants (`layers.dtsi`)

| Constant | Value | Purpose |
|----------|-------|---------|
| `PINKY_HOLDING_TIME` | 270ms | Tapping-term for pinky (Z/;, //.) |
| `RINGY_HOLDING_TIME` | 240ms | Tapping-term for ring (X/., L/.) |
| `MIDDY_HOLDING_TIME` | 210ms | Tapping-term for middle (C/,, D/K) |
| `INDEX_HOLDING_TIME` | 180ms | Tapping-term for index (V/M, F/J) |
| `HOMEY_HOLDING_TYPE` | tap-preferred | HRM flavor |
| `HOMEY_STREAK_DECAY` | 150ms | `require-prior-idle-ms` for HRMs |
| `HOMEY_REPEAT_DECAY` | 300ms | `quick-tap-ms` for HRMs |
| `THUMB_HOLDING_TIME` | 200ms | Tapping-term for thumb layer-taps |
| `THUMB_HOLDING_TYPE` | balanced | Thumb layer-tap flavor |
| `THUMB_REPEAT_DECAY` | 300ms | `quick-tap-ms` for thumbs |
| `COMBO_FIRING_DECAY` | 50ms | Combo `timeout-ms` |

### File Structure

| File | Purpose |
|------|---------|
| `config/adv360.keymap` | Main keymap: behaviors, combos, all layer bindings |
| `config/layers.dtsi` | Layer defines, key positions, timing, mod assignments, HRM macros |
| `config/macros.dtsi` | Included in `behaviors{}`: select_word/line, bilateral hold/tap, mod_tab |
| `config/west.yml` | ZMK version/fork reference |
