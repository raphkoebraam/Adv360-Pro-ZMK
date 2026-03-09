#!/usr/bin/env python3
"""
Generate a complete Glove80 keymap from the Kinesis Adv360 Pro sunaku config.

Reads the Kinesis keymap (config/adv360.keymap), layers.dtsi, and macros.dtsi,
remaps key positions from 76→80, adjusts position-dependent references,
and outputs a buildable glove80.keymap file.

Usage:
  ./tools/kinesis2glove80.py > ../glove80-zmk-config/config/glove80.keymap
  ./tools/kinesis2glove80.py --dry-run   # preview without writing
"""

import re
import sys
import os

# ===========================================================================
# Position mapping: Kinesis (76 keys) → Glove80 (80 keys)
# ===========================================================================

KINESIS_TO_GLOVE80 = {
    # Row 0 (numbers) → Glove80 Row 1
    0: 10, 1: 11, 2: 12, 3: 13, 4: 14, 5: 15,
    6: None, 7: None,  # inner columns (no Glove80 equivalent)
    8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21,
    # Row 1 (QWERTY) → Glove80 Row 2
    14: 22, 15: 23, 16: 24, 17: 25, 18: 26, 19: 27,
    20: None, 21: None,  # inner columns
    22: 28, 23: 29, 24: 30, 25: 31, 26: 32, 27: 33,
    # Row 2 (home) → Glove80 Row 3 + Row 4 center
    28: 34, 29: 35, 30: 36, 31: 37, 32: 38, 33: 39,
    34: None,  # inner column left
    35: 52, 36: 53,  # center → Glove80 row 4 middle
    37: 56, 38: 57,  # center → Glove80 row 4 middle
    39: None,  # inner column right
    40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 45,
    # Row 3 (below home) → Glove80 Row 4
    46: 46, 47: 47, 48: 48, 49: 49, 50: 50, 51: 51,
    52: 54, 53: 55,  # center → Glove80 row 4 middle
    54: 58, 55: 59, 56: 60, 57: 61, 58: 62, 59: 63,
    # Row 4 (thumb/bottom) → Glove80 Row 5
    60: 64, 61: 65, 62: 66, 63: 67, 64: 68,
    65: 69, 66: 70, 67: 71,
    68: 72, 69: 73, 70: 74,
    71: 75, 72: 76, 73: 77, 74: 78, 75: 79,
}

GLOVE80_TO_KINESIS = {}
for k, v in KINESIS_TO_GLOVE80.items():
    if v is not None:
        GLOVE80_TO_KINESIS[v] = k

# Glove80 positions with no Kinesis equivalent (F-key row)
GLOVE80_FKEY_ROW = list(range(10))  # positions 0-9

# ===========================================================================
# Glove80 key position groups (for hold-trigger-key-positions)
# Mapped from Kinesis equivalents
# ===========================================================================

GLOVE80_LEFT_HAND_KEYS = sorted([
    KINESIS_TO_GLOVE80[k] for k in [
        0, 1, 2, 3, 4, 5, 6,
        14, 15, 16, 17, 18, 19, 20,
        28, 29, 30, 31, 32, 33, 34,
        46, 47, 48, 49, 50, 51,
        60, 61, 62, 63, 64,
    ] if KINESIS_TO_GLOVE80[k] is not None
] + GLOVE80_FKEY_ROW[:5])  # add F-key row left (0-4)

GLOVE80_RIGHT_HAND_KEYS = sorted([
    KINESIS_TO_GLOVE80[k] for k in [
        7, 8, 9, 10, 11, 12, 13,
        21, 22, 23, 24, 25, 26, 27,
        39, 40, 41, 42, 43, 44, 45,
        54, 55, 56, 57, 58, 59,
        71, 72, 73, 74, 75,
    ] if KINESIS_TO_GLOVE80[k] is not None
] + GLOVE80_FKEY_ROW[5:])  # add F-key row right (5-9)

GLOVE80_THUMB_KEYS = sorted([
    KINESIS_TO_GLOVE80[k] for k in [
        35, 36, 37, 38,
        52, 53,
        65, 66, 67, 68, 69, 70,
    ] if KINESIS_TO_GLOVE80[k] is not None
])

# Glove80 thumb positions (mapped from Kinesis POS_* defines)
GLOVE80_THUMB_POS = {
    'POS_LH_T1': KINESIS_TO_GLOVE80[52],  # 54
    'POS_LH_T2': KINESIS_TO_GLOVE80[53],  # 55
    'POS_LH_T4': KINESIS_TO_GLOVE80[65],  # 69
    'POS_LH_T5': KINESIS_TO_GLOVE80[66],  # 70
    'POS_LH_T6': KINESIS_TO_GLOVE80[67],  # 71
    'POS_RH_T1': KINESIS_TO_GLOVE80[68],  # 72
    'POS_RH_T4': KINESIS_TO_GLOVE80[70],  # 74
    'POS_RH_T5': KINESIS_TO_GLOVE80[69],  # 73
}

# ===========================================================================
# Glove80 row structure for formatting layer bindings
# ===========================================================================

GLOVE80_ROW_SIZES = [5, 6, 6, 6, 12, 6, 8, 8, 6]
# Row 0: 5+5=10 (F-key, split left/right)
# Row 1: 6+6=12
# Row 2: 6+6=12
# Row 3: 6+6=12
# Row 4: 6+3+3+6=18
# Row 5: 5+3+3+5=16

GLOVE80_ROW_RANGES = [
    (0, 5),     # F-key left
    (5, 10),    # F-key right
    (10, 16),   # Row 1 left
    (16, 22),   # Row 1 right
    (22, 28),   # Row 2 left
    (28, 34),   # Row 2 right
    (34, 40),   # Row 3 left
    (40, 46),   # Row 3 right
    (46, 58),   # Row 4 (left 6 + center 3+3 + right 6) - displayed as single row
    (58, 64),   # Row 4 right
    (64, 72),   # Row 5 left (5 + 3 thumb)
    (72, 80),   # Row 5 right (3 thumb + 5)
]

# Pair rows for output (left + right per line)
GLOVE80_OUTPUT_ROWS = [
    (0, 10),    # F-key row: 10 keys
    (10, 22),   # Row 1: 12 keys
    (22, 34),   # Row 2: 12 keys
    (34, 46),   # Row 3: 12 keys
    (46, 64),   # Row 4: 18 keys
    (64, 80),   # Row 5: 16 keys
]


def remap_bindings(kinesis_bindings: list[str], fill: str = "&none") -> list[str]:
    """Convert 76 Kinesis bindings to 80 Glove80 bindings."""
    glove80 = [fill] * 80

    for k_pos, binding in enumerate(kinesis_bindings):
        g_pos = KINESIS_TO_GLOVE80.get(k_pos)
        if g_pos is not None:
            glove80[g_pos] = binding

    return glove80


def parse_kinesis_bindings(bindings_text: str) -> list[str]:
    """Parse binding entries from a bindings = < ... > block."""
    bindings = []
    pattern = re.compile(r'&\S+(?:\s+(?!&)[^\s>]+)*')
    for match in pattern.finditer(bindings_text):
        bindings.append(match.group().strip())
    return bindings


def format_layer(name: str, bindings: list[str], indent: str = "        ") -> str:
    """Format a layer block with Glove80 row structure."""
    rows = []
    for start, end in GLOVE80_OUTPUT_ROWS:
        row_bindings = bindings[start:end]
        rows.append("  ".join(row_bindings))

    body = "\n".join(rows)
    return f"""{indent}{name} {{
{indent}    bindings = <
{body}
{indent}    >;
{indent}}};"""


def remap_position_list(positions: list[int]) -> list[int]:
    """Remap a list of Kinesis key positions to Glove80 positions."""
    result = []
    for pos in positions:
        g_pos = KINESIS_TO_GLOVE80.get(pos)
        if g_pos is not None:
            result.append(g_pos)
    return sorted(result)


def extract_layers_from_keymap(content: str) -> list[tuple[str, list[str]]]:
    """Extract layer names and their bindings from the keymap section."""
    layers = []
    # Find the keymap block
    keymap_match = re.search(r'keymap\s*\{[^}]*compatible\s*=\s*"zmk,keymap"', content)
    if not keymap_match:
        print("ERROR: Could not find keymap block", file=sys.stderr)
        return layers

    # From keymap start, find all layer blocks with bindings
    keymap_start = keymap_match.start()
    # Find matching closing brace for keymap
    remaining = content[keymap_start:]

    # Find each layer: name { bindings = < ... >; };
    # Also handle layers without bindings (display-name only, like kinesis extras)
    layer_pat = re.compile(
        r'(\w+)\s*\{\s*(?:display-name\s*=\s*"[^"]*"\s*;\s*)?bindings\s*=\s*<(.*?)>\s*;',
        re.DOTALL
    )
    for match in layer_pat.finditer(remaining):
        name = match.group(1)
        if name in ('keymap', 'behaviors', 'combos', 'macros'):
            continue
        bindings_text = match.group(2)
        bindings = parse_kinesis_bindings(bindings_text)
        if len(bindings) >= 10:  # filter out non-layer blocks
            layers.append((name, bindings))

    return layers


def generate_layers_dtsi() -> str:
    """Generate a Glove80-adapted layers.dtsi content."""
    left_keys = " ".join(str(k) for k in GLOVE80_LEFT_HAND_KEYS)
    right_keys = " ".join(str(k) for k in GLOVE80_RIGHT_HAND_KEYS)
    thumb_keys = " ".join(str(k) for k in GLOVE80_THUMB_KEYS)

    return """// Layer defines for sunaku-style Miryoku layout
// Auto-generated for Glove80 from Kinesis Adv360 Pro config
// Source: tools/kinesis2glove80.py

// Operating system
#define OPERATING_SYSTEM 'M' // macOS

// macOS key abstractions
#define _C      LG
#define _A_TAB  LGUI
#define _G_TAB  LALT
#define _REDO   LG(LS(Z))
#define _POWER  K_POWER
#define _WORD   LA
#define _HOME   LG(LEFT)
#define _END    LG(RIGHT)
#define _EMOJI  LG(LC(SPACE))
#define _LOCK   _C(LC(Q))
#define _UNDO   _C(Z)
#define _CUT    _C(X)
#define _COPY   _C(C)
#define _PASTE  _C(V)
#define _FIND       _C(F)
#define _FIND_NEXT  _C(G)
#define _FIND_PREV  _C(LS(G))
#define _FILES      LS(LA(M))
#define _SLEEP      C_SLEEP

// Select word/line delay
#define SELECT_WORD_DELAY 1

// Select all is just Ctrl+A (not a macro)
#define select_all kp _C(A)

// Layer ordering
#define LAYER_QWERTY      0
#define LAYER_Cursor      1
#define LAYER_Keypad      2
#define LAYER_Mod         3
#define LAYER_Symbol      4
#define LAYER_Function    5
#define LAYER_System      6
#define LAYER_Lower       7
//
// Bilateral enforcement layers:
#define LAYER_LeftPinky    8
#define LAYER_LeftRingy    9
#define LAYER_LeftMiddy   10
#define LAYER_LeftIndex   11
#define LAYER_RightIndex  12
#define LAYER_RightMiddy  13
#define LAYER_RightRingy  14
#define LAYER_RightPinky  15
//
#define LAYER_SunakuNumber 16
//
// Mouse and utility layers (after bilateral):
#define LAYER_Mouse       17
#define LAYER_Factory     21

// Finger mod assignments (macOS: CAGS)
#define LEFT_PINKY_MOD  LCTL
#define LEFT_RINGY_MOD  LALT
#define LEFT_MIDDY_MOD  LGUI
#define LEFT_INDEX_MOD  LSFT
#define RIGHT_INDEX_MOD LSFT
#define RIGHT_MIDDY_MOD LGUI
#define RIGHT_RINGY_MOD LALT
#define RIGHT_PINKY_MOD LCTL

// Home row key codes (QWERTY)
#define LEFT_PINKY_KEY  A
#define LEFT_RINGY_KEY  S
#define LEFT_MIDDY_KEY  D
#define LEFT_INDEX_KEY  F
#define RIGHT_INDEX_KEY J
#define RIGHT_MIDDY_KEY K
#define RIGHT_RINGY_KEY L
#define RIGHT_PINKY_KEY SEMI

// Mod row key codes (below-home row)
#define LEFT_PINKY_TAP_KEY  Z
#define LEFT_RINGY_TAP_KEY  X
#define LEFT_MIDDY_TAP_KEY  C
#define LEFT_INDEX_TAP_KEY  V
#define RIGHT_INDEX_TAP_KEY M
#define RIGHT_MIDDY_TAP_KEY COMMA
#define RIGHT_RINGY_TAP_KEY DOT
#define RIGHT_PINKY_TAP_KEY FSLH

//
// Glove80 key positions (80 keys)
//
// Row 0: [ 0][ 1][ 2][ 3][ 4]                                        [ 5][ 6][ 7][ 8][ 9]
// Row 1: [10][11][12][13][14][15]                                [16][17][18][19][20][21]
// Row 2: [22][23][24][25][26][27]                                [28][29][30][31][32][33]
// Row 3: [34][35][36][37][38][39]                                [40][41][42][43][44][45]
// Row 4: [46][47][48][49][50][51]  [52][53][54]  [55][56][57]  [58][59][60][61][62][63]
// Row 5: [64][65][66][67][68]      [69][70][71]  [72][73][74]      [75][76][77][78][79]
//
#define                                                \\
     LEFT_HAND_KEYS                                    \\
      0  1  2  3  4                                    \\
     10 11 12 13 14 15                                 \\
     22 23 24 25 26 27                                 \\
     34 35 36 37 38 39                                 \\
     46 47 48 49 50 51                                 \\
     64 65 66 67 68
#define                                                \\
                                     RIGHT_HAND_KEYS   \\
                                       5  6  7  8  9   \\
                                      16 17 18 19 20 21 \\
                                      28 29 30 31 32 33 \\
                                      40 41 42 43 44 45 \\
                                      58 59 60 61 62 63 \\
                                         75 76 77 78 79
#define                                                \\
     THUMB_KEYS                                        \\
     52 53 54 55 56 57                                 \\
     69 70 71 72 73 74

// Thumb key positions (for combos)
#define POS_LH_T1 {POS_LH_T1}
#define POS_LH_T2 {POS_LH_T2}
#define POS_LH_T4 {POS_LH_T4}
#define POS_LH_T5 {POS_LH_T5}
#define POS_LH_T6 {POS_LH_T6}
#define POS_RH_T1 {POS_RH_T1}
#define POS_RH_T4 {POS_RH_T4}
#define POS_RH_T5 {POS_RH_T5}

// Per-finger timing
#define PINKY_HOLDING_TIME 270
#define RINGY_HOLDING_TIME 240
#define MIDDY_HOLDING_TIME 210
#define INDEX_HOLDING_TIME 180
#define HOMEY_STREAK_DECAY 150
#define HOMEY_REPEAT_DECAY 300
#define HOMEY_HOLDING_TYPE "tap-preferred"

// Thumb cluster timing
#define THUMB_HOLDING_TIME 200
#define THUMB_REPEAT_DECAY 300
#define THUMB_HOLDING_TYPE "balanced"

// Combo timing
#define COMBO_FIRING_DECAY 50

// Sticky key timing
#define STICKY_HOLDING_TIME 200
#define STICKY_1SHOT_DECAY  500

// Bilateral enforcement (uncomment to enable)
//#define ENFORCE_BILATERAL

// Base layer HRM macros
#ifdef ENFORCE_BILATERAL
  #define HRM_LEFT_PINKY(key)  left_pinky_bilateral LEFT_PINKY_MOD key
  #define HRM_LEFT_RINGY(key)  left_ringy_bilateral LEFT_RINGY_MOD key
  #define HRM_LEFT_MIDDY(key)  left_middy_bilateral LEFT_MIDDY_MOD key
  #define HRM_LEFT_INDEX(key)  left_index_bilateral LEFT_INDEX_MOD key
  #define HRM_RIGHT_INDEX(key) right_index_bilateral RIGHT_INDEX_MOD key
  #define HRM_RIGHT_MIDDY(key) right_middy_bilateral RIGHT_MIDDY_MOD key
  #define HRM_RIGHT_RINGY(key) right_ringy_bilateral RIGHT_RINGY_MOD key
  #define HRM_RIGHT_PINKY(key) right_pinky_bilateral RIGHT_PINKY_MOD key
#else
  #define HRM_LEFT_PINKY(key)  left_pinky LEFT_PINKY_MOD key
  #define HRM_LEFT_RINGY(key)  left_ringy LEFT_RINGY_MOD key
  #define HRM_LEFT_MIDDY(key)  left_middy LEFT_MIDDY_MOD key
  #define HRM_LEFT_INDEX(key)  left_index LEFT_INDEX_MOD key
  #define HRM_RIGHT_INDEX(key) right_index RIGHT_INDEX_MOD key
  #define HRM_RIGHT_MIDDY(key) right_middy RIGHT_MIDDY_MOD key
  #define HRM_RIGHT_RINGY(key) right_ringy RIGHT_RINGY_MOD key
  #define HRM_RIGHT_PINKY(key) right_pinky RIGHT_PINKY_MOD key
#endif
""".format(**{k: v for k, v in GLOVE80_THUMB_POS.items()})


def read_kinesis_file(filename: str) -> str:
    """Read a file from the Kinesis config directory."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base, "config", filename)
    with open(filepath) as f:
        return f.read()


def generate_glove80_keymap() -> str:
    """Generate the complete Glove80 keymap file."""
    kinesis_keymap = read_kinesis_file("adv360.keymap")
    kinesis_macros = read_kinesis_file("macros.dtsi")

    # Extract layers from kinesis keymap
    layers = extract_layers_from_keymap(kinesis_keymap)

    # Classify layers to skip
    kinesis_only_layers = {
        'kinesis_default_layer', 'kinesis_keypad', 'kinesis_fn', 'kinesis_mod',
        'kinesis_extra1', 'kinesis_extra2', 'kinesis_extra3', 'kinesis_extra4',
        'mod',  # Kinesis-specific mod layer — replaced by Glove80 magic_layer
    }

    # Define the correct layer order to match defines in layers.dtsi
    # This ensures layer indices match the #define values
    layer_order = [
        'default_layer',      # 0 = LAYER_QWERTY
        'layer_Cursor',       # 1
        'layer_Keypad',       # 2
        '__magic__',          # 3 = LAYER_Mod (Glove80 magic layer)
        'layer_Symbol',       # 4
        'layer_Function',     # 5
        'layer_System',       # 6
        'layer_Lower',        # 7
        'layer_LeftPinky',    # 8
        'layer_LeftRingy',    # 9
        'layer_LeftMiddy',    # 10
        'layer_LeftIndex',    # 11
        'layer_RightIndex',   # 12
        'layer_RightMiddy',   # 13
        'layer_RightRingy',   # 14
        'layer_RightPinky',   # 15
        'layer_SunakuNumber', # 16
        'mouse',              # 17
        'mouse_slow',         # 18
        'mouse_fast',         # 19
        'mouse_warp',         # 20
        '__factory__',        # 21 = LAYER_Factory
    ]

    # Build a dict of converted layers
    converted_layers = {}
    for name, bindings in layers:
        if name in kinesis_only_layers:
            continue

        key_count = len(bindings)
        # Determine fill for remapping
        if name in ('mouse_slow', 'mouse_fast', 'mouse_warp'):
            fill = "&trans"
        elif all(b == "&trans" for b in bindings):
            fill = "&trans"
        else:
            fill = "&none"

        if key_count == 76:
            glove80_bindings = remap_bindings(bindings, fill=fill)
        elif key_count == 80:
            glove80_bindings = bindings
        else:
            print(f"WARNING: layer {name} has {key_count} keys (expected 76), "
                  f"attempting remap anyway", file=sys.stderr)
            glove80_bindings = remap_bindings(bindings, fill=fill)

        # For default layer, add F-key row content (media controls)
        if name == 'default_layer':
            glove80_bindings[0] = "&kp C_BRIGHTNESS_DEC"
            glove80_bindings[1] = "&kp C_BRIGHTNESS_INC"
            glove80_bindings[2] = "&kp C_PREVIOUS"
            glove80_bindings[3] = "&kp C_PLAY_PAUSE"
            glove80_bindings[4] = "&kp C_NEXT"
            glove80_bindings[5] = "&kp C_MUTE"
            glove80_bindings[6] = "&kp C_VOLUME_DOWN"
            glove80_bindings[7] = "&kp C_VOLUME_UP"
            glove80_bindings[8] = "&kp LG(LS(N4))"
            glove80_bindings[9] = "&kp LG(LS(N5))"

        converted_layers[name] = format_layer(name, glove80_bindings)

    # Glove80 magic layer (replaces Kinesis mod layer)
    magic_layer = """        magic_layer {
            bindings = <
&bt BT_CLR   &none            &none            &none            &none                                                                                     &none  &none  &none  &none  &bt BT_CLR_ALL
&none        &none            &none            &none            &none            &none                                                             &none  &none  &none  &none  &none  &none
&none        &rgb_ug RGB_SPI  &rgb_ug RGB_SAI  &rgb_ug RGB_HUI  &rgb_ug RGB_BRI  &rgb_ug RGB_TOG                                                   &none  &none  &none  &none  &none  &none
&bootloader  &rgb_ug RGB_SPD  &rgb_ug RGB_SAD  &rgb_ug RGB_HUD  &rgb_ug RGB_BRD  &rgb_ug RGB_EFF                                                   &none  &none  &none  &none  &none  &bootloader
&sys_reset   &none            &none            &none            &none            &none            &bt_2  &bt_3  &none         &none  &none  &none  &none  &none  &none  &none  &none  &sys_reset
&none        &none            &none            &none            &none                             &bt_0  &bt_1  &out OUT_USB  &none  &none  &none         &none  &none  &none  &none  &to LAYER_Factory
            >;
        };"""

    # Glove80 factory test layer
    factory_test = """        factory_test_layer {
            bindings = <
&kp N0  &kp N6  &kp N2  &kp N8  &kp N4                                                                  &kp N4  &kp N8  &kp N2  &kp N6  &kp N0
&kp N1  &kp N7  &kp N3  &kp N9  &kp N5  &kp N0                                                  &kp N0  &kp N5  &kp N9  &kp N3  &kp N7  &kp N1
&kp N2  &kp N8  &kp N4  &kp N0  &kp N6  &kp N1                                                  &kp N1  &kp N6  &kp N0  &kp N4  &kp N8  &kp N2
&kp N3  &kp N9  &kp N5  &kp N1  &kp N7  &kp N2                                                  &kp N2  &kp N7  &kp N1  &kp N5  &kp N9  &kp N3
&kp N4  &kp N0  &kp N6  &kp N2  &kp N8  &kp N3  &kp N4  &kp N5  &kp N6  &kp N6  &kp N5  &kp N4  &kp N3  &kp N8  &kp N2  &kp N6  &kp N0  &kp N4
&kp N5  &kp N1  &kp N7  &kp N3  &kp N9          &kp N7  &kp N8  &kp N9  &kp N9  &kp N8  &kp N7          &kp N9  &kp N3  &kp N7  &kp N1  &kp N5
            >;
        };"""

    # Build layer blocks in the correct order (matching defines)
    layer_blocks = []
    for slot in layer_order:
        if slot == '__magic__':
            layer_blocks.append(magic_layer)
        elif slot == '__factory__':
            layer_blocks.append(factory_test)
        elif slot in converted_layers:
            layer_blocks.append(converted_layers[slot])
        else:
            print(f"WARNING: layer {slot} not found in Kinesis keymap", file=sys.stderr)

    layers_output = "\n\n".join(layer_blocks)

    # Read macros.dtsi content and strip Kinesis-only macros
    macros_content = kinesis_macros
    # Remove macro_kinesis (types "Kinesis")
    macros_content = re.sub(
        r'  macro_kinesis:.*?;\n  \};\n',
        '', macros_content, flags=re.DOTALL
    )

    # Post-process layers: replace Kinesis-specific bindings
    layers_output = layers_output.replace("&macro_ver", "&none")
    layers_output = layers_output.replace("&bl BL_TOG", "&none")
    layers_output = layers_output.replace("&bl BL_INC", "&none")
    layers_output = layers_output.replace("&bl BL_DEC", "&none")
    # Replace Kinesis RGB_MEFS_CMD with plain RGB_TOG if present
    layers_output = re.sub(r'&rgb_ug RGB_MEFS_CMD \d+', '&none', layers_output)
    # Use Glove80 magic behavior for mod layer access on corner keys
    layers_output = layers_output.replace("&mo LAYER_Mod", "&magic LAYER_Mod 0")

    # Build complete keymap
    output = """/*
 * Glove80 keymap — auto-generated from Kinesis Adv360 Pro sunaku config
 * Source: tools/kinesis2glove80.py
 *
 * WARNING: This file is auto-generated. Edit the Kinesis source and re-run
 * the generator, or your changes will be lost on next sync.
 */

#include <input/processors.dtsi>
#include <behaviors.dtsi>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/outputs.h>
#include <dt-bindings/zmk/pointing.h>
#include <dt-bindings/zmk/rgb.h>
#include "layers.dtsi"

#define MOUSE_LAYER_SLOW 18
#define MOUSE_LAYER_FAST 19
#define MOUSE_LAYER_WARP 20

&mmv {{
    acceleration-exponent = <1>;
    time-to-max-speed-ms = <300>;
    delay-ms = <0>;
}};

&msc {{
    acceleration-exponent = <0>;
    time-to-max-speed-ms = <300>;
    delay-ms = <0>;
}};

// Mouse movement speed scaling per layer

&mmv_input_listener {{
    slow {{
        layers = <MOUSE_LAYER_SLOW>;
        input-processors = <&zip_xy_scaler 1 12>;
    }};

    fast {{
        layers = <MOUSE_LAYER_FAST>;
        input-processors = <&zip_xy_scaler 4 1>;
    }};

    warp {{
        layers = <MOUSE_LAYER_WARP>;
        input-processors = <&zip_xy_scaler 12 1>;
    }};
}};

&msc_input_listener {{
    slow {{
        layers = <MOUSE_LAYER_SLOW>;
        input-processors = <&zip_scroll_scaler 1 9>;
    }};

    fast {{
        layers = <MOUSE_LAYER_FAST>;
        input-processors = <&zip_scroll_scaler 3 1>;
    }};

    warp {{
        layers = <MOUSE_LAYER_WARP>;
        input-processors = <&zip_scroll_scaler 9 1>;
    }};
}};

&caps_word {{
    continue-list = <
        UNDERSCORE MINUS KP_MINUS
        BACKSPACE DELETE
        LEFT_SHIFT RIGHT_SHIFT
        N1 N2 N3 N4 N5 N6 N7 N8 N9 N0
        KP_N1 KP_N2 KP_N3 KP_N4 KP_N5 KP_N6 KP_N7 KP_N8 KP_N9 KP_N0
    >;
}};

/ {{
    behaviors {{
{macros_content}

        // Per-finger home row mods — left hand
        left_pinky: homey_left_pinky {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <PINKY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_ringy: homey_left_ringy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <RINGY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_middy: homey_left_middy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <MIDDY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_index: homey_left_index {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <INDEX_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        // Per-finger home row mods — right hand
        right_pinky: homey_right_pinky {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <PINKY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_ringy: homey_right_ringy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <RINGY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_middy: homey_right_middy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <MIDDY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_index: homey_right_index {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <INDEX_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        // Bilateral enforcement hold-tap behaviors
        left_pinky_bilateral: homey_left_pinky_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&left_pinky_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <PINKY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_ringy_bilateral: homey_left_ringy_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&left_ringy_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <RINGY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_middy_bilateral: homey_left_middy_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&left_middy_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <MIDDY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_index_bilateral: homey_left_index_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&left_index_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <INDEX_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        right_index_bilateral: homey_right_index_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&right_index_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <INDEX_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_middy_bilateral: homey_right_middy_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&right_middy_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <MIDDY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_ringy_bilateral: homey_right_ringy_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&right_ringy_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <RINGY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_pinky_bilateral: homey_right_pinky_bilateral {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&right_pinky_hold>, <&kp>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <PINKY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        // Cross-finger bilateral behaviors
        left_pinky_cross: cross_left_pinky {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&left_pinky_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <PINKY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_ringy_cross: cross_left_ringy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&left_ringy_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <RINGY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_middy_cross: cross_left_middy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&left_middy_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <MIDDY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        left_index_cross: cross_left_index {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&left_index_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <INDEX_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <RIGHT_HAND_KEYS THUMB_KEYS>;
        }};

        right_index_cross: cross_right_index {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&right_index_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <INDEX_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_middy_cross: cross_right_middy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&right_middy_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <MIDDY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_ringy_cross: cross_right_ringy {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&right_ringy_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <RINGY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        right_pinky_cross: cross_right_pinky {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&right_pinky_tap>;
            flavor = HOMEY_HOLDING_TYPE;
            tapping-term-ms = <PINKY_HOLDING_TIME>;
            quick-tap-ms = <HOMEY_REPEAT_DECAY>;
            require-prior-idle-ms = <HOMEY_STREAK_DECAY>;
            hold-trigger-on-release;
            hold-trigger-key-positions = <LEFT_HAND_KEYS THUMB_KEYS>;
        }};

        // Thumb cluster layer-tap
        thumb: thumb_layer_access {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&mo>, <&kp>;
            flavor = THUMB_HOLDING_TYPE;
            tapping-term-ms = <THUMB_HOLDING_TIME>;
            quick-tap-ms = <THUMB_REPEAT_DECAY>;
        }};

        // Sticky key one-shot
        sticky_key_modtap: sticky_key_modtap {{
            compatible = "zmk,behavior-hold-tap";
            #binding-cells = <2>;
            bindings = <&kp>, <&sticky_key_oneshot>;
            flavor = "tap-preferred";
            tapping-term-ms = <STICKY_HOLDING_TIME>;
        }};
        sticky_key_oneshot: sticky_key_oneshot_macro {{
            compatible = "zmk,behavior-macro-one-param";
            wait-ms = <0>;
            tap-ms = <0>;
            #binding-cells = <1>;
            bindings
              = <&macro_param_1to1>
              , <&macro_tap &sticky_key_quickrel MACRO_PLACEHOLDER>
              ;
        }};
        sticky_key_quickrel: sticky_key_quick_release {{
            compatible = "zmk,behavior-sticky-key";
            #binding-cells = <1>;
            bindings = <&kp>;
            release-after-ms = <STICKY_1SHOT_DECAY>;
            quick-release;
            ignore-modifiers;
        }};

        key_lh_t2: key_lh_t2 {{
            compatible = "zmk,behavior-mod-morph";
            label = "KEY_LH_T2";
            bindings = <&kp LS(N3)>, <&kp LG(LS(N4))>;
            #binding-cells = <0>;
            mods = <(MOD_LSFT|MOD_RSFT)>;
        }};

        key_rh_t2: key_rh_t2 {{
            compatible = "zmk,behavior-mod-morph";
            label = "KEY_RH_T2";
            bindings = <&kp LS(N6)>, <&kp LG(LS(N5))>;
            #binding-cells = <0>;
            mods = <(MOD_LSFT|MOD_RSFT)>;
        }};

        // Glove80 magic key (RGB status)
        magic: magic_hold_tap {{
            compatible = "zmk,behavior-hold-tap";
            label = "MAGIC_HOLD_TAP";
            #binding-cells = <2>;
            flavor = "tap-preferred";
            tapping-term-ms = <200>;
            bindings = <&mo>, <&rgb_ug_status_macro>;
        }};
    }};

    macros {{
        rgb_ug_status_macro: rgb_ug_status_macro_0 {{
            label = "RGB_UG_STATUS";
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings = <&rgb_ug RGB_STATUS>;
        }};

        bt_0: bt_profile_macro_0 {{
            label = "BT_0";
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings = <&out OUT_BLE &bt BT_SEL 0>;
        }};

        bt_1: bt_profile_macro_1 {{
            label = "BT_1";
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings = <&out OUT_BLE &bt BT_SEL 1>;
        }};

        bt_2: bt_profile_macro_2 {{
            label = "BT_2";
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings = <&out OUT_BLE &bt BT_SEL 2>;
        }};

        bt_3: bt_profile_macro_3 {{
            label = "BT_3";
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings = <&out OUT_BLE &bt BT_SEL 3>;
        }};
    }};

    // Combos omitted — accessible through layers

    keymap {{
        compatible = "zmk,keymap";

{layers_output}
    }};
}};
""".format(
        macros_content=macros_content,
        layers_output=layers_output,
    )

    return output


def main():
    dry_run = "--dry-run" in sys.argv
    output_layers = "--layers-only" in sys.argv

    if output_layers:
        print(generate_layers_dtsi())
        return

    keymap = generate_glove80_keymap()

    if dry_run:
        print(keymap)
    else:
        # Write to stdout (pipe to file)
        print(keymap)


if __name__ == "__main__":
    main()
