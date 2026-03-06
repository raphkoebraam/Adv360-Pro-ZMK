# Advantage 360 Pro — Custom Layout Documentation

## Overview

Custom ZMK layout optimized for software engineering (Swift, Objective-C, Rust) with
minimal finger and hand movement. Based on QWERTY with the following philosophy:

- **Home row mods on the row BELOW home** — avoids misfires common with true home row mods (planned: move back to home row with urob's timeless config)
- **Brackets/parens on number row via Shift** — `{`, `[`, `(` are Shift+2/3/4; closing mirrors on 7/8/9
- **Hyper key on G and H** — for global shortcuts without modifier chording
- **Caps Word combo** — F+J activates smart caps (for CONSTANT_NAMES)
- **macOS integration** — screenshot shortcuts, lock screen, media controls built in

OS Input Source: **ABC** (previously US International — no dead keys, all characters are direct)


## Physical Key Positions

```
LEFT HAND                                                    RIGHT HAND
Row 0: [ 0][ 1][ 2][ 3][ 4][ 5]  [ 6]                [ 7]  [ 8][ 9][10][11][12][13]
Row 1: [14][15][16][17][18][19]  [20]                  [21]  [22][23][24][25][26][27]
Row 2: [28][29][30][31][32][33]  [34]  [35][36]  [37][38]  [39]  [40][41][42][43][44][45]
Row 3: [46][47][48][49][50][51]        [52]      [53]        [54][55][56][57][58][59]
Row 4: [60][61][62][63][64]      [65][66][67]  [68][69][70]      [71][72][73][74][75]
```

Positions 35-38 = inner thumb keys, 52-53 = center thumb, 65-70 = lower thumb cluster.


## Layer 0 — Default

### Row 0: Number Row (mod-morph: tap / Shift)

```
  ~(+)   1(!)   2({)   3([)   4(()   5(%)  [tog1]     [mo3]   6(&)   7())   8(])   9(})   0(*)    -
```

The Shift layer replaces standard shifted numbers with bracket pairs and common
coding symbols. Opening brackets are on the left hand (2/3/4), closing on the
right (7/8/9), creating a symmetric pair:

| Key | Tap | Shift | Notes |
|-----|-----|-------|-------|
| 0   | ~   | +     | sr_lh_1 mod-morph |
| 1   | 1   | !     | sr_lh_2 — force unwrap (Swift), macro invocation (Rust) |
| 2   | 2   | {     | sr_lh_3 — opening brace |
| 3   | 3   | [     | sr_lh_4 — opening bracket (ObjC message sending) |
| 4   | 4   | (     | sr_lh_5 — opening paren |
| 5   | 5   | %     | sr_lh_6 |
| 6   | tog 1 | —   | Toggle keypad layer |
| 7   | mo 3  | —   | Momentary system layer |
| 8   | 6   | &     | sr_rh_1 — reference (Rust) |
| 9   | 7   | )     | sr_rh_2 — closing paren |
| 10  | 8   | ]     | sr_rh_3 — closing bracket |
| 11  | 9   | }     | sr_rh_4 — closing brace |
| 12  | 0   | *     | sr_rh_5 — pointer/deref (ObjC, Rust) |
| 13  | -   | _     | Standard (underscore via Shift) |

### Row 1: Top Alpha

```
   @      Q      W      E      R      T    [Scr3]     [Scr5]   Y      U      I      O      P      \
```

- Position 14: `@` — critical for ObjC (@interface, @property, @"string") and Swift (@State, @objc)
- Position 20: Cmd+Shift+3 (macOS full screenshot)
- Position 21: Cmd+Shift+5 (macOS screen recording)
- Position 27: `\` (Shift gives `|` via standard OS behavior)

### Row 2: Home Row + Inner/Thumb Keys

```
  ESC     A      S      D      F    G|Hyp  [Scr4]  [`] [#|Scr4]  [=] [^|Scr5] [Lock]  H|Hyp   J      K      L      ;      '
```

- Positions 29-32: A S D F — standard QWERTY, no mods (mods are below)
- Position 33: G — tap=G, hold=Hyper (Ctrl+Alt+Cmd+Shift)
- Position 34: Cmd+Shift+4 (macOS area screenshot)
- Position 35: `` ` `` (backtick/grave) — useful for Rust raw strings, Swift string interpolation
- Position 36: tap=`#`, Shift=Cmd+Shift+4 — preprocessor (ObjC), attributes (Rust #[derive])
- Position 37: `=`
- Position 38: tap=`^`, Shift=Cmd+Shift+5
- Position 39: Ctrl+Cmd+Q (macOS lock screen)
- Position 40: H — tap=H, hold=Hyper
- Positions 41-43: J K L — standard QWERTY
- Position 44: `;` — statement terminator (ObjC, Rust)
- Position 45: `'` — Rust lifetimes ('a, 'static), Swift/ObjC characters

### Row 3: Below Home — Home Row Mods

```
  LSh  Z|Ctrl X|Alt  C|Cmd  V|Sh  B|Hyp          [Spc|Cmd]  [$|Cmd]          N|Hyp  M|RSh  ,|Cmd  .|Alt  /|Ctrl  RSh
```

Modifiers activate on HOLD, characters on TAP:

| Position | Tap | Hold | Notes |
|----------|-----|------|-------|
| 46 | — | Left Shift | Dedicated Shift (redundant backup) |
| 47 | Z | Left Ctrl | |
| 48 | X | Left Alt | |
| 49 | C | Left Cmd | |
| 50 | V | Left Shift | |
| 51 | B | Hyper | |
| 52 | Space | Left Cmd | Left center thumb |
| 53 | $ | Right Cmd | Right center thumb |
| 54 | N | Hyper | |
| 55 | M | Right Shift | |
| 56 | , | Right Cmd | |
| 57 | . | Left Alt | |
| 58 | / | Left Ctrl | |
| 59 | — | Right Shift | Dedicated Shift (redundant backup) |

Hold-tap configuration: balanced flavor, 200ms tapping-term, 150ms quick-tap,
positional hold-trigger (only opposite-hand keys trigger hold), hold-trigger-on-release.

### Row 4: Bottom + Thumb Cluster

```
  [FN]  End   PgUp  PgDn  Home        [Ret|L1] [Tab] [Bksp]  [Ret] [Bksp] [Spc|L1]        Left  Down   Up    Right  [FN]
```

- Positions 60, 75: mo 2 (FN layer)
- Positions 61-64: End, PgUp, PgDn, Home
- Position 65: Return (tap) / Layer 1 (hold)
- Position 66: Tab
- Position 67: Backspace
- Position 68: Return
- Position 69: Backspace
- Position 70: Space (tap) / Layer 1 (hold)
- Positions 71-74: Arrow keys (Left, Down, Up, Right)


## Layer 1 — Keypad

Mirrored numpad layout accessible via hold on Return (pos 65) or Space (pos 70).

```
  =    *    /    =   NumLk  5   [_]                [mo3]   6   NumLk  =    /    *    -
  _    -    9    8    7     (   [_]                [_]     (    7     8    9    -    _
  _    +    6    5    4     )   [_]  [_]  [_]  [_] [_]    [_]  )     4    5    6    +    _
  _   Ent   3    2    1     %              [_]  [_]              %    1    2    3   Ent   _
 [FN]  :    .    0    ,         [Spc][Bksp][_]  [_][Bksp][Spc]       ,    0    .    :  [FN]
```


## Layer 2 — Function / Media

Accessible via mo 2 (positions 60/75).

```
  F1   F2   F3   F4   F5   F6  [tog1]          [mo3]  F7   F8    F9   F10  F11  F12
  _    _    _    _    _    _   [_]              [_]    _    _   VolD* VolU*  _    _
  _   BriD  Prev Play Next BriU [_]  [_]  [_]  [_] [_]  [_]   _   Mute  VolD  VolU  _    _
  _    _    _    _    _    _              [_]  [_]              _    _     _     _    _    _
  _    _    _    _    _         [_]  [_]  [_]  [_] [_]  [_]         _    _     _     _    _
```

*VolD/VolU with Shift+Alt modifier = fine-grained volume on macOS.


## Layer 3 — System / Bluetooth

Accessible via mo 3 (position 7).

- Row 0: BT profile select (0-4)
- Row 1: Bootloader mode (both halves)
- Row 2: BT clear, RGB controls
- Row 4: Backlight toggle, brightness


## Combos

| Combo | Left hand | Right hand | Action | Status |
|-------|-----------|------------|--------|--------|
| caps_word | F+J (32+41) | — | Caps Word | Active |
| caps_lock | V+M (50+55) | — | Caps Lock | Active |
| cut | Q+W (15+16) | O+P (25+26) | Cmd+X | Active |
| copy | W+E (16+17) | I+O (24+25) | Cmd+C | Active |
| paste | E+R (17+18) | U+I (23+24) | Cmd+V | Active |
| undo | W+R (16+18) | U+O (23+25) | Cmd+Z | Active |
| redo | Q+E (15+17) | I+P (24+26) | Cmd+Shift+Z | Active |
| select all | Q+R (15+18) | U+P (23+26) | Cmd+A | Active |

All combos use `timeout-ms = <40>` and `require-prior-idle-ms = <150>` to prevent misfires.
Row above home (QWER/UIOP) chosen over home row to avoid interference with home row mods.


## Macros (defined in macros.dtsi)

| Macro | Output | Status |
|-------|--------|--------|
| macro_quotes | `''` + cursor between | Defined, NOT bound |
| macro_dquotes | `""` + cursor between | Defined, NOT bound |
| macro_braces | `{}` + cursor between | Defined, NOT bound |
| macro_parens | `()` + cursor between | Defined, NOT bound |
| macro_brackets | `[]` + cursor between | Defined, NOT bound |
| macro_kinesis | Types "Kinesis" | Defined, NOT bound |


## ABC vs US International

The layout was originally designed for US International. It now runs on ABC.
ZMK sends HID keycodes — the OS input source interprets them.

| Key | US International | ABC | Impact |
|-----|-----------------|-----|--------|
| `` ` `` | Dead key | Direct | Better — backtick types immediately |
| `'` | Dead key | Direct | Better — quote types immediately |
| `"` | Dead key | Direct | Better — double quote types immediately |
| `~` | Dead key | Direct | Better — tilde types immediately |
| `^` | Dead key | Direct | Better — caret types immediately |

No changes needed for compatibility. ABC is strictly better for this layout.


---


# Proposed Upgrades

## Status

| # | Change | Priority | Status |
|---|--------|----------|--------|
| 1 | Timeless home row mods (move mods back to ASDF/JKL;) | Critical | Done |
| 2 | Fix and re-enable combos with require-prior-idle-ms | Critical | Done |
| 3 | Add Nav/Symbol layer (vim arrows + direct symbols) | High | Done |
| 4 | Add code macros (->, =>, ::, .., ??) | Medium | Done |
| 5 | Bind existing auto-pair macros | Medium | Pending |
| 6 | Reconsider right thumb $ tap | Low | Pending |


## Upgrade 1: Timeless Home Row Mods — Move Mods Back to ASDF/JKL; (CRITICAL)

### Problem
Home row mods were moved to the row below (ZXCVB / NM,./) to avoid misfires.
This works but has downsides:
- Fingers must curl down to activate modifiers — more movement than intended
- Common shortcuts like Cmd+C are awkward: C is itself the Cmd key, so copy
  requires using the opposite-hand Cmd (hold `,` then press C)
- The row below home loses its letters as pure taps during fast typing, since
  the hold-tap behavior adds latency to every keypress on that row
- 10 keys on the below-home row have dual behavior, creating a large "misfire
  surface" even though it's less prone than the home row

### Solution: urob's "Timeless" Home Row Mods
Based on https://github.com/urob/zmk-config#timeless-homerow-mods

The key insight: use `require-prior-idle-ms` on the hold-tap behaviors themselves
(not just combos). This makes the hold-tap resolve as TAP immediately when pressed
during a typing flow. The hold behavior only activates after a deliberate pause.

Combined with a larger `tapping-term-ms` (280ms vs current 200ms), the timing
becomes almost irrelevant — hence "timeless."

### How It Works (Three-Layer Defense Against Misfires)

1. **`require-prior-idle-ms = <150>`** — If any key was pressed in the last 150ms,
   the hold-tap immediately resolves as TAP. During typing, inter-key intervals
   are 50-100ms, so mods never accidentally activate mid-word.
   Formula: set to at least `10500 / your_relaxed_WPM`.

2. **Positional hold-trigger** — Same-hand keys always resolve as TAP. Only
   opposite-hand keypresses (and thumbs) can trigger the hold. This prevents
   "sd" from becoming Shift+D when rolling keys on the same hand.

3. **`hold-trigger-on-release`** — Delays the positional check until the key is
   released. This allows deliberately chording multiple modifiers on the same
   hand (e.g., Ctrl+Shift) while still preventing same-hand typing rolls from
   misfiring.

### New Modifier Arrangement

Moving mods from ZXCVB back to ASDF, preserving the existing modifier order
(pinky-to-index: Ctrl, Alt, Cmd, Shift):

```
Left home row:                    Right home row:
A = Ctrl   (hold)                 ; = Ctrl   (hold)
S = Alt    (hold)                 L = Alt    (hold)
D = Cmd    (hold)                 K = Cmd    (hold)
F = Shift  (hold)                 J = Shift  (hold)
G = Hyper  (hold) [unchanged]     H = Hyper  (hold) [unchanged]
```

This is the standard CAGS (Ctrl-Alt-Gui-Shift) order, mirrored on both hands.
Shift on the index finger is ideal — it's the most-used modifier and the index
finger is the fastest/most precise.

### What Happens to the Below-Home Row

ZXCVB and NM,./ become **pure letter keys** again (no hold-tap). This means:
- Faster key registration on that row (no hold-tap latency)
- `/` is just `/`, no more accidental Ctrl
- The row below home becomes a normal typing row

The dedicated Shift keys at positions 46/59 remain as backup.

### Implementation

```dts
// Replace existing hml/hmr behaviors with urob's timeless config:

hmr: home_row_mods_right {
    compatible = "zmk,behavior-hold-tap";
    label = "HOME_ROW_MODS_RIGHT";
    #binding-cells = <2>;
    bindings = <&kp>, <&kp>;
    tapping-term-ms = <280>;
    quick-tap-ms = <175>;
    require-prior-idle-ms = <150>;
    flavor = "balanced";
    hold-trigger-on-release;
    hold-trigger-key-positions = <
        0  1  2  3  4  5  6
        14 15 16 17 18 19 20
        28 29 30 31 32 33 34
        46 47 48 49 50 51
        60 61 62 63 64
        35 36 52 65 66 67
    >;
};

hml: home_row_mods_left {
    compatible = "zmk,behavior-hold-tap";
    label = "HOME_ROW_MODS_LEFT";
    #binding-cells = <2>;
    bindings = <&kp>, <&kp>;
    tapping-term-ms = <280>;
    quick-tap-ms = <175>;
    require-prior-idle-ms = <150>;
    flavor = "balanced";
    hold-trigger-on-release;
    hold-trigger-key-positions = <
        7  8  9 10 11 12 13
        21 22 23 24 25 26 27
        39 40 41 42 43 44 45
        54 55 56 57 58 59
        71 72 73 74 75
        37 38 53 68 69 70
    >;
};
```

### Default Layer Changes (Row 2 and Row 3)

```
Row 2 (Home row) — BEFORE:
  ESC   A     S     D     F    G|Hyp   ...   H|Hyp   J     K     L     ;     '

Row 2 (Home row) — AFTER:
  ESC  A|Ctrl S|Alt D|Cmd F|Sh G|Hyp   ...   H|Hyp  J|Sh  K|Cmd L|Alt ;|Ctrl  '

Row 3 (Below home) — BEFORE:
  LSh  Z|Ctrl X|Alt C|Cmd V|Sh B|Hyp   ...   N|Hyp  M|RSh ,|Cmd .|Alt /|Ctrl RSh

Row 3 (Below home) — AFTER:
  LSh    Z      X     C     V     B     ...     N      M     ,     .     /    RSh
```

### Impact on Other Features

- **Combos on QWER/UIOP row**: Unaffected (different row from mods)
- **Caps Word combo (F+J)**: Still works — F(Shift) + J(Shift) are now both
  hold-tap keys, but the combo fires on tap which happens before hold resolves
- **Nav layer vim arrows (HJKL)**: Layer bindings override hold-tap, so arrows
  work as direct keypresses on the nav layer
- **Hyper on G/H**: Unchanged
- **Copy/Paste shortcuts**: Now much easier — Cmd is on D (hold D + tap C = Cmd+C
  using the same hand, but positional enforcement means this resolves as "dc" tap.
  Instead, use opposite hand: hold K (right Cmd) + tap C = Cmd+C. Or use combos.

### Tuning Guide
- If mods feel too hard to activate: lower `require-prior-idle-ms` (try 120ms)
- If misfires occur during fast typing: raise `require-prior-idle-ms` (try 175ms)
- If same-hand mod+key is needed: the 280ms tapping term allows it with a
  deliberate hold, but cross-hand is always preferred
- `quick-tap-ms = <175>`: tapping a key twice quickly always produces two taps


## Upgrade 2: Fix Combo Misfires with require-prior-idle-ms (CRITICAL)

### Problem
Combos on the QWER/UIOP row were disabled because they misfired during fast
typing. For example, typing "we" quickly would trigger the copy combo (W+E).

### Solution
ZMK's `require-prior-idle-ms` parameter prevents combos from firing during fast
typing. It requires a pause of N milliseconds before the combo keys are pressed.
During a typing flow, keys are pressed in rapid succession (< 100ms apart), so
the combo won't trigger. When you deliberately want the combo, there's naturally
a brief pause before you press both keys.

### Implementation

```dts
combos {
    compatible = "zmk,combos";

    combo_caps_word {
        bindings = <&caps_word>;
        key-positions = <32 41>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    combo_caps_lock {
        bindings = <&kp CAPSLOCK>;
        key-positions = <50 55>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    // Row above home — left hand
    lh_combo_copy {
        bindings = <&kp LG(C)>;
        key-positions = <16 17>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
    rh_combo_copy {
        bindings = <&kp LG(C)>;
        key-positions = <24 25>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    lh_combo_paste {
        bindings = <&kp LG(V)>;
        key-positions = <17 18>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
    rh_combo_paste {
        bindings = <&kp LG(V)>;
        key-positions = <23 24>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    lh_combo_cut {
        bindings = <&kp LG(X)>;
        key-positions = <15 16>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
    rh_combo_cut {
        bindings = <&kp LG(X)>;
        key-positions = <25 26>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    lh_combo_select_all {
        bindings = <&kp LG(A)>;
        key-positions = <15 18>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
    rh_combo_select_all {
        bindings = <&kp LG(A)>;
        key-positions = <23 26>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    lh_combo_undo {
        bindings = <&kp LG(Z)>;
        key-positions = <16 18>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
    rh_combo_undo {
        bindings = <&kp LG(Z)>;
        key-positions = <23 25>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };

    lh_combo_redo {
        bindings = <&kp LS(LG(Z))>;
        key-positions = <15 17>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
    rh_combo_redo {
        bindings = <&kp LS(LG(Z))>;
        key-positions = <24 26>;
        timeout-ms = <40>;
        require-prior-idle-ms = <150>;
    };
};
```

### Tuning
- `timeout-ms = <40>`: Both combo keys must be pressed within 40ms of each other
  (tighter than default 50ms, reduces accidental triggers)
- `require-prior-idle-ms = <150>`: Combo only triggers if no key was pressed in
  the preceding 150ms. During typing flow, inter-key intervals are typically
  50-100ms, so combos won't fire. Start at 150ms and lower to 100ms if combos
  feel too hard to trigger.


## Upgrade 3: Nav/Symbol Layer (HIGH) — DONE

Replaces the keypad layer (Layer 1). Activated by holding Return (pos 65) or
Space (pos 70). Inspired by Sunaku's Glove80 symbol layer — bracket pairs
adjacent, most-used symbols on home row, logical groupings by category.

### Layout

```
LEFT HAND (symbols)                                          RIGHT HAND (navigation)
Row 0:  ~      `      [      ]      $      %   [trans]     [trans]  ---    ---    ---    ---    ---    ---
Row 1:  #      <      (      )      >      @   [trans]     [trans]  ---    ---    ---    ---    ---    ---
Row 2:  ---    _      {      }      !      ?   [trans] [t][t] [t][t] [trans]  Left  Down   Up   Right   +      =
Row 3:  ---    ->     =>     ::     ..     ??          [t][t]              Home  PgDn  PgUp   End   ---    ---
Row 4:  ---    &      |      ^      *           [trans][t][t] [t][t][trans]      ---    ---    ---    ---    ---
```

### Left Hand — Symbol Groupings

| Row | Keys | Logic |
|-----|------|-------|
| Row 0 | `~` `` ` `` `[` `]` `$` `%` | Utility: backtick/tilde + square brackets + money/math |
| Row 1 | `#` `<` `(` `)` `>` `@` | Brackets: angle brackets frame parens, `#` and `@` on edges |
| Row 2 | `_` `{` `}` `!` `?` | Home row: most-used symbols (underscore, braces, logic) |
| Row 3 | `->` `=>` `::` `..` `??` | Code macros: Swift/Rust/ObjC multi-char operators |
| Row 4 | `&` `|` `^` `*` | Bitwise/pointer operators |

### Right Hand — Vim Navigation

| Row | Keys | Logic |
|-----|------|-------|
| Row 2 | Left Down Up Right `+` `=` | Vim arrows on HJKL, operators on edges |
| Row 3 | Home PgDn PgUp End | Page navigation mirrors vim (J=down, below J=PgDn) |

All other right-hand keys are `&trans` (fall through to default layer).
All thumb/inner keys are `&trans` (Return, Tab, Backspace, Space still work).


## Upgrade 4: Code Macros for Swift/ObjC/Rust (MEDIUM) — DONE

Macros defined in `macros.dtsi` and bound on the nav/symbol layer (Row 3, left hand).

| Macro | Output | Layer Position | Primary Use |
|-------|--------|----------------|-------------|
| macro_thin_arrow | `->` | Z position (47) | Swift/Rust fn return types, ObjC pointer member |
| macro_fat_arrow | `=>` | X position (48) | Rust match arms |
| macro_double_colon | `::` | C position (49) | Rust path separator (std::io::Result) |
| macro_range | `..` | V position (50) | Rust ranges (0..10) |
| macro_nil_coalesce | `??` | B position (51) | Swift nil coalescing |

`||` and `&&` were not implemented — they're only 2 keypresses anyway and would
add complexity without significant benefit.


## Upgrade 5: Bind Existing Auto-Pair Macros (MEDIUM)

The following macros exist in macros.dtsi but are not bound to any key:
- `macro_quotes` — types `''` with cursor between
- `macro_dquotes` — types `""` with cursor between
- `macro_braces` — types `{}` with cursor between
- `macro_parens` — types `()` with cursor between
- `macro_brackets` — types `[]` with cursor between

### Binding Suggestions
On the nav/symbol layer, use Shift+bracket keys for auto-pair:
- Shift + `(` key = `()` auto-pair
- Shift + `[` key = `[]` auto-pair
- Shift + `{` key = `{}` auto-pair
- Shift + `'` key = `''` auto-pair
- Shift + `"` key = `""` auto-pair

Or bind as combos on the default layer using bracket key + adjacent key.


## Upgrade 6: Reconsider Right Thumb $ Tap (LOW)

Position 53 currently types `$` on tap (hold = Right Cmd). `$` is not commonly
used in Swift/ObjC/Rust (unlike shell or JS). Consider replacing with:
- `Delete` (forward delete) — complements Backspace
- Keep `$` if shell usage is frequent
- A layer toggle or momentary key for a different purpose


---


# Language-Specific Symbol Frequency Reference

## Swift
Most used: `()` `{}` `[]` `.` `->` `@` `?` `!` `_` `//` `""` `:` `=` `<>`
Common:    `??` `&&` `||` `!=` `==` `#` `$` (string interpolation `\()`)

## Objective-C
Most used: `@` `[]` `()` `{}` `*` `:` `;` `#` `_` `.` `-` `+` `//`
Common:    `->` `@""` `@[]` `@{}` `@()` `!=` `==` `&&` `||` `<>`

## Rust
Most used: `::` `()` `{}` `<>` `&` `->` `=>` `.` `_` `|` `!` `?` `//`
Common:    `..` `..=` `'` (lifetimes) `#[]` `""` `*` `&&` `||` `!=` `==`

## Cross-Language Priority (what should be easiest to type)
1. `_` (underscore) — all three languages, very frequent
2. `@` — critical for ObjC/Swift
3. `->` — all three languages
4. `&` — Rust references
5. `|` — Rust closures, shell, logical OR
6. `::` — Rust paths
7. `=>` — Rust match
8. `!` — Swift force unwrap, Rust macros
9. `?` — Swift optionals, Rust error propagation
10. `'` — Rust lifetimes (already on home row!)
