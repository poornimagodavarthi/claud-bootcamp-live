#!/usr/bin/env bash
#
# check-contrast.sh — verify the wow-beginner palette tokens meet WCAG AA.
#
# WCAG 2.1 AA requires:
#   - Normal body text:   contrast ratio ≥ 4.5:1
#   - Large text (≥24px): contrast ratio ≥ 3.0:1
#   - Non-text UI parts:  contrast ratio ≥ 3.0:1
#
# Each row below pairs a foreground with the background it sits on in the
# wow-beginner theme, declares the minimum ratio for that role, and the script
# fails if any pair falls short.
#
# Algorithm: relative luminance per WCAG (sRGB → linear → Y), then
#   ratio = (L1 + 0.05) / (L2 + 0.05).
#
# Usage:  scripts/check-contrast.sh
# Exit 0 = all pairs pass.
# Exit 1 = at least one pair fails.
#
set -euo pipefail

python3 - <<'PY'
import sys

# Palette tokens (must match :root in slides/themes/wow-beginner.css)
P = {
    "bg":          "#FAF7F2",
    "ink":         "#1B1B1F",
    "muted":       "#5A5A66",
    "accent":      "#D9531E",
    "accent_soft": "#FCE6DA",
    "success":     "#1F7A4D",
    "danger":      "#9A2B2B",
}

def luminance(hex_color: str) -> float:
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (1, 3, 5))
    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    R, G, B = chan(r), chan(g), chan(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def ratio(fg: str, bg: str) -> float:
    L1, L2 = luminance(fg), luminance(bg)
    Lhi, Llo = max(L1, L2), min(L1, L2)
    return (Lhi + 0.05) / (Llo + 0.05)

# Pairs to check: (description, fg, bg, min_required, role)
checks = [
    ("Body text on background",          P["ink"],     P["bg"],          4.5, "AA normal"),
    ("Muted text on background",         P["muted"],   P["bg"],          4.5, "AA normal"),
    ("Accent text on background",        P["accent"],  P["bg"],          3.0, "AA large"),
    ("Accent text on accent-soft",       P["accent"],  P["accent_soft"], 3.0, "AA large"),
    ("Ink text on accent-soft",          P["ink"],     P["accent_soft"], 4.5, "AA normal"),
    ("Body text on ink (divider)",       P["bg"],      P["ink"],         4.5, "AA normal (dark)"),
    ("Accent text on ink (divider)",     P["accent"],  P["ink"],         3.0, "AA large (dark)"),
    ("Success text on background",       P["success"], P["bg"],          4.5, "AA normal"),
    ("Danger text on background",        P["danger"],  P["bg"],          4.5, "AA normal"),
]

ok = True
print("WCAG AA contrast check — wow-beginner palette")
print("-" * 70)
for desc, fg, bg, need, role in checks:
    r = ratio(fg, bg)
    status = "PASS" if r >= need else "FAIL"
    if r < need:
        ok = False
    print(f"{status}  {r:5.2f}:1  (need {need}:1, {role:18})  {desc}")
print("-" * 70)
if ok:
    print("OK: all palette pairs meet WCAG AA.")
    sys.exit(0)
else:
    print("FAIL: at least one palette pair is below the WCAG AA threshold.")
    sys.exit(1)
PY
