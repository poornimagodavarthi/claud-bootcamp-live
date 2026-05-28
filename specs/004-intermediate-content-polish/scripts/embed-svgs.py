#!/usr/bin/env python3
"""T048 — embed the per-module teaching SVG into the Concepts slide."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SVG_BY_MOD = {
    "01": "01-tcc-loop.svg",
    "02": "02-prompt-anatomy.svg",
    "03": "03-claude-md-cheatsheet.svg",
    "04": "04-bon-scoring.svg",
    "05": "05-test-debug-loop.svg",
    "06": "06-git-flow.svg",
    "07": "07-screenshot-to-ui.svg",
    "08": "08-refactor-constraints.svg",
    "09": "09-skills-catalogue.svg",
    "10": "10-five-axes.svg",
}

for deck in sorted(ROOT.glob("slides/part-*.md")):
    mod = re.search(r"part-(\d{2})", deck.name).group(1)
    svg = SVG_BY_MOD[mod]
    embed = f"![w:760](intermediate/assets/{svg})"
    text = deck.read_text()
    if embed in text:
        print(f"SKIP {deck.name} (already embedded)")
        continue
    # Insert just before the slide separator that closes the Concepts slide.
    m = re.search(r"(^## Concepts\n[\s\S]*?)(?=^---\n)", text, re.M)
    if not m:
        print(f"FAIL {deck.name}: Concepts section not found", file=sys.stderr); continue
    block = m.group(1).rstrip() + f"\n\n{embed}\n\n"
    text = text[:m.start()] + block + text[m.end():]
    deck.write_text(text)
    print(f"OK   {deck.name}  ← {svg}")
