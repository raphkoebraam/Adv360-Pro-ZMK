#!/usr/bin/env python3
"""
Kinesis Adv360 Pro <-> Glove80 keymap position translator.

Reads a ZMK keymap file, extracts layer bindings, and remaps key positions
between the two keyboards.

Usage:
  ./keymap_sync.py kinesis2glove80 config/adv360.keymap > glove80_layers.txt
  ./keymap_sync.py glove802kinesis ../glove80-keymaps/keymap.zmk > kinesis_layers.txt
  ./keymap_sync.py diff config/adv360.keymap ../glove80-keymaps/keymap.zmk
"""

import re
import sys
from typing import Optional

# ===========================================================================
# Position mapping tables
# ===========================================================================
#
# Kinesis Adv360 Pro: 76 keys (positions 0-75)
# Glove80: 80 keys (positions 0-79)
#
# Kinesis layout:
# Row 0: [ 0][ 1][ 2][ 3][ 4][ 5]  [ 6]              [ 7]  [ 8][ 9][10][11][12][13]
# Row 1: [14][15][16][17][18][19]  [20]                [21]  [22][23][24][25][26][27]
# Row 2: [28][29][30][31][32][33]  [34]  [35][36] [37][38]  [39]  [40][41][42][43][44][45]
# Row 3: [46][47][48][49][50][51]        [52]     [53]        [54][55][56][57][58][59]
# Row 4: [60][61][62][63][64]      [65][66][67] [68][69][70]      [71][72][73][74][75]
#
# Glove80 layout:
# Row 0: [ 0][ 1][ 2][ 3][ 4]                                        [ 5][ 6][ 7][ 8][ 9]
# Row 1: [10][11][12][13][14][15]                                [16][17][18][19][20][21]
# Row 2: [22][23][24][25][26][27]                                [28][29][30][31][32][33]
# Row 3: [34][35][36][37][38][39]                                [40][41][42][43][44][45]
# Row 4: [46][47][48][49][50][51]  [52][53][54]  [55][56][57]  [58][59][60][61][62][63]
# Row 5: [64][65][66][67][68]      [69][70][71]  [72][73][74]      [75][76][77][78][79]

# Kinesis position -> Glove80 position (None = no equivalent / inner column)
KINESIS_TO_GLOVE80 = {
    # Row 0 (numbers)
    0: 10, 1: 11, 2: 12, 3: 13, 4: 14, 5: 15,
    6: None,  # inner column left
    7: None,  # inner column right
    8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21,
    # Row 1 (QWERTY)
    14: 22, 15: 23, 16: 24, 17: 25, 18: 26, 19: 27,
    20: None,  # inner column left
    21: None,  # inner column right
    22: 28, 23: 29, 24: 30, 25: 31, 26: 32, 27: 33,
    # Row 2 (home)
    28: 34, 29: 35, 30: 36, 31: 37, 32: 38, 33: 39,
    34: None,  # inner column left
    35: 52, 36: 53,  # center left -> Glove80 row 4 middle
    37: 56, 38: 57,  # center right -> Glove80 row 4 middle
    39: None,  # inner column right
    40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 45,
    # Row 3 (below home)
    46: 46, 47: 47, 48: 48, 49: 49, 50: 50, 51: 51,
    52: 54, 53: 55,  # center -> Glove80 row 4 middle
    54: 58, 55: 59, 56: 60, 57: 61, 58: 62, 59: 63,
    # Row 4 (thumb/bottom)
    60: 64, 61: 65, 62: 66, 63: 67, 64: 68,
    65: 69, 66: 70, 67: 71,
    68: 72, 69: 73, 70: 74,
    71: 75, 72: 76, 73: 77, 74: 78, 75: 79,
}

# Glove80 position -> Kinesis position (None = no equivalent / F-key row)
GLOVE80_TO_KINESIS = {}
for k, v in KINESIS_TO_GLOVE80.items():
    if v is not None:
        GLOVE80_TO_KINESIS[v] = k

# Glove80 positions with no Kinesis equivalent (F-key row)
for i in range(10):
    if i not in GLOVE80_TO_KINESIS:
        GLOVE80_TO_KINESIS[i] = None

KINESIS_KEY_COUNT = 76
GLOVE80_KEY_COUNT = 80

# Glove80 row structure (for formatting output)
GLOVE80_ROWS = [
    list(range(0, 5)),        # Row 0: 5 left
    list(range(5, 10)),       # Row 0: 5 right
    list(range(10, 16)),      # Row 1: 6 left
    list(range(16, 22)),      # Row 1: 6 right
    list(range(22, 28)),      # Row 2: 6 left
    list(range(28, 34)),      # Row 2: 6 right
    list(range(34, 40)),      # Row 3: 6 left
    list(range(40, 46)),      # Row 3: 6 right
    list(range(46, 58)),      # Row 4: 6+3+3 left+center
    list(range(58, 64)),      # Row 4: 6 right
    list(range(64, 72)),      # Row 5: 5+3 left
    list(range(72, 80)),      # Row 5: 3+5 right
]

# Kinesis row structure (for formatting output) — matches adv360.keymap binding order
KINESIS_ROWS = [
    list(range(0, 7)) + list(range(7, 14)),         # Row 0: 14 keys
    list(range(14, 21)) + list(range(21, 28)),       # Row 1: 14 keys
    list(range(28, 35)) + list(range(35, 40)) + list(range(39, 46)),  # Row 2: 18 keys
    list(range(46, 54)) + list(range(54, 60)),       # Row 3: 14 keys
    list(range(60, 68)) + list(range(68, 76)),       # Row 4: 16 keys
]


def parse_bindings(text: str) -> list[str]:
    """Extract individual key bindings from a bindings = < ... > block."""
    bindings = []
    # Match individual bindings: &behavior [params...]
    # Each binding starts with & and continues until the next & or >
    pattern = re.compile(r'&\S+(?:\s+(?!&)[^\s>]+)*')
    for match in pattern.finditer(text):
        bindings.append(match.group().strip())
    return bindings


def extract_layers(filepath: str,
                   min_keys: int = 10) -> dict[str, list[str]]:
    """Extract keymap layers and their bindings from a ZMK keymap file.

    Only includes blocks with at least min_keys bindings (filters out
    non-layer blocks like behaviors and macros).
    """
    with open(filepath) as f:
        content = f.read()

    layers = {}
    # Match layer blocks nested inside keymap block.
    # Find bindings = < ... >; inside named blocks, take the innermost
    # block name (closest { before bindings).
    # Pattern: word { [no braces] bindings = < ... >;
    layer_pattern = re.compile(
        r'(\w+)\s*\{\s*bindings\s*=\s*<(.*?)>\s*;',
        re.DOTALL
    )
    # Skip non-layer container blocks
    skip_names = {"keymap", "behaviors", "combos", "macros"}
    for match in layer_pattern.finditer(content):
        name = match.group(1)
        if name in skip_names:
            continue
        bindings_text = match.group(2)
        bindings = parse_bindings(bindings_text)
        if len(bindings) >= min_keys:
            layers[name] = bindings

    return layers


def kinesis_to_glove80(bindings: list[str], fill: str = "&none") -> list[str]:
    """Convert 76 Kinesis bindings to 80 Glove80 bindings."""
    glove80 = [fill] * GLOVE80_KEY_COUNT

    for k_pos, binding in enumerate(bindings):
        g_pos = KINESIS_TO_GLOVE80.get(k_pos)
        if g_pos is not None:
            glove80[g_pos] = binding

    return glove80


def glove80_to_kinesis(bindings: list[str], fill: str = "&none") -> list[str]:
    """Convert 80 Glove80 bindings to 76 Kinesis bindings."""
    kinesis = [fill] * KINESIS_KEY_COUNT

    for g_pos, binding in enumerate(bindings):
        k_pos = GLOVE80_TO_KINESIS.get(g_pos)
        if k_pos is not None:
            kinesis[k_pos] = binding

    return kinesis


def format_bindings(bindings: list[str], pad: int = 20) -> str:
    """Format bindings into aligned rows."""
    lines = []
    for binding in bindings:
        lines.append(binding.ljust(pad))
    return " ".join(lines)


def format_layer_kinesis(name: str, bindings: list[str]) -> str:
    """Format a layer in Kinesis keymap format (76 keys, 5 rows)."""
    rows = [
        # Row 0: 7 left + 7 right = 14
        bindings[0:7] + bindings[7:14],
        # Row 1: 7 left + 7 right = 14
        bindings[14:21] + bindings[21:28],
        # Row 2: 7 left + 6 center + 7 right = 18 (note: 28-34, 35-38, 39-45 but 39 overlaps)
        bindings[28:35] + bindings[35:40] + bindings[40:46],
        # Row 3: 8 left+center + 6 right = 14
        bindings[46:54] + bindings[54:60],
        # Row 4: 8 left+thumb + 8 right+thumb = 16
        bindings[60:68] + bindings[68:76],
    ]
    lines = []
    for row in rows:
        lines.append(" ".join(row))
    return f"        {name} {{\n            bindings = <\n" + \
           "\n".join(lines) + \
           "\n            >;\n        }};"


def print_diff(layer_name: str,
               kinesis_bindings: list[str],
               glove80_bindings: list[str]):
    """Show differences between Kinesis and Glove80 layer bindings."""
    diffs = []

    for k_pos in range(KINESIS_KEY_COUNT):
        g_pos = KINESIS_TO_GLOVE80.get(k_pos)
        if g_pos is None:
            continue

        k_bind = kinesis_bindings[k_pos] if k_pos < len(kinesis_bindings) else "???"
        g_bind = glove80_bindings[g_pos] if g_pos < len(glove80_bindings) else "???"

        if k_bind != g_bind:
            diffs.append((k_pos, g_pos, k_bind, g_bind))

    if not diffs:
        print(f"  {layer_name}: identical")
    else:
        print(f"  {layer_name}: {len(diffs)} differences")
        for k_pos, g_pos, k_bind, g_bind in diffs:
            print(f"    K[{k_pos:2d}]->G[{g_pos:2d}]: {k_bind:30s} vs {g_bind}")


def cmd_convert(direction: str, filepath: str):
    """Convert keymap between formats."""
    layers = extract_layers(filepath)

    if not layers:
        print(f"Error: no layers found in {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"# Extracted {len(layers)} layers from {filepath}")
    print(f"# Direction: {direction}")
    print()

    for name, bindings in layers.items():
        key_count = len(bindings)
        print(f"# Layer: {name} ({key_count} keys)")

        if direction == "kinesis2glove80":
            if key_count != KINESIS_KEY_COUNT:
                print(f"#   WARNING: expected {KINESIS_KEY_COUNT} keys, got {key_count}")
            converted = kinesis_to_glove80(bindings)
        else:
            if key_count != GLOVE80_KEY_COUNT:
                print(f"#   WARNING: expected {GLOVE80_KEY_COUNT} keys, got {key_count}")
            converted = glove80_to_kinesis(bindings)

        for i, b in enumerate(converted):
            print(f"  [{i:2d}] {b}")
        print()


def cmd_diff(kinesis_path: str, glove80_path: str):
    """Compare layers between Kinesis and Glove80 keymaps."""
    k_layers = extract_layers(kinesis_path)
    g_layers = extract_layers(glove80_path)

    print(f"Kinesis: {len(k_layers)} layers from {kinesis_path}")
    print(f"Glove80: {len(g_layers)} layers from {glove80_path}")
    print()

    # Try to match layers by name similarity
    matches = []
    for k_name in k_layers:
        for g_name in g_layers:
            # Match by substring (e.g., "default_layer" matches "layer_QWERTY")
            k_lower = k_name.lower().replace("layer_", "").replace("_layer", "")
            g_lower = g_name.lower().replace("layer_", "").replace("_layer", "")
            if k_lower == g_lower or k_lower in g_lower or g_lower in k_lower:
                matches.append((k_name, g_name))

    if matches:
        print("Matched layers:")
        for k_name, g_name in matches:
            print_diff(f"{k_name} <-> {g_name}",
                       k_layers[k_name], g_layers[g_name])
    else:
        print("No matching layer names found.")
        print(f"  Kinesis layers: {', '.join(k_layers.keys())}")
        print(f"  Glove80 layers: {', '.join(g_layers.keys())}")


def cmd_positions():
    """Print the position mapping table."""
    print("Kinesis -> Glove80 position mapping:")
    print()
    for k_pos in range(KINESIS_KEY_COUNT):
        g_pos = KINESIS_TO_GLOVE80.get(k_pos)
        marker = " (inner column, dropped)" if g_pos is None else ""
        g_str = f"G[{g_pos:2d}]" if g_pos is not None else "  --  "
        print(f"  K[{k_pos:2d}] -> {g_str}{marker}")

    print()
    print("Glove80 positions without Kinesis equivalent:")
    for g_pos in range(GLOVE80_KEY_COUNT):
        if g_pos not in GLOVE80_TO_KINESIS or GLOVE80_TO_KINESIS[g_pos] is None:
            print(f"  G[{g_pos:2d}] (F-key row)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd in ("kinesis2glove80", "glove802kinesis"):
        if len(sys.argv) < 3:
            print(f"Usage: {sys.argv[0]} {cmd} <keymap_file>")
            sys.exit(1)
        cmd_convert(cmd, sys.argv[2])

    elif cmd == "diff":
        if len(sys.argv) < 4:
            print(f"Usage: {sys.argv[0]} diff <kinesis_keymap> <glove80_keymap>")
            sys.exit(1)
        cmd_diff(sys.argv[2], sys.argv[3])

    elif cmd == "positions":
        cmd_positions()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
