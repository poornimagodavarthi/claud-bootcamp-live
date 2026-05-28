# Contract — Teaching SVG

**Feature**: 004 Intermediate Course Content Polish
**Consumers**: SVG authors, the verbatim-block audit script (asset-count assertion), human reviewers running the SC-004 visual-only comprehension panel.

This contract defines the structural, accessibility, and palette requirements for every intermediate teaching visual. It is satisfied by 10 SVG files under `slides/intermediate/assets/`.

---

## File-naming contract

```text
slides/intermediate/assets/<NN>-<lesson-slug>.svg
```

| Segment | Rule |
|---|---|
| `<NN>` | Two-digit zero-padded module number (01 through 10). |
| `<lesson-slug>` | Kebab-case noun phrase naming the visual's central concept (≤ 32 chars). |
| extension | `.svg` (lowercase). |

Canonical 10:

| Module | Filename | Concept |
|---|---|---|
| 01 | `01-tcc-loop.svg` | Human-as-PM ↔ Claude-as-engineer loop |
| 02 | `02-prompt-anatomy.svg` | 4-part prompt: Context, Constraints, Examples, Output spec |
| 03 | `03-claude-md-cheatsheet.svg` | 5-section CLAUDE.md card |
| 04 | `04-bon-scoring.svg` | 3 candidates → scorecard → winner badge |
| 05 | `05-test-debug-loop.svg` | Red → Green → Refactor with bug-report arrow into Red |
| 06 | `06-git-flow.svg` | Branch tree: main / feature/* / review / merge |
| 07 | `07-screenshot-to-ui.svg` | PNG mock → mermaid wireframe → rendered UI |
| 08 | `08-refactor-constraints.svg` | Dead-code map → constrained-refactor arrow → tightened module + doc badge |
| 09 | `09-skills-catalogue.svg` | 3×2 skill tile grid with GCOE checkmarks |
| 10 | `10-five-axes.svg` | 5-axis readiness radar (Security, Reliability, Performance, Observability, Operability) |

---

## Structural contract

Every SVG file MUST:

1. Start with the XML declaration: `<?xml version="1.0" encoding="UTF-8"?>`.
2. Root element `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="100%" height="auto">`.
3. As the first two children of `<svg>`, exactly one `<title>` and exactly one `<desc>` element (a11y contract).
4. Use only the following element types: `<g>`, `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polyline>`, `<polygon>`, `<path>`, `<text>`, `<tspan>`, `<defs>`, `<marker>`, `<use>`, `<symbol>`.
5. NOT contain any `<image>` element (FR-005 — no embedded rasters).
6. NOT contain any `<script>` element.
7. NOT contain any external `xlink:href` (no cross-file references).

The XML MUST validate against the SVG 1.1 schema.

---

## Accessibility contract

The `<title>` text MUST be:

- A single sentence ending with a period.
- ≤ 100 characters.
- A complete statement of the visual's lesson (e.g., "The Best-of-N flow: generate three candidates, score them against the rubric, ship the winner.").

The `<desc>` text MUST be:

- 1–4 sentences, separated by single spaces.
- ≤ 400 characters total.
- A screen-reader-friendly walkthrough of the visual's structure ("Three candidate folders on the left labelled A, B, C. Each connects via an arrow to a centered scorecard table with five rows. The scorecard's top row is highlighted and connects via a final arrow to a winner badge on the right.").

---

## Palette contract

Every `fill=`, `stroke=`, and `style="…"` colour-bearing attribute MUST be one of:

| Allowed value | Source |
|---|---|
| `none` | — |
| `currentColor` | — |
| One of the 8 hex literals from the wow palette | `#FAF7F2`, `#1B1B1F`, `#5A5A66`, `#D9531E`, `#FCE6DA`, `#1F7A4D`, `#9A2B2B`, `#E7E1D6` |
| `var(--bg)` `var(--ink)` `var(--muted)` `var(--accent)` `var(--accent-soft)` `var(--success)` `var(--danger)` `var(--rule)` | matches palette tokens declared in wow-beginner.css |

Any other colour value (named CSS colours, RGB/HSL functions, opacity-bearing hex like `#ff0000aa`) is a contract violation.

---

## Typography contract

Every `<text>` element MUST:

- Declare `font-family="Inter Variable, system-ui, sans-serif"` (matches deck body type) OR `font-family="JetBrains Mono Variable, ui-monospace, monospace"` (matches deck code type — use only when the visual depicts code or a path).
- Use `font-size` in the range 14–32 (visual hierarchy: 14 for annotations, 18 for labels, 22 for term names, 28–32 for the single hero label if any).
- Use `fill=` from the palette contract above.

No external font references; the deck inherits the bundled Inter + JetBrains Mono Variable fonts from `slides/themes/fonts/`.

---

## Grayscale-recoverability contract

When the SVG is rendered through a grayscale filter, every information-bearing distinction MUST remain detectable. Concretely:

- Distinct entities MUST be distinguishable by shape, position, or label — never by hue alone.
- Status indicators (success/warning/danger) MUST pair the colour with an icon AND a label (echoes FR-006).
- Arrow direction MUST be conveyed by the marker, not by colour.

This is verified during the SC-008 colorblind audit; the protocol simulates deuteranopia + protanopia + grayscale.

---

## Embedding contract (in the deck markdown)

Every intermediate deck MUST embed its SVG on the Concepts slide using exactly this Markdown form:

```markdown
![<a11y label matching the SVG <title>](intermediate/assets/<NN>-<slug>.svg)
```

Examples:

```markdown
![The TCC pair-programming loop: human-as-PM hands a goal to Claude-as-engineer, who returns code; human reviews and merges.](intermediate/assets/01-tcc-loop.svg)
```

The alt text MUST match the SVG's `<title>` content (one source of truth for the lesson statement).

---

## Verification

```bash
# 1. Exactly 10 SVGs exist with correct names
ls slides/intermediate/assets/[0-1][0-9]-*.svg | wc -l   # expect 10

# 2. Every SVG has <title> and <desc> as the first two element children
for f in slides/intermediate/assets/*.svg; do
  python3 -c "
import xml.etree.ElementTree as ET, sys
ns = '{http://www.w3.org/2000/svg}'
root = ET.parse('$f').getroot()
kids = [c.tag for c in root if isinstance(c.tag, str)]
assert kids[:2] == [ns+'title', ns+'desc'], '$f missing title/desc'
"
done

# 3. No <image>, no <script>, no external xlink:href
grep -lE '<image|<script|xlink:href' slides/intermediate/assets/*.svg
# expect: no output

# 4. Every colour value is in the allowed palette
# (manual audit; the script lives in scripts/check-svg-palette.sh once authored)

# 5. Every deck embeds its SVG with the canonical alt-text form
for n in 01 02 03 04 05 06 07 08 09 10; do
  grep -l "intermediate/assets/${n}-" slides/part-${n}-*.md
done | wc -l   # expect 10
```

All five assertions MUST pass. They support FR-004 + FR-005 + SC-004.
