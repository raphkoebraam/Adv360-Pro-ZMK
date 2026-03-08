#!/usr/bin/env python3
"""
Sync shared layers between Kinesis Adv360 Pro and Glove80 ZMK keymaps.

Usage:
    keymap_sync.py diff                      # Show differences in shared layers
    keymap_sync.py sync --to glove80         # Sync from Kinesis → Glove80
    keymap_sync.py sync --to kinesis         # Sync from Glove80 → Kinesis
    keymap_sync.py sync --to glove80 -l mouse nav_symbol  # Sync specific layers

The script handles the position mapping between the 76-key Kinesis Adv360 Pro
and the 80-key MoErgo Glove80, accounting for:
  - Glove80's extra F-key row (row 0, 10 keys) — no Kinesis equivalent
  - Kinesis's inner columns (2 extra keys per half on rows 0-2) — no Glove80 equivalent
  - Different center key arrangement (Kinesis: split across rows 2-3, Glove80: all in row 4)
  - Identical thumb row layout (16 keys each)
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# ─── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
KINESIS_KEYMAP = SCRIPT_DIR.parent / "config" / "adv360.keymap"
GLOVE80_KEYMAP = SCRIPT_DIR.parent / ".." / "glove80-zmk-config" / "config" / "glove80.keymap"

# ─── Physical Layout ─────────────────────────────────────────────────────────
#
# Kinesis Adv360 Pro (76 keys, 5 rows):
#   Row 0: 14 keys (7L + 7R)         — number row + inner layer keys
#   Row 1: 14 keys (7L + 7R)         — top alpha + inner extra keys
#   Row 2: 18 keys (7L + 4ctr + 7R)  — home row + center column
#   Row 3: 14 keys (6L + 2ctr + 6R)  — bottom alpha + center keys
#   Row 4: 16 keys (5L + 6thm + 5R)  — bottom row + thumb cluster
#
# Glove80 (80 keys, 6 rows):
#   Row 0: 10 keys (5L + 5R)         — F-key row (no Kinesis equivalent)
#   Row 1: 12 keys (6L + 6R)         — number row
#   Row 2: 12 keys (6L + 6R)         — top alpha
#   Row 3: 12 keys (6L + 6R)         — home row
#   Row 4: 18 keys (6L + 6ctr + 6R)  — bottom alpha + center column
#   Row 5: 16 keys (5L + 6thm + 5R)  — bottom row + thumb cluster

KINESIS_ROW_SIZES = [14, 14, 18, 14, 16]  # total 76
GLOVE80_ROW_SIZES = [10, 12, 12, 12, 18, 16]  # total 80

# Position mapping: Kinesis position → Glove80 position
# None = Kinesis-only key (inner column), no Glove80 equivalent
KINESIS_TO_GLOVE80 = {
    # Row 0 (number) → Glove80 Row 1
    0: 10, 1: 11, 2: 12, 3: 13, 4: 14, 5: 15,
    6: None, 7: None,  # inner column keys (layer toggle)
    8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21,

    # Row 1 (top alpha) → Glove80 Row 2
    14: 22, 15: 23, 16: 24, 17: 25, 18: 26, 19: 27,
    20: None, 21: None,  # inner column keys (screenshot)
    22: 28, 23: 29, 24: 30, 25: 31, 26: 32, 27: 33,

    # Row 2 (home + center) → Glove80 Row 3 + Row 4 center
    28: 34, 29: 35, 30: 36, 31: 37, 32: 38, 33: 39,
    34: None,  # inner column (left)
    35: 52, 36: 53,  # center-left → Glove80 row 4 center-left
    37: 56, 38: 57,  # center-right → Glove80 row 4 center-right
    39: None,  # inner column (right)
    40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 45,

    # Row 3 (bottom alpha + center) → Glove80 Row 4 outer + center
    46: 46, 47: 47, 48: 48, 49: 49, 50: 50, 51: 51,
    52: 54, 53: 55,  # center → Glove80 row 4 center
    54: 58, 55: 59, 56: 60, 57: 61, 58: 62, 59: 63,

    # Row 4 (thumb) → Glove80 Row 5 (1:1 mapping)
    60: 64, 61: 65, 62: 66, 63: 67, 64: 68,
    65: 69, 66: 70, 67: 71, 68: 72, 69: 73, 70: 74,
    71: 75, 72: 76, 73: 77, 74: 78, 75: 79,
}

# Reverse mapping: Glove80 position → Kinesis position
GLOVE80_TO_KINESIS = {v: k for k, v in KINESIS_TO_GLOVE80.items() if v is not None}

# Glove80-only positions (F-key row) — no Kinesis equivalent
GLOVE80_ONLY_POSITIONS = set(range(10))  # positions 0-9

# Kinesis-only positions (inner columns) — no Glove80 equivalent
KINESIS_ONLY_POSITIONS = {k for k, v in KINESIS_TO_GLOVE80.items() if v is None}

# ─── Shared Layers ───────────────────────────────────────────────────────────
# Map of layer names: (kinesis_name, glove80_name)
# These layers have identical logical content, just different physical grids.

SHARED_LAYERS = {
    "nav_symbol": ("nav_symbol", "nav_symbol"),
    "mouse": ("mouse", "mouse"),
    "mouse_slow": ("mouse_slow", "mouse_slow"),
    "mouse_fast": ("mouse_fast", "mouse_fast"),
    "mouse_warp": ("mouse_warp", "mouse_warp"),
    "keypad": ("keypad", "lower_layer"),
    "default": ("default_layer", "default_layer"),
}

DEFAULT_SYNC_LAYERS = ["nav_symbol", "mouse", "mouse_slow", "mouse_fast", "mouse_warp"]

# ─── Parser ──────────────────────────────────────────────────────────────────


@dataclass
class Layer:
    name: str
    bindings: list[str]  # flat list of binding strings
    raw_block: str  # original text of the bindings = < ... >; block
    start_offset: int  # character offset in file where bindings block starts
    end_offset: int  # character offset where bindings block ends


def parse_bindings(text: str) -> list[str]:
    """Parse a ZMK bindings block into a flat list of binding strings.

    Each binding starts with & and may have parameters.
    Example: "&kp EQUAL" or "&hml LEFT_CONTROL Z" or "&lt 5 BACKSPACE"
    """
    # Strip angle brackets if present
    text = text.strip()
    if text.startswith("<"):
        text = text[1:]
    if text.endswith(">"):
        text = text[:-1]

    # Split on & boundaries
    parts = re.split(r"(?=&)", text)
    bindings = []
    for part in parts:
        part = part.strip()
        if part:
            # Normalize whitespace within the binding
            part = " ".join(part.split())
            bindings.append(part)
    return bindings


def parse_defines(content: str) -> dict[str, str]:
    """Extract #define macros from keymap content.

    Returns a dict mapping define name to its value.
    Only captures simple numeric defines (e.g., #define MOUSE 5).
    """
    defines = {}
    for match in re.finditer(r"#define\s+(\w+)\s+(\d+)", content):
        defines[match.group(1)] = match.group(2)
    return defines


def resolve_defines(binding: str, defines: dict[str, str]) -> str:
    """Replace #define names with their numeric values in a binding.

    Example: "&tog MOUSE_LAYER_FAST" with defines={MOUSE_LAYER_FAST: "7"}
    becomes "&tog 7".
    """
    parts = binding.split()
    resolved = []
    for part in parts:
        if part in defines:
            resolved.append(defines[part])
        else:
            resolved.append(part)
    return " ".join(resolved)


def parse_keymap(path: Path) -> tuple[dict[str, Layer], dict[str, str]]:
    """Parse a ZMK keymap file and extract all layers with their bindings.

    Returns (layers_dict, defines_dict).
    """
    content = path.read_text()
    layers = {}
    defines = parse_defines(content)

    # Find the keymap block
    keymap_match = re.search(r"keymap\s*\{", content)
    if not keymap_match:
        print(f"Error: Could not find keymap block in {path}", file=sys.stderr)
        sys.exit(1)

    keymap_start = keymap_match.start()

    # Find all layer blocks within the keymap.
    # Layers are direct children of the keymap block. Each has:
    #   layer_name { bindings = < ... >; };
    # We skip the "keymap" block itself by requiring the layer name
    # to NOT be "keymap" (which is the container, not a layer).
    # [^{}]*? prevents crossing nested brace boundaries, so we only match
    # direct children of the keymap block (layers), not the keymap itself.
    layer_pattern = re.compile(
        r"(\w+)\s*\{"  # layer name and opening brace
        r"([^{}]*?)"  # content before bindings (no braces — can't cross blocks)
        r"bindings\s*=\s*<"  # bindings = <
        r"(.*?)"  # binding content (non-greedy)
        r">\s*;",  # >;
        re.DOTALL,
    )

    for match in layer_pattern.finditer(content, keymap_start):
        name = match.group(1)

        bindings_text = match.group(3)
        bindings = parse_bindings(bindings_text)

        # Calculate offsets for the bindings = < ... >; portion
        bindings_start = match.start(3) - 1  # include the <
        bindings_end = match.end(3) + 1  # include the >

        layers[name] = Layer(
            name=name,
            bindings=bindings,
            raw_block=match.group(0),
            start_offset=bindings_start,
            end_offset=bindings_end,
        )

    return layers, defines


# ─── Translation ─────────────────────────────────────────────────────────────


def translate_bindings(
    source_bindings: list[str],
    source_keyboard: str,
    target_current_bindings: Optional[list[str]] = None,
) -> list[str]:
    """Translate layer bindings from one keyboard layout to another.

    Args:
        source_bindings: Flat list of bindings from the source keyboard
        source_keyboard: "kinesis" or "glove80"
        target_current_bindings: Current bindings on target (to preserve keyboard-only keys)

    Returns:
        Flat list of bindings for the target keyboard
    """
    if source_keyboard == "kinesis":
        mapping = KINESIS_TO_GLOVE80
        target_size = 80
        target_only = GLOVE80_ONLY_POSITIONS
    else:
        mapping = GLOVE80_TO_KINESIS
        target_size = 76
        target_only = KINESIS_ONLY_POSITIONS

    # Start with current target bindings or defaults
    if target_current_bindings and len(target_current_bindings) == target_size:
        result = list(target_current_bindings)
    else:
        result = ["&trans"] * target_size

    # Map each source position to target position
    for src_pos, binding in enumerate(source_bindings):
        if src_pos in mapping:
            tgt_pos = mapping[src_pos]
            if tgt_pos is not None:
                result[tgt_pos] = binding

    return result


def format_bindings(bindings: list[str], keyboard: str, indent: str = "") -> str:
    """Format a flat list of bindings into the ZMK keymap row structure.

    Args:
        bindings: Flat list of binding strings
        keyboard: "kinesis" or "glove80"
        indent: Whitespace prefix for each row line
    """
    row_sizes = (
        KINESIS_ROW_SIZES if keyboard == "kinesis" else GLOVE80_ROW_SIZES
    )

    lines = []
    pos = 0
    for row_size in row_sizes:
        row_bindings = bindings[pos : pos + row_size]
        line = indent + "  ".join(row_bindings)
        lines.append(line)
        pos += row_size

    return "\n".join(lines)


# ─── Diff ────────────────────────────────────────────────────────────────────

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
DIM = "\033[2m"
BOLD = "\033[1m"


def diff_layer(
    layer_name: str,
    kinesis_layer: Optional[Layer],
    glove80_layer: Optional[Layer],
    kinesis_defines: dict[str, str] = None,
    glove80_defines: dict[str, str] = None,
) -> bool:
    """Compare a shared layer between keyboards. Returns True if different."""
    if not kinesis_layer or not glove80_layer:
        if not kinesis_layer:
            print(f"  {YELLOW}Layer missing on Kinesis{RESET}")
        if not glove80_layer:
            print(f"  {YELLOW}Layer missing on Glove80{RESET}")
        return True

    kinesis_defines = kinesis_defines or {}
    glove80_defines = glove80_defines or {}

    # Translate Kinesis → Glove80 format and compare with actual Glove80
    translated = translate_bindings(
        kinesis_layer.bindings, "kinesis", glove80_layer.bindings
    )

    differences = []
    for pos in range(80):
        if pos in GLOVE80_ONLY_POSITIONS:
            continue  # Skip F-key row (Glove80-only)
        if pos not in GLOVE80_TO_KINESIS:
            continue  # Skip positions with no mapping

        actual = glove80_layer.bindings[pos] if pos < len(glove80_layer.bindings) else "???"
        expected = translated[pos]

        # Compare with defines resolved (e.g., &tog MOUSE == &tog 5)
        actual_resolved = resolve_defines(actual, glove80_defines)
        expected_resolved = resolve_defines(expected, kinesis_defines)

        if actual_resolved != expected_resolved:
            kinesis_pos = GLOVE80_TO_KINESIS[pos]
            differences.append((pos, kinesis_pos, expected, actual))

    if not differences:
        print(f"  {GREEN}In sync ✓{RESET}")
        return False

    print(f"  {RED}{len(differences)} difference(s):{RESET}")
    for g_pos, k_pos, expected, actual in differences:
        print(f"    pos K{k_pos}/G{g_pos}: Kinesis has {CYAN}{expected}{RESET}, Glove80 has {YELLOW}{actual}{RESET}")

    return True


def cmd_diff(args):
    """Show differences between shared layers on both keyboards."""
    kinesis_layers, kinesis_defines = parse_keymap(KINESIS_KEYMAP)
    glove80_layers, glove80_defines = parse_keymap(GLOVE80_KEYMAP)

    layers_to_check = args.layers or DEFAULT_SYNC_LAYERS
    any_diff = False

    for layer_name in layers_to_check:
        if layer_name not in SHARED_LAYERS:
            print(f"{YELLOW}Warning: '{layer_name}' is not a known shared layer{RESET}")
            continue

        k_name, g_name = SHARED_LAYERS[layer_name]
        print(f"\n{BOLD}Layer: {layer_name}{RESET} (Kinesis: {k_name}, Glove80: {g_name})")

        k_layer = kinesis_layers.get(k_name)
        g_layer = glove80_layers.get(g_name)

        if diff_layer(layer_name, k_layer, g_layer, kinesis_defines, glove80_defines):
            any_diff = True

    if not any_diff:
        print(f"\n{GREEN}All shared layers are in sync!{RESET}")
    else:
        print(f"\n{YELLOW}Some layers differ. Use 'sync --to <target>' to sync.{RESET}")

    return 1 if any_diff else 0


# ─── Sync ────────────────────────────────────────────────────────────────────


def replace_layer_bindings(
    content: str, layer_name: str, new_bindings: list[str], keyboard: str
) -> str:
    """Replace a layer's bindings in the keymap file content."""
    # Find the layer block — \b ensures we don't match partial names
    # (e.g., "mouse" won't match inside "mouse_slow")
    # [^{}]*? prevents crossing nested brace boundaries
    pattern = re.compile(
        r"(\b" + re.escape(layer_name) + r"\s*\{[^{}]*?"
        r"bindings\s*=\s*)<"
        r"(.*?)"
        r">\s*(;)",
        re.DOTALL,
    )

    match = pattern.search(content)
    if not match:
        print(f"  {RED}Error: Could not find layer '{layer_name}' bindings{RESET}", file=sys.stderr)
        return content

    # Detect indentation from the original bindings block
    original_bindings = match.group(2)
    indent_match = re.search(r"\n(\s*)&", original_bindings)
    indent = indent_match.group(1) if indent_match else ""

    formatted = format_bindings(new_bindings, keyboard, indent)
    replacement = f"{match.group(1)}<\n{formatted}\n{indent}>{match.group(3)}"

    return content[: match.start()] + replacement + content[match.end() :]


def cmd_sync(args):
    """Sync shared layers from source to target keyboard."""
    target = args.to
    source = "glove80" if target == "kinesis" else "kinesis"

    kinesis_layers, kinesis_defines = parse_keymap(KINESIS_KEYMAP)
    glove80_layers, glove80_defines = parse_keymap(GLOVE80_KEYMAP)
    source_defines = kinesis_defines if source == "kinesis" else glove80_defines
    target_defines = glove80_defines if target == "glove80" else kinesis_defines

    if source == "kinesis":
        source_layers = kinesis_layers
        target_layers = glove80_layers
        target_path = GLOVE80_KEYMAP
    else:
        source_layers = glove80_layers
        target_layers = kinesis_layers
        target_path = KINESIS_KEYMAP

    layers_to_sync = args.layers or DEFAULT_SYNC_LAYERS
    target_content = target_path.read_text()
    changes_made = 0

    for layer_name in layers_to_sync:
        if layer_name not in SHARED_LAYERS:
            print(f"{YELLOW}Warning: '{layer_name}' is not a known shared layer, skipping{RESET}")
            continue

        k_name, g_name = SHARED_LAYERS[layer_name]
        s_name = k_name if source == "kinesis" else g_name
        t_name = g_name if target == "glove80" else k_name

        print(f"\n{BOLD}Syncing: {layer_name}{RESET} ({source}:{s_name} → {target}:{t_name})")

        s_layer = source_layers.get(s_name)
        t_layer = target_layers.get(t_name)

        if not s_layer:
            print(f"  {RED}Source layer '{s_name}' not found, skipping{RESET}")
            continue

        if not t_layer:
            print(f"  {RED}Target layer '{t_name}' not found, skipping{RESET}")
            continue

        # Translate and check for changes
        new_bindings = translate_bindings(
            s_layer.bindings, source, t_layer.bindings
        )

        # Compare with defines resolved to get accurate change count
        new_resolved = [resolve_defines(b, source_defines) for b in new_bindings]
        old_resolved = [resolve_defines(b, target_defines) for b in t_layer.bindings]

        if new_resolved == old_resolved:
            print(f"  {GREEN}Already in sync ✓{RESET}")
            continue

        # Count semantic changes (after define resolution)
        diffs = sum(
            1
            for a, b in zip(new_resolved, old_resolved)
            if a != b
        )
        print(f"  {CYAN}Updating {diffs} binding(s){RESET}")

        target_content = replace_layer_bindings(
            target_content, t_name, new_bindings, target
        )
        changes_made += 1

    if changes_made == 0:
        print(f"\n{GREEN}Nothing to sync — all layers already match!{RESET}")
        return 0

    if args.dry_run:
        print(f"\n{YELLOW}Dry run — no files written. Would update {changes_made} layer(s).{RESET}")
        return 0

    target_path.write_text(target_content)
    print(f"\n{GREEN}Updated {changes_made} layer(s) in {target_path}{RESET}")
    return 0


# ─── Layer Info ──────────────────────────────────────────────────────────────


def cmd_info(args):
    """Show parsed layer info for debugging."""
    print(f"{BOLD}Kinesis Adv360 Pro:{RESET} {KINESIS_KEYMAP}")
    kinesis_layers, kinesis_defines = parse_keymap(KINESIS_KEYMAP)
    for name, layer in kinesis_layers.items():
        print(f"  {name}: {len(layer.bindings)} bindings")

    print(f"\n{BOLD}Glove80:{RESET} {GLOVE80_KEYMAP}")
    glove80_layers, glove80_defines = parse_keymap(GLOVE80_KEYMAP)
    for name, layer in glove80_layers.items():
        print(f"  {name}: {len(layer.bindings)} bindings")

    print(f"\n{BOLD}Shared layers:{RESET}")
    for logical, (k, g) in SHARED_LAYERS.items():
        k_found = "✓" if k in kinesis_layers else "✗"
        g_found = "✓" if g in glove80_layers else "✗"
        default = " (default sync)" if logical in DEFAULT_SYNC_LAYERS else ""
        print(f"  {logical}: Kinesis:{k} [{k_found}]  Glove80:{g} [{g_found}]{default}")

    return 0


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Sync shared layers between Kinesis Adv360 Pro and Glove80 ZMK keymaps.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # diff
    diff_parser = subparsers.add_parser("diff", help="Show differences in shared layers")
    diff_parser.add_argument(
        "-l", "--layers", nargs="+", help="Layers to compare (default: all syncable)"
    )

    # sync
    sync_parser = subparsers.add_parser("sync", help="Sync layers from one keyboard to another")
    sync_parser.add_argument(
        "--to",
        required=True,
        choices=["kinesis", "glove80"],
        help="Target keyboard to sync TO",
    )
    sync_parser.add_argument(
        "-l", "--layers", nargs="+", help="Layers to sync (default: nav_symbol, mouse*)"
    )
    sync_parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Show what would change without writing"
    )

    # info
    subparsers.add_parser("info", help="Show parsed keymap info")

    args = parser.parse_args()

    if args.command == "diff":
        return cmd_diff(args)
    elif args.command == "sync":
        return cmd_sync(args)
    elif args.command == "info":
        return cmd_info(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
