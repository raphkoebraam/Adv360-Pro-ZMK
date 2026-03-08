# Advantage 360 Pro — Layout Documentation

## Overview

Sunaku-style Miryoku layout translated from [sunaku/glove80-keymaps](https://github.com/sunaku/glove80-keymaps) v52
to the Kinesis Advantage 360 Pro (76 keys). Optimized for macOS with QWERTY as the default base layer.

Key design principles (from sunaku):
- **Home row mods on the row BELOW home** (ZXCV / M,./) — per-finger timing, bilateral enforcement
- **Hyper key on index fingers** (F/J hold) — global shortcuts without modifier chording
- **Thumb keys as layer-tap** — hold for layer access, tap for common keys
- **Thumb combos** — two-thumb chords for sticky shift, caps word, alt-tab, etc.
- **Alpha row combos** — cut/copy/paste/undo/redo on QWER and UIOP rows

OS Input Source: **ABC** (no dead keys — backtick, quote, tilde all type directly)


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

- 6, 7: Inner column top (left, right)
- 20, 21: Inner column middle
- 34, 39: Inner column home row
- 35-36: Center cluster left pair
- 37-38: Center cluster right pair
- 52-53: Center thumb keys
- 65-67: Left thumb cluster
- 68-70: Right thumb cluster


## Layer 0 — Default (QWERTY)

### Visual Layout

```
LEFT HAND                                                                     RIGHT HAND
  =      1      2      3      4      5    [Mod]                       [Mod]     6      7      8      9      0      -
  @      Q      W      E      R      T    [Scr3]                     [Scr5]    Y      U      I      O      P      \
 ESC     A      S      D    F|Hyp    G    [Scr4]   `   [#|Scr4] [=] [^|Scr5] [Lock]   H    J|Hyp    K      L      ;      '
 LSh  Z|Ctrl  X|Alt  C|Cmd  V|Shft   B          [Esc|Fn] [Del|Low]         N   M|Shft ,|Cmd  .|Alt  /|Ctrl  RSh
[Mod]  End    PgUp   PgDn   Home       [Ret|Cur] [Tab|Num] [Bksp] [Ret|Sys] [Bksp] [Spc|Sym]      Left   Down    Up   Right [Mod]
```

### Row 0 — Number Row

| Pos | Key | Notes |
|-----|-----|-------|
| 0 | `=` | Equals (standard `=`, Shift gives `+`) |
| 1-5 | `1` `2` `3` `4` `5` | Standard numbers |
| 6 | `mo Mod` | Inner column — momentary Mod/BT layer |
| 7 | `mo Mod` | Inner column — momentary Mod/BT layer |
| 8-12 | `6` `7` `8` `9` `0` | Standard numbers |
| 13 | `-` | Minus (Shift gives `_`) |

### Row 1 — Top Alpha

| Pos | Key | Notes |
|-----|-----|-------|
| 14 | `@` (`LS(N2)`) | Critical for ObjC/Swift (`@interface`, `@State`) |
| 15-19 | `Q` `W` `E` `R` `T` | Standard QWERTY |
| 20 | `Cmd+Shift+3` | macOS full screenshot |
| 21 | `Cmd+Shift+5` | macOS screen recording |
| 22-26 | `Y` `U` `I` `O` `P` | Standard QWERTY |
| 27 | `\` | Backslash (Shift gives `|`) |

### Row 2 — Home Row

| Pos | Key | Tap | Hold | Notes |
|-----|-----|-----|------|-------|
| 28 | ESC | `Escape` | — | |
| 29-31 | A S D | letter | — | Plain keys (no mods — mods are on row below) |
| 32 | F | `F` | Hyper (`Ctrl+Alt+Cmd+Shift`) | `left_index` behavior, 180ms tapping-term |
| 33 | G | `G` | — | Plain key |
| 34 | Scr4 | `Cmd+Shift+4` | — | Inner column — macOS area screenshot |
| 35 | `` ` `` | Grave/backtick | — | Center cluster |
| 36 | #/Scr4 | `#` (`LS(N3)`) | — | Mod-morph: Shift sends `Cmd+Shift+4` |
| 37 | `=` | Equals | — | Center cluster |
| 38 | ^/Scr5 | `^` (`LS(N6)`) | — | Mod-morph: Shift sends `Cmd+Shift+5` |
| 39 | Lock | `Ctrl+Cmd+Q` | — | Inner column — macOS lock screen |
| 40 | H | `H` | — | Plain key |
| 41 | J | `J` | Hyper (`Ctrl+Alt+Cmd+Shift`) | `right_index` behavior, 180ms tapping-term |
| 42-44 | K L ; | letter | — | Plain keys |
| 45 | `'` | Single quote | — | Rust lifetimes, string delimiters |

### Row 3 — Below Home (Home Row Mods)

This is where the modifiers live. Per-finger timing from sunaku, positional enforcement
(only opposite-hand keys trigger hold), `hold-trigger-on-release` enabled.

| Pos | Tap | Hold | Finger | Tapping-term |
|-----|-----|------|--------|-------------|
| 46 | — | Left Shift | — | Dedicated shift key |
| 47 | Z | Left Ctrl (`LCTL`) | Pinky | 270ms |
| 48 | X | Left Alt (`LALT`) | Ring | 240ms |
| 49 | C | Left Cmd (`LGUI`) | Middle | 210ms |
| 50 | V | Left Shift (`LSFT`) | Index | 180ms |
| 51 | B | — | — | Plain key |
| 54 | N | — | — | Plain key |
| 55 | M | Right Shift (`LSFT`) | Index | 180ms |
| 56 | `,` | Right Cmd (`LGUI`) | Middle | 210ms |
| 57 | `.` | Right Alt (`LALT`) | Ring | 240ms |
| 58 | `/` | Right Ctrl (`LCTL`) | Pinky | 270ms |
| 59 | — | Right Shift | — | Dedicated shift key |

**Modifier order** (pinky to index): Ctrl, Alt, Cmd, Shift — mirrored on both hands.

**Misfire prevention** (three-layer defense):
1. `require-prior-idle-ms = 150` — during typing flow (50-100ms between keys), hold-tap always resolves as tap
2. Positional hold-trigger — same-hand keys always produce tap; only opposite-hand keys can trigger hold
3. `hold-trigger-on-release` — allows deliberately chording two mods on the same hand
4. `quick-tap-ms = 300` — double-tapping always produces two taps (generous window)

**Bilateral enforcement** (optional, currently disabled via `ENFORCE_BILATERAL`):
When enabled, holding a mod activates a per-finger bilateral layer where same-hand keys
are remapped to cancel the modifier, ensuring only cross-hand mod+key combinations work.

### Center Thumb Keys (Row 3)

| Pos | Tap | Hold | Sunaku equiv |
|-----|-----|------|-------------|
| 52 | `Escape` | `mo Function` | T1 (Esc/Function) |
| 53 | `Delete` | `mo Lower` | T2 (Del/Lower) |

### Row 4 — Bottom Row + Thumb Cluster

| Pos | Tap | Hold | Sunaku equiv |
|-----|-----|------|-------------|
| 60 | — | `mo Mod` | — |
| 61-64 | End, PgUp, PgDn, Home | — | — |
| **65** | **Return** | **`mo Cursor`** | **T4 (main left thumb)** |
| **66** | **Tab** | **`mo Number`** | **T5** |
| **67** | Backspace | — | T6 |
| **68** | **Return** | **`mo System`** | **T1 (main right thumb)** |
| **69** | Backspace | — | T5 |
| **70** | **Space** | **`mo Symbol`** | **T4 (main right thumb)** |
| 71-74 | Left, Down, Up, Right | — | — |
| 75 | — | `mo Mod` | — |

Thumb layer-tap uses `balanced` flavor, 200ms tapping-term, 300ms quick-tap.


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

### Alpha Row Combos (QWER / UIOP)

Mirrored on both hands. All use `timeout-ms = 50`, `require-prior-idle-ms = 150`.

| Action | Left hand | Right hand |
|--------|-----------|------------|
| Cut (`Cmd+X`) | Q+W (15+16) | O+P (25+26) |
| Copy (`Cmd+C`) | W+E (16+17) | I+O (24+25) |
| Paste (`Cmd+V`) | E+R (17+18) | U+I (23+24) |
| Undo (`Cmd+Z`) | W+R (16+18) | U+O (23+25) |
| Redo (`Cmd+Shift+Z`) | Q+E (15+17) | I+P (24+26) |
| Select All (`Cmd+A`) | Q+R (15+18) | U+P (23+26) |

### Home Row Combos

| Action | Keys |
|--------|------|
| Caps Word | F+J (32+41) |
| Caps Lock | V+M (50+55) |

### Thumb Combos (sunaku-style)

Using sunaku's T1-T6 naming. All use `timeout-ms = 50`.

| Combo | Left hand | Right hand | Action |
|-------|-----------|------------|--------|
| T1+T2 | 52+53 | — | Sticky AltGr (`&sk RALT`) |
| T1+T4 | 52+65 | 68+70 | Alt-Tab switcher (LH) / Hyper (RH) |
| T2+T5 | 53+66 | — | Ctrl-Tab switcher |
| T1+T5 | 52+66 | 68+69 | Sticky Shift (one-shot) |
| T4+T5 | 65+66 | 70+69 | Caps Word |
| T2+T6 | 53+67 | — | Caps Lock |
| T1+T2+T4 | 52+53+65 | 68+70+69 | Base layer reset (safety: 3-key chord) |


## Configuration Reference

### Timing Constants (from `layers.dtsi`)

| Constant | Value | Purpose |
|----------|-------|---------|
| `PINKY_HOLDING_TIME` | 270ms | Tapping-term for pinky HRMs (A/;, Z//) |
| `RINGY_HOLDING_TIME` | 240ms | Tapping-term for ring HRMs (S/L, X/.) |
| `MIDDY_HOLDING_TIME` | 210ms | Tapping-term for middle HRMs (D/K, C/,) |
| `INDEX_HOLDING_TIME` | 180ms | Tapping-term for index HRMs (F/J, V/M) |
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

### macOS Shortcuts (built into default layer)

| Key | Position | Shortcut |
|-----|----------|----------|
| `Cmd+Shift+3` | 20 | Full screenshot |
| `Cmd+Shift+4` | 34 | Area screenshot |
| `Cmd+Shift+5` | 21 / Shift+38 | Screen recording |
| `Cmd+Shift+4` | Shift+36 | Area screenshot (alt position) |
| `Ctrl+Cmd+Q` | 39 | Lock screen |
