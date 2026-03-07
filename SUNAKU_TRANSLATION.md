# Sunaku Glove80 Keymap -> Kinesis Adv360 Pro Translation Plan

## Source Reference
- Repo: `../glove80-keymaps` (sunaku/glove80-keymaps)
- Website: https://sunaku.github.io/moergo-glove80-keyboard.html
- Version: v52 "Glorious Engrammer"

## Scope

Adopt sunaku's Miryoku-style layer architecture and home row mods approach,
translated for the Kinesis Advantage 360 Pro (76 keys) and then synced to
the Glove80 (80 keys).

**Adopting:**
- Miryoku-style dedicated layers (Cursor, Number, Function, Symbol, System)
- Per-finger home row mod timing (different hold times per finger)
- Thumb keys as layer-tap access points
- Home row mods available on same-hand side of all layers
- Thumb combos (caps word, sticky shift, hyper/meh)

**NOT adopting:**
- Multiple alpha layouts (only QWERTY)
- Bilateral enforcement layers (8 per-finger layers) -- consider later
- Gaming / Typing / Emoji / World / Unicode layers
- Mouse layer (Kinesis lacks HID pointing support)
- macOS-specific duplicate layers (we use `LG()` directly)
- Space/Shift/Thumb forgiveness features
- RGB per-key indicators
- Difficulty level system

---

## 1. Physical Key Mapping

### Glove80 (80 keys) vs Kinesis Adv360 (76 keys)

```
Glove80 (6 rows):                     Kinesis (5 rows):
Row 0: 5+5 = 10  (F-key row)         (no equivalent -- use for media/brightness)
Row 1: 6+6 = 12  (number row)        Row 0: 6+1+1+6 = 14  (number + inner col)
Row 2: 6+6 = 12  (QWERTY row)        Row 1: 6+1+1+6 = 14  (QWERTY + inner col)
Row 3: 6+6 = 12  (home row)          Row 2: 6+1+2+2+1+6 = 18  (home + middle cluster)
Row 4: 6+3+3+6 = 18  (below home)    Row 3: 6+1+1+6 = 14  (below home + center)
Row 5: 5+3+3+5 = 16  (thumb/bottom)  Row 4: 5+3+3+5 = 16  (thumb/bottom)
```

Key differences:
- Kinesis has NO F-key row (use a Function layer instead)
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

### Current Kinesis layers (5)
| # | Name | Access |
|---|------|--------|
| 0 | Default (QWERTY) | -- |
| 1 | Keypad | hold Return (65) or hold Space (70) |
| 2 | FN (media/F-keys) | mo 2 (60, 75) |
| 3 | Mod (BT/system) | mo 3 (7) |
| 4 | Nav/Symbol | hold Space (70) |

### Proposed layers (sunaku-inspired)
| # | Name | Thumb access | Sunaku equivalent |
|---|------|-------------|-------------------|
| 0 | Default (QWERTY) | -- | Base layer |
| 1 | Cursor | hold Space (65 left) | LAYER_Cursor (15) |
| 2 | Number | hold Tab (66 left) | LAYER_Number (16) |
| 3 | Function | hold Esc (67 left? or combo) | LAYER_Function (17) |
| 4 | Symbol | hold R/Backspace (70 right) | LAYER_Symbol (19) |
| 5 | System | hold Enter (68 right) | LAYER_System (21) |
| 6 | Mod (BT/boot) | combo or existing mo | LAYER_Magic (31) |

NOTE: The Kinesis Adv360 has a max of ~10 usable layers in practice.

### Thumb Cluster Redesign

Sunaku's thumb philosophy: every thumb key is a **layer-tap** (tap = key, hold = layer).

```
Sunaku Glove80 thumb mapping:
Left:  T4=Space/Cursor  T5=Tab/Number    T6=PgDn
       T1=Esc/Function  T2=Insert/Lower  T3=PgUp

Right: T4=R/Symbol      T5=Bksp/Mouse    T6=--
       T1=Enter/System  T2=Delete/Lower  T3=--
```

Proposed Kinesis thumb mapping (positions 65-70):
```
Left thumb cluster:           Right thumb cluster:
[65] Space / Cursor layer     [68] Enter
[66] Tab / Number layer       [69] Backspace
[67] Backspace                [70] Space / Symbol layer

Current center keys (52, 53) can hold Function/System access or be repurposed.
```

Alternative (closer to sunaku's intent):
```
Left thumb:                   Right thumb:
[65] Space / Cursor           [68] Enter / System
[66] Tab / Number             [69] Backspace
[67] Esc / Function           [70] Space / Symbol
```

This gives 4 layer-tap thumbs (Cursor, Number, Function, Symbol) plus System
on the right Enter, matching sunaku's 5 main layers. The Mod/BT layer stays
on a corner key or combo.

---

## 3. Per-Finger Home Row Mod Timing

### Current (urob-style, uniform timing)
```
All fingers: tapping-term-ms=280, quick-tap-ms=175, require-prior-idle-ms=150
```

### Sunaku's per-finger timing (DIFFICULTY_LEVEL 0)
```
Base resolution: 150ms
Pinky:  hold=270ms  streak-decay=150ms  repeat-decay=300ms
Ring:   hold=240ms  streak-decay=150ms  repeat-decay=300ms
Middle: hold=210ms  streak-decay=150ms  repeat-decay=300ms
Index:  hold=180ms  streak-decay=150ms  repeat-decay=300ms
```

### Proposed per-finger behaviors for Kinesis

Instead of one `hml`/`hmr`, create per-finger hold-tap behaviors:

```
hml_pinky / hmr_pinky:  tapping-term-ms=270  quick-tap-ms=300  require-prior-idle-ms=150
hml_ring  / hmr_ring:   tapping-term-ms=240  quick-tap-ms=300  require-prior-idle-ms=150
hml_mid   / hmr_mid:    tapping-term-ms=210  quick-tap-ms=300  require-prior-idle-ms=150
hml_index / hmr_index:  tapping-term-ms=180  quick-tap-ms=300  require-prior-idle-ms=150
```

Each with appropriate `hold-trigger-key-positions` for left/right hand.

### Home Row Assignment (QWERTY, macOS CAGS order)
```
Left:   A=Ctrl(pinky)  S=Alt(ring)  D=Cmd(middle)  F=Shift(index)
Right:  J=Shift(index) K=Cmd(middle) L=Alt(ring)   ;=Ctrl(pinky)
```

---

## 4. Layer Content Translation

### 4a. Cursor Layer (Sunaku LAYER_Cursor -> our Layer 1)

Access: hold Space (left thumb, position 65)

Sunaku's cursor layer design:
- Right hand: arrow keys on home row (LEFT, UP, DOWN, RIGHT)
- Right hand below: HOME, PG_UP, PG_DN, END
- Left hand: editing keys (RET, SPACE, TAB, BSPC on ASDF)
- Left hand: same-hand mods (home row mods still active)
- Left hand below: select_all, select_line, select_word, FIND
- Shortcuts: CUT, COPY, PASTE, UNDO, REDO

```
Kinesis Cursor layer (76 keys):
Row 0: ---  ESC   INS  S(TAB) DEL   ---  [---]       [---]  ---   ---   ---    ---   ---   ---
Row 1: ---  RET   SPC   TAB  BSPC  CUT  [---]       [---]  CUT  S(TAB) UNDO  REDO   TAB  ---
Row 2: ---  LSFT PINKY RING  MID   IDX  COPY [---][---] [---][---] COPY LEFT  DOWN   UP   RIGHT LSFT
Row 3: C(L) SelA  SelL  SelW  FIND PASTE       [---] [---]       PASTE HOME  PgUp  PgDn  END  C(L)
Row 4: ---  UNDO  REDO FndPv FndNx      [tog]  FIND FndPv FndNx C(H) [tog]       ---   ---   ---   ---  ---
```

Key: PINKY/RING/MID/IDX = same-hand home row mods (for chording with layer keys)

### 4b. Number Layer (Sunaku LAYER_Number -> our Layer 2)

Access: hold Tab (left thumb, position 66)

Sunaku's number layer:
- Right hand: numpad (789/456/123/0) on home-ish positions
- Right hand edges: math operators (-, +, /, *, =)
- Left hand: editing keys + same-hand mods
- Top right: hex digits A-E

```
Kinesis Number layer (76 keys):
Row 0: ---  ESC   INS  S(TAB) DEL   ---  [---]       [---]  |    #    $    ^    `    !
Row 1: ---  RET   SPC   TAB  BSPC    0   [---]       [---] S(G)   7    8    9    :    %
Row 2: ---  LSFT PINKY RING  MID   IDX    X   [---][---] [---][---]  K    4    5    6    -    +=
Row 3:  E  SelA  SelL  SelW  FIND    F           [---] [---]          J    1    2    3    /    *
Row 4: S(-) UNDO  REDO FndPv FndNx      [tog]  S(9) LBKT RBKT S(0) [tog]       ,    0    .   S(2)  ---
```

### 4c. Function Layer (Sunaku LAYER_Function -> our Layer 3)

Access: hold Esc or dedicated key

```
Kinesis Function layer (76 keys):
Row 0: ---  ESC   INS  S(TAB) DEL   ---  [---]       [---] MEDIA PLAY  PREV  NEXT  STOP EJECT
Row 1: ---  RET   SPC   TAB  BSPC  CALC [---]       [---]  CALC   F7    F8    F9   F10   F13
Row 2: ---  LSFT PINKY RING  MID   IDX   WWW  [---][---] [---][---] WWW   F4    F5    F6   F11   F14
Row 3: ---  SelA  SelL  SelW  FIND FILES       [---] [---]       FILES  F1    F2    F3   F12   F15
Row 4: ---  UNDO  REDO FndPv FndNx      [tog] PREV  C_PP  MUTE BriUp [tog]      BriUp BriDn VolUp VolDn ---
```

### 4d. Symbol Layer (Sunaku LAYER_Symbol -> our Layer 4)

Access: hold Space (right thumb, position 70)

This is the most important layer for programming. Sunaku's symbol layer
is very similar to our existing nav_symbol layer. Key differences:

Sunaku's symbol layer (right side has editing + same-hand mods):
```
Left side (symbols):              Right side (editing + mods):
Row 2: `  (  )  ;  ,             ---  ---  ---  ---  ---
Row 3: !  [  {  }  ]  ?          .   DEL  S(TAB) INS ESC
Row 4: #  ^  =  _  $  *          ,  BSPC  TAB  SPC  RET  ```
Row 5: ~  <  |  -  >  /  \  .    ;   "    '    `    \
Row 6: .. &  '  "  +   %  :  @   Sh  Cmd  Alt  Ctrl
```

Our current nav_symbol layer is already very close to this. The main
differences are:
1. Sunaku has `?` (`S(FSLH)`) where we have `@`
2. Sunaku has `\` and `.` as extra keys on Row 5 middle
3. Right side: sunaku has editing keys (DEL, BSPC, TAB, SPC, RET)
   and same-hand mods on bottom row -- we have similar but different positions

**Decision**: Keep our existing nav_symbol layer mostly as-is since it was
already inspired by sunaku's design. Consider adopting the right-side
editing keys and mods pattern if beneficial.

### 4e. System Layer (Sunaku LAYER_System -> our Layer 5)

Access: hold Enter (right thumb, position 68)

Content: BT profiles, bootloader, RGB, power management.
Our current "mod" layer (layer 3) already covers this.

---

## 5. Combos Translation

### Sunaku's thumb combos (translate to Kinesis thumb positions)

Sunaku uses thumb key combinations. Our thumb positions:
- Left: 65 (Space/Cursor), 66 (Tab/Number), 67 (Backspace)
- Right: 68 (Enter/System), 69 (Backspace), 70 (Space/Symbol)

| Sunaku combo | Keys | Proposed Kinesis | Keys |
|-------------|------|-----------------|------|
| caps_word | LT4+LT5 | Space+Tab (left) | 65+66 |
| caps_word | RT4+RT5 | Enter+Bksp (right) | 68+69 |
| caps_lock | LT2+LT6 | (keep existing F+J or V+M) | 32+41 or 50+55 |
| sticky_shift_left | LT1+LT5 | Bksp+Tab (left) | 67+66 |
| sticky_shift_right | RT1+RT5 | Enter+Bksp (right) | 68+69 |
| hyper (GACS) | RT1+RT4 | (keep as home row hold) | -- |
| base_layer_reset | LT1+LT2+LT3 | triple thumb combo | 65+66+67 |

### Keep existing QWER/UIOP combos
The cut/copy/paste/undo/redo/select-all combos on the QWER row stay as-is.

---

## 6. Implementation TODO

| # | Task | Priority | Depends on | Status |
|---|------|----------|-----------|--------|
| 1 | Design final thumb cluster layout | Critical | -- | Pending |
| 2 | Create per-finger hold-tap behaviors | Critical | 1 | Pending |
| 3 | Implement Cursor layer | High | 1 | Pending |
| 4 | Implement Number layer | High | 1 | Pending |
| 5 | Implement Function layer | High | 1 | Pending |
| 6 | Update Symbol layer (refine from current nav_symbol) | Medium | 1 | Pending |
| 7 | Implement System layer (merge with current mod layer) | Medium | 1 | Pending |
| 8 | Add thumb combos (caps_word, sticky_shift, etc.) | Medium | 1 | Pending |
| 9 | Sync all changes to Glove80 config | High | 3-8 | Pending |
| 10 | Build translation script (Kinesis -> Glove80) | Low | 9 | Pending |

### Task 10: Translation Script

After completing the manual translation (tasks 1-9), we'll have learned the
exact mapping rules between the two keyboards. The script should:

1. Parse a Kinesis `.keymap` file
2. Map 76-key positions to 80-key positions
3. Handle row differences (Kinesis 5 rows -> Glove80 6 rows)
4. Handle middle/inner column key mapping
5. Output a Glove80-compatible `.keymap` file
6. Handle behaviors, macros, combos (position remapping)

Language: Python or shell script, stored in this repo.

---

## 7. Key Position Mapping Table (Kinesis -> Glove80)

For the translation script, this is the definitive position map:

```
Kinesis pos -> Glove80 pos (by physical position)

Glove80 Row 0 (F-keys, 10 keys): No Kinesis equivalent
  G[0-4] = extra row (media/brightness)
  G[5-9] = extra row

Kinesis Row 0 (14) -> Glove80 Row 1 (12) + extras:
  K[0]  -> G[10]    K[1]  -> G[11]    K[2]  -> G[12]
  K[3]  -> G[13]    K[4]  -> G[14]    K[5]  -> G[15]
  K[6]  -> (no equiv, inner column -- place on Glove80 Row 4 middle or drop)
  K[7]  -> (no equiv, inner column)
  K[8]  -> G[16]    K[9]  -> G[17]    K[10] -> G[18]
  K[11] -> G[19]    K[12] -> G[20]    K[13] -> G[21]

Kinesis Row 1 (14) -> Glove80 Row 2 (12) + extras:
  K[14] -> G[22]    K[15] -> G[23]    K[16] -> G[24]
  K[17] -> G[25]    K[18] -> G[26]    K[19] -> G[27]
  K[20] -> (inner column)
  K[21] -> (inner column)
  K[22] -> G[28]    K[23] -> G[29]    K[24] -> G[30]
  K[25] -> G[31]    K[26] -> G[32]    K[27] -> G[33]

Kinesis Row 2 (18) -> Glove80 Row 3 (12) + Row 4 middle (6):
  K[28] -> G[34]    K[29] -> G[35]    K[30] -> G[36]
  K[31] -> G[37]    K[32] -> G[38]    K[33] -> G[39]
  K[34] -> (inner column)
  K[35] -> G[52]    K[36] -> G[53]    (center-left)
  K[37] -> G[56]    K[38] -> G[57]    (center-right)
  K[39] -> (inner column)
  K[40] -> G[40]    K[41] -> G[41]    K[42] -> G[42]
  K[43] -> G[43]    K[44] -> G[44]    K[45] -> G[45]

Kinesis Row 3 (14) -> Glove80 Row 4 outer (12) + middle (2):
  K[46] -> G[46]    K[47] -> G[47]    K[48] -> G[48]
  K[49] -> G[49]    K[50] -> G[50]    K[51] -> G[51]
  K[52] -> G[54]    (center-left)
  K[53] -> G[55]    (center-right)
  K[54] -> G[58]    K[55] -> G[59]    K[56] -> G[60]
  K[57] -> G[61]    K[58] -> G[62]    K[59] -> G[63]

Kinesis Row 4 (16) -> Glove80 Row 5 (16):
  K[60] -> G[64]    K[61] -> G[65]    K[62] -> G[66]
  K[63] -> G[67]    K[64] -> G[68]
  K[65] -> G[69]    K[66] -> G[70]    K[67] -> G[71]
  K[68] -> G[72]    K[69] -> G[73]    K[70] -> G[74]
  K[71] -> G[75]    K[72] -> G[76]    K[73] -> G[77]
  K[74] -> G[78]    K[75] -> G[79]
```

Inner column keys (K[6], K[7], K[20], K[21], K[34], K[39]):
- These exist on the Kinesis but NOT on the Glove80 rows 1-3
- K[34] and K[39] map loosely to Glove80 Row 4 middle area
- K[6], K[7], K[20], K[21] have no direct Glove80 equivalent
- For Kinesis->Glove80 sync: these keys are dropped or placed in Glove80's
  extra F-key row (G[0-9])

---

## 8. Decision Log

Decisions to make before implementation (discuss with user):

1. **Thumb cluster layout**: Which thumb gets which layer-tap?
2. **Keep keypad layer?** Or replace with Number layer entirely?
3. **Per-finger timing**: Adopt sunaku's exact values or tune our own?
4. **Bilateral enforcement**: Skip for now, add later? (adds 8 layers)
5. **Keep current nav_symbol or replace with sunaku-style Symbol?**
6. **Lower layer**: Add a dedicated Lower/utility layer for toggles?
