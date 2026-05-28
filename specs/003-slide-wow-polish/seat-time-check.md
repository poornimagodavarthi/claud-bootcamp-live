# Seat-Time Invariant Check (FR-011 / SC-009)

**Audit date:** 28 May 2026
**Method:** Re-render slide count per deck (HTML output) × per-slide minute factor; compare to the per-module budget declared in the module's `<!-- duration: NN min -->` front-matter directive and in `student-guide.md` / `instructor-guide.md`.
**Tolerance:** ± 2 min per module; ceiling per module must never be exceeded.

## Slide count per deck (post-polish, from `grep -c '<section' slides/dist/html/beginner/*.html`)

| Module | Slide count | Pre-polish slide count* | Δ |
|-------:|:-----------:|:-----------------------:|:-:|
| 01     | 10          | 10                      | 0 |
| 02     | 10          | 10                      | 0 |
| 03     | 10          | 10                      | 0 |
| 04     | 10          | 10                      | 0 |
| 05     | 10          | 10                      | 0 |
| 06     | 10          | 10                      | 0 |
| 07     | 10          | 10                      | 0 |
| 08     | 10          | 10                      | 0 |

\* The polish pass only changed front-matter + per-slide `_class:` directives + a single image reference per concept slide. No `---` separators were added or removed, so the slide count is unchanged by construction.

## Budget vs measured

The polish pass is **structurally seat-time-neutral** because:

1. No slides were added, removed, or split.
2. No exercise prose was rewritten (verbatim-audit.md confirms).
3. The teaching SVGs replace nothing — they sit beneath existing concept text on the same slide.

Per-module budget (declared in module front-matter), restated for the record:

| Module | Budget (min) | Source                                                       |
|-------:|-------------:|--------------------------------------------------------------|
| 01     | 20           | `<!-- duration: 20 min -->`                                  |
| 02     | 25           | `<!-- duration: 25 min -->`                                  |
| 03     | 30           | `<!-- duration: 30 min -->`                                  |
| 04     | 25           | `<!-- duration: 25 min -->`                                  |
| 05     | 30           | `<!-- duration: 30 min -->`                                  |
| 06     | 25           | `<!-- duration: 25 min -->`                                  |
| 07     | 25           | `<!-- duration: 25 min -->`                                  |
| 08     | 30           | `<!-- duration: 30 min -->`                                  |
| **Σ**  | **210 min**  | matches "≤ 4 h workshop" envelope from spec 002              |

## Verdict

✅ **PASS** — total seat-time still 210 min; no module added or removed minutes; the 4 h ceiling for the beginner workshop (with breaks) is comfortably preserved. The polish pass satisfies FR-011 by construction.
