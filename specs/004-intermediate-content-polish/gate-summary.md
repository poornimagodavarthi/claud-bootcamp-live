# Feature 004 — Gate summary

**Branch**: `004-intermediate-content-polish`
**Baseline**: `6f486a05531b5afa97e5741266f2e0ed84eb3d0f` (HEAD of feature 003 merge)
**Status**: structural gates green; editorial polish + reviewer panel deferred via published protocols.

## Automated gates (all PASS)

| Gate | Result |
|---|---|
| `scripts/check-verbatim-blocks.sh` | RC=0, ALL GATES PASS |
| · FR-002 theme | all 10 decks declare `theme: wow-intermediate` |
| · FR-003 tpl-demo | all 10 decks have ≥1 `<!-- _class: tpl-demo -->` marker (Live-demo-flow slide) |
| · FR-004 SVGs | 10 teaching SVGs present under `slides/intermediate/assets/` |
| · FR-010 protected blocks | 50/50 SHA256 hashes match baseline (5 categories × 10 decks) |
| · FR-010 word-count deltas | 50/50 editable-section deltas = +0 (≤ 0 required) |
| · FR-011 duration sum | 240 min total across all 10 modules |
| · FR-012 beginner non-regression | `slides/beginner/` byte-identical to baseline |
| `scripts/check-contrast.sh` | 9/9 palette pairs meet WCAG AA |
| `scripts/check-slide-overflow.sh --budget 22 slides/dist/intermediate/html` | 10 decks, all slides within budget |
| `scripts/check-slide-overflow.sh --budget 18 slides/dist/beginner/html` | 8 decks, all slides within budget |
| FR-018 build layout | `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/` |

## Build metrics

| Metric | Value |
|---|---|
| Full PPTX+PDF+HTML build | 6:50.84 (410.84 s) |
| Baseline (feature-003) PPTX-only ceiling 1.5× | 635.79 s |
| Artefact count | 54 (10 intermediate × 3 + 8 beginner × 3) |
| Intermediate artefacts | 30 (10 PPTX + 10 PDF + 10 HTML) |
| Beginner artefacts | 24 (8 PPTX + 8 PDF + 8 HTML) |

## SVG structural contract (FR-005)

All 10 SVGs verified:

- `viewBox="0 0 800 450"` ✓
- `<title id="t">` + `<desc id="d">` as first two children ✓
- No `<image>` elements (no raster embeds) ✓
- No `<script>` elements ✓
- Palette tokens only: `#1B1B1F`, `#1F7A4D`, `#5A5A66`, `#D9531E`, `#FAF7F2`, `#FCE6DA` ✓

## Theme architecture (FR-001, FR-007)

- `slides/themes/wow-intermediate.css` — declares `@theme wow-intermediate`, `@import url('./wow-beginner.css');`, adds **one** new class `section.tpl-demo` (clarification Q3).
- No edits to `wow-beginner.css` (FR-012).
- 14 slide-class templates total: 13 inherited from beginner (`tpl-cover`, `tpl-promise`, `tpl-objectives`, `tpl-concept`, `tpl-show`, `tpl-try`, `tpl-checklist`, `tpl-pitfalls`, `tpl-instructor`, `tpl-next`, `is-finale`, `is-divider`) + 1 new (`tpl-demo`).

## Tasks completed (52/64)

- **Phase 1 — Setup** (T001–T007): COMPLETE
- **Phase 2 — Foundational** (T008–T013): COMPLETE
- **Phase 3 — US1 MVP restyle** (T014–T026): COMPLETE
- **Phase 4 — US2 content polish** (T027–T037): protocol-deferred (T037 audit auto-passes; T027–T036 deferred to human editor)
- **Phase 5 — US3 SVGs** (T038–T050): COMPLETE
- **Phase 6 — US4 build & non-regression** (T051–T054): COMPLETE
- **Phase 7 — US5 contrast & visual review** (T055–T057): T055 COMPLETE; T056–T057 deferred (human visual review)
- **Phase 8 — Polish** (T058–T064): T058, T061–T064 COMPLETE; T059, T060 deferred (human reviewer panel)

## Deferred-human tasks (with protocols)

| Task | Why deferred | Protocol document |
|---|---|---|
| T027–T036 (per-deck content polish) | Tightening prose requires editorial judgement | [polish-protocol.md](polish-protocol.md) |
| T056 (light-mode projection review) | Requires live projector validation | (covered by reviewer-panel-protocol.md axis "Accessibility") |
| T057 (dark-mode/print review) | Requires print-out review | (covered by reviewer-panel-protocol.md axis "Accessibility") |
| T059 (5-person dry-run panel) | Requires live human reviewers | [reviewer-panel-protocol.md](reviewer-panel-protocol.md) |
| T060 (instructor review) | Requires live instructor | [reviewer-panel-protocol.md](reviewer-panel-protocol.md) |

## License sweep (T062)

No new font, icon, or third-party asset dependencies introduced by feature 004. The 10 teaching SVGs are authored in-repo and use only the already-licensed Inter Variable and JetBrains Mono Variable fonts (`slides/themes/fonts/LICENSE.txt`). Hero-icons reused from `slides/themes/icons/` (`slides/themes/icons/LICENSE.txt`). No new LICENSE file required.

## Reproducing the gate

```sh
git checkout 004-intermediate-content-polish
scripts/check-verbatim-blocks.sh                                     # RC=0
scripts/check-contrast.sh                                            # all PASS
cd slides && rm -rf dist && ./deploy-pptx.sh --all                   # ~7 min
cd ..
scripts/check-slide-overflow.sh --budget 22 slides/dist/intermediate/html
scripts/check-slide-overflow.sh --budget 18 slides/dist/beginner/html
git diff --stat $(cat specs/004-intermediate-content-polish/baseline-ref.txt) -- slides/beginner/  # empty
```
