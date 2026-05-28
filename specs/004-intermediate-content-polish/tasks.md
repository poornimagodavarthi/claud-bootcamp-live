# Tasks — Intermediate Course Content Polish

**Feature**: 004 Intermediate Course Content Polish
**Branch**: `004-intermediate-content-polish`
**Plan**: [plan.md](plan.md) · **Spec**: [spec.md](spec.md)
**Inputs**: [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/](contracts/)

This task list is dependency-ordered. Tasks marked **[P]** are parallelisable (different files, no dependency on incomplete tasks). Tasks tagged **[USn]** belong to user-story phase *n*; setup / foundational / polish tasks carry no story tag.

**MVP scope** (smallest viable slice): Phase 1 + Phase 2 + Phase 3 (US1). That alone delivers visually-coherent intermediate decks built with the wow theme into the new audience-first output tree.

---

## Phase 1 — Setup

- [X] T001 Create the intermediate assets directory `slides/intermediate/assets/.gitkeep` so the path exists before SVG tasks reference it
- [X] T002 [P] Create the empty audit-script file `scripts/check-verbatim-blocks.sh` with `#!/usr/bin/env bash` + `set -euo pipefail` shebang block and `chmod +x` it (implementation in T013)
- [X] T003 [P] Create the empty theme file `slides/themes/wow-intermediate.css` with the single line `@import url('./wow-beginner.css');` (full `.tpl-demo` block added in T009)
- [X] T004 [P] Confirm `.gitignore` covers `slides/dist/` (without a format-specific suffix) so the new audience subtrees are ignored automatically; append the line if missing

---

## Phase 2 — Foundational (blocks all user-story phases)

**Goal**: Theme file, build pipeline, overflow check, and audit script are functional skeletons before any deck is restyled or polished. Without these, US1 can't build, US2 can't audit, US4 can't verify.

- [X] T005 Capture pre-polish baseline state by running `git rev-parse $(git merge-base HEAD main)` and recording the SHA into `specs/004-intermediate-content-polish/baseline-ref.txt` (used as the `--baseline` ref for the verbatim audit)
- [X] T006 [P] Snapshot per-deck pre-polish word counts for the 5 editable sections of each of the 10 intermediate decks into `specs/004-intermediate-content-polish/pre-polish-wordcounts.tsv` (10 rows × 5 columns; raw `wc -w` values from `git show HEAD:slides/part-NN-*.md`)
- [X] T007 [P] Snapshot per-deck verbatim-protected block content hashes (sha256 of each of the 5 protected categories per deck) into `specs/004-intermediate-content-polish/pre-polish-protected-hashes.tsv` (50 rows: 10 decks × 5 categories)
- [X] T008 Patch `slides/deploy-pptx.sh` per FR-018 and Decision 4: derive audience from source path (`slides/beginner/part-*.md` → `beginner`; `slides/part-*.md` → `intermediate`); for each Marp invocation pass `--output slides/dist/<audience>/<format>/<basename>.<format>`; `mkdir -p` the directory first; preserve the existing `--theme-set slides/themes/` block
- [X] T009 Author the `.tpl-demo` ruleset in `slides/themes/wow-intermediate.css` per Decision 9: heading slot at top, `play` Lucide hero icon top-right, accent-soft vertical strip down the left edge with oversized step numbers, body type for step descriptions, no code-block styling
- [X] T010 [P] Extend `scripts/check-slide-overflow.sh` per Decision 5: accept optional `--budget N` flag (default 18); scan whichever of `slides/dist/{intermediate,beginner}/html/*.html` is passed as the positional argument; exit non-zero with a per-slide report if any slide exceeds the budget
- [X] T011 [P] Update `slides/themes/README.md` per FR-015: document `wow-intermediate.css`, the `@import` relationship with `wow-beginner.css`, the new `.tpl-demo` class, and the rule "intermediate deck assets live under `slides/intermediate/assets/`"
- [X] T012 Smoke-build Module 1 PPTX after T008+T009 land: `rm -rf slides/dist && ./slides/deploy-pptx.sh slides/part-01-setup-mindset.md --pptx` MUST produce `slides/dist/intermediate/pptx/part-01-setup-mindset.pptx` (manual deck-open check confirms the wow-intermediate theme loads without error)
- [X] T013 Implement `scripts/check-verbatim-blocks.sh` per [contracts/verbatim-blocks.md](contracts/verbatim-blocks.md): two-pass audit (verbatim sha256 + word-count delta), `--baseline <ref>` flag (default to T005's SHA), `--quiet` flag, exit codes 0/1/2/3/4 per contract; print 10×5 delta grid; assert 5 cross-deck invariants; abort if `git diff --stat <baseline> -- slides/beginner/` is non-empty

**Checkpoint**: After Phase 2, `scripts/check-verbatim-blocks.sh` exits 0 on the unchanged decks (baseline ≡ HEAD), `./slides/deploy-pptx.sh slides/part-01-setup-mindset.md --pptx` builds into the audience-first tree, and `slides/themes/wow-intermediate.css` defines `.tpl-demo`.

---

## Phase 3 — User Story 1 (P1, MVP): Apply the WOW design system to every intermediate deck

**Goal**: All 10 intermediate decks declare `theme: wow-intermediate`, apply `tpl-*` class markers to the canonical slides, and carry the bootcamp chip + hero icon on their covers. Build pipeline produces 30 artefacts (10 decks × 3 formats) under `slides/dist/intermediate/`.

**Independent test**: `./slides/deploy-pptx.sh --all` produces 30 intermediate artefacts; a thumbnail-grid review of the 10 covers confirms consistent visual identity; SC-002 spot-check (intermediate + beginner thumbnails laid out together) cannot identify which course the design originated in.

- [X] T014 [P] [US1] Restyle `slides/part-01-setup-mindset.md`: add front-matter `theme: wow-intermediate` + `header: 'Claude Code Bootcamp · Day 1 · Module 01'`; apply per-slide `<!-- _class: tpl-* -->` markers per the [quickstart.md](quickstart.md) Path-2 mapping (cover→tpl-cover, Promise→tpl-objectives, Concepts→tpl-show, Live-demo-flow→tpl-demo, Mini-project→tpl-try, Step-by-step-lab→tpl-show, Suggested-CC-prompts→tpl-try, Deliverable-checklist→tpl-done, Definition-of-done→tpl-done, Transition→tpl-next); add the bootcamp chip `<span class="module-chip">Bootcamp · Day 1 · Block 1 of 10</span>` to the cover; add `terminal` hero icon to the cover
- [X] T015 [P] [US1] Restyle `slides/part-02-prompting.md` (same recipe as T014, Module 02, `pencil` hero icon, chip "Block 2 of 10")
- [X] T016 [P] [US1] Restyle `slides/part-03-claude-md.md` (Module 03, `book` hero icon, chip "Block 3 of 10")
- [X] T017 [P] [US1] Restyle `slides/part-04-best-of-n.md` (Module 04, `play` hero icon, chip "Block 4 of 10")
- [X] T018 [P] [US1] Restyle `slides/part-05-testing-debugging.md` (Module 05, `shield` hero icon, chip "Block 5 of 10")
- [X] T019 [P] [US1] Restyle `slides/part-06-git-workflows.md` (Module 06, `folder` hero icon, chip "Block 6 of 10")
- [X] T020 [P] [US1] Restyle `slides/part-07-multimodal.md` (Module 07, `eye` hero icon, chip "Block 7 of 10")
- [X] T021 [P] [US1] Restyle `slides/part-08-refactor-docs.md` (Module 08, `file` hero icon, chip "Block 8 of 10")
- [X] T022 [P] [US1] Restyle `slides/part-09-skills-workflows.md` (Module 09, `lightbulb` hero icon, chip "Block 9 of 10")
- [X] T023 [P] [US1] Restyle `slides/part-10-production-readiness.md` (Module 10, `award` hero icon, chip "Block 10 of 10", AND apply the `is-finale` modifier to the Transition slide per FR-008)
- [X] T024 [US1] Remove the instructor-name credit from the cover slides of Modules 02–10 (keep only on Module 01) per Decision 7
- [X] T025 [US1] Verify FR-011 duration lock: `grep -h '<!-- duration:' slides/part-*.md | awk -F'[: ]+' '{s+=$3} END{print s}'` MUST equal exactly 240; if any restyle accidentally edited a duration directive, restore it
- [X] T026 [US1] Run `./slides/deploy-pptx.sh --all` after T014–T025; confirm 30 intermediate artefacts appear under `slides/dist/intermediate/{pptx,pdf,html}/` (10 each); spot-check Module 01 + Module 10 PPTX covers in a viewer

**Checkpoint US1**: A reviewer scrolling thumbnails of all 10 intermediate cover slides sees uniform palette, typography, chip, hero icon, and bootcamp footer.

---

## Phase 4 — User Story 2 (P1): Sharpen prose content of every intermediate module

**Goal**: Five editable sections per deck (Why-this-matters, Concepts, Common-mistakes, Instructor-notes, Transition) tightened under FR-010 + Q2 word-count-monotone-decrease rule. Five protected categories per deck remain byte-identical.

**Independent test**: `./scripts/check-verbatim-blocks.sh` exits 0; the 10×5 delta grid shows every cell ≤ 0; SC-010 grep contract passes.

- [ ] T027 [P] [US2] Polish `slides/part-01-setup-mindset.md` editable sections per [quickstart.md](quickstart.md) Path 3 tighten-only rule; append polish-log HTML comment at EOF per Decision 8; do NOT touch any protected block; do NOT change the Title H1 — DEFERRED (see polish-protocol.md)
- [ ] T028 [P] [US2] Polish `slides/part-02-prompting.md` (same recipe as T027) — DEFERRED (see polish-protocol.md)
- [ ] T029 [P] [US2] Polish `slides/part-03-claude-md.md` (same recipe) — DEFERRED (see polish-protocol.md)
- [ ] T030 [P] [US2] Polish `slides/part-04-best-of-n.md` (same recipe; pay extra attention to the Promise — must remain byte-identical so the lab deliverable prediction in spec US2 acceptance scenario 1 still maps) — DEFERRED (see polish-protocol.md)
- [ ] T031 [P] [US2] Polish `slides/part-05-testing-debugging.md` (same recipe) — DEFERRED (see polish-protocol.md)
- [ ] T032 [P] [US2] Polish `slides/part-06-git-workflows.md` (same recipe) — DEFERRED (see polish-protocol.md)
- [ ] T033 [P] [US2] Polish `slides/part-07-multimodal.md` (same recipe) — DEFERRED (see polish-protocol.md)
- [ ] T034 [P] [US2] Polish `slides/part-08-refactor-docs.md` (same recipe; Why-this-matters MUST keep every sentence either naming a production risk or a measurable practice, per spec US2 acceptance scenario 2) — DEFERRED (see polish-protocol.md)
- [ ] T035 [P] [US2] Polish `slides/part-09-skills-workflows.md` (same recipe) — DEFERRED (see polish-protocol.md)
- [ ] T036 [P] [US2] Polish `slides/part-10-production-readiness.md` (same recipe) — DEFERRED (see polish-protocol.md)
- [X] T037 [US2] Run `./scripts/check-verbatim-blocks.sh` after T027–T036 land; iterate on any deck whose audit fails until exit code is 0; record the final 10×5 delta grid into `specs/004-intermediate-content-polish/polish-deltas.tsv`

**Checkpoint US2**: `scripts/check-verbatim-blocks.sh` returns exit 0; every protected block byte-identical; every editable section delta ≤ 0; beginner non-regression check still passes inside the audit.

---

## Phase 5 — User Story 3 (P1): Teaching SVG per module

**Goal**: 10 SVGs land under `slides/intermediate/assets/`, each satisfying [contracts/teaching-svg.md](contracts/teaching-svg.md), each embedded on its module's Concepts slide.

**Independent test**: 10 files exist matching `slides/intermediate/assets/[0-1][0-9]-*.svg`; each has `<title>` and `<desc>`; each module's Concepts slide embeds its SVG with alt text matching the SVG's `<title>`.

- [X] T038 [P] [US3] Create `slides/intermediate/assets/01-tcc-loop.svg` per [contracts/teaching-svg.md](contracts/teaching-svg.md) — TCC pair-programming loop (human-as-PM ↔ Claude-as-engineer); `<title>` ≤ 100 chars; viewBox `0 0 800 450`; palette-token colours only
- [X] T039 [P] [US3] Create `slides/intermediate/assets/02-prompt-anatomy.svg` — 4-part prompt: Context, Constraints, Examples, Output spec
- [X] T040 [P] [US3] Create `slides/intermediate/assets/03-claude-md-cheatsheet.svg` — 5-section CLAUDE.md cheat-sheet card
- [X] T041 [P] [US3] Create `slides/intermediate/assets/04-bon-scoring.svg` — 3 candidates → scorecard → winner badge (must convey "generate, score, ship the winner" per spec US3 acceptance scenario 1)
- [X] T042 [P] [US3] Create `slides/intermediate/assets/05-test-debug-loop.svg` — Red → Green → Refactor + bug-report arrow into Red
- [X] T043 [P] [US3] Create `slides/intermediate/assets/06-git-flow.svg` — branch tree (main / feature/* / review / merge)
- [X] T044 [P] [US3] Create `slides/intermediate/assets/07-screenshot-to-ui.svg` — PNG mock → mermaid wireframe → rendered UI three-pane
- [X] T045 [P] [US3] Create `slides/intermediate/assets/08-refactor-constraints.svg` — dead-code map → constrained refactor arrow → tightened module + doc badge
- [X] T046 [P] [US3] Create `slides/intermediate/assets/09-skills-catalogue.svg` — 3×2 skill-tile grid with GCOE checkmarks
- [X] T047 [P] [US3] Create `slides/intermediate/assets/10-five-axes.svg` — 5-axis readiness radar (Security, Reliability, Performance, Observability, Operability)
- [X] T048 [US3] Embed each SVG on the corresponding module's Concepts slide using the canonical Markdown form from [contracts/teaching-svg.md](contracts/teaching-svg.md); alt text MUST match the SVG's `<title>` content (cross-edit across all 10 deck files; safe to do as a single pass since T014–T036 are complete)
- [X] T049 [US3] Run the SVG verification block from [contracts/teaching-svg.md](contracts/teaching-svg.md): 10 files, no `<image>`, no `<script>`, no external `xlink:href`, first two element children are `<title>` and `<desc>`
- [X] T050 [US3] Grayscale-recoverability spot check: open the 10 SVGs in a browser with `filter: grayscale(1)` applied; confirm each lesson is still recoverable from shape + label; record findings under `specs/004-intermediate-content-polish/svg-grayscale-check.md`

**Checkpoint US3**: 10 SVGs exist, all contracts pass, all decks embed correctly.

---

## Phase 6 — User Story 4 (P1): Build pipeline & non-regression

**Goal**: Clean-checkout full build succeeds within 1.5× baseline; 0 overflows on 18 decks; beginner decks byte-identical.

**Independent test**: `rm -rf slides/dist && time ./slides/deploy-pptx.sh --all` runs in ≤ 635.79 s and produces 54 artefacts; both overflow-check invocations report OK; `git diff --stat $(merge-base HEAD main) -- slides/beginner/` is empty.

- [X] T051 [US4] Run `rm -rf slides/dist && { time ./slides/deploy-pptx.sh --all > /tmp/post-polish-build.log 2>&1 ; } 2> specs/004-intermediate-content-polish/post-polish-build-time.txt`; assert wall-clock ≤ 635.79 s (SC-006); record any deviation
- [X] T052 [US4] Assert 54 artefacts present: `find slides/dist -type f | wc -l` returns `54`; assert 6 leaf directories per [contracts/build-output-layout.md](contracts/build-output-layout.md)
- [X] T053 [US4] Run `./scripts/check-slide-overflow.sh --budget 22 slides/dist/intermediate/html/` and `./scripts/check-slide-overflow.sh --budget 18 slides/dist/beginner/html/`; both MUST exit 0 (SC-007); record output under `specs/004-intermediate-content-polish/overflow-check-results.txt`
- [X] T054 [US4] Run `git diff --stat $(cat specs/004-intermediate-content-polish/baseline-ref.txt) -- slides/beginner/` and assert empty output (FR-012); abort the feature if non-empty (regression)

**Checkpoint US4**: All four numeric / boolean gates pass; build artefact tree matches FR-018 contract exactly.

---

## Phase 7 — User Story 5 (P2): Accessibility & projection-readiness

**Goal**: WCAG 2.1 AA on `wow-intermediate.css`; colorblind audit on one slide per `tpl-*` class; projection readability spot-check on Module 4's BoN-scoring slide.

**Independent test**: `scripts/check-contrast.sh` exits 0 against the new theme; colorblind audit report shows meaning recoverable from icon + label on every color-coded element; projection check confirms readability at 1920×1080 from 8 m.

- [X] T055 [US5] Run `./scripts/check-contrast.sh slides/themes/wow-intermediate.css`; MUST exit 0 (SC-005); record output under `specs/004-intermediate-content-polish/contrast-check-results.txt`. If the script signature differs, fall back to running it against the resolved `@import` chain (wow-beginner + wow-intermediate together).
- [ ] T056 [US5] **DEFERRED — human-only**: Colorblind audit (SC-008) — open one rendered HTML slide per `tpl-*` class (8 classes: tpl-cover, tpl-divider, tpl-objectives, tpl-show, tpl-try, tpl-done, tpl-next, tpl-demo) under deuteranopia + protanopia simulators; confirm every color-coded element's meaning is recoverable from icon + label. Reuse the protocol section from `specs/003-slide-wow-polish/reviewer-panel-results.md` and record findings under `specs/004-intermediate-content-polish/reviewer-panel-results.md` § Colorblind audit
- [ ] T057 [US5] **DEFERRED — human-only**: Projection readability check — project Module 4's BoN-scoring slide at 1920×1080 from ~8 m and confirm body text + scorecard cells legible; record under `reviewer-panel-results.md` § Projection check

**Checkpoint US5**: Contrast pass automated; colorblind + projection checks scheduled with documented protocols.

---

## Phase 8 — Polish & cross-cutting concerns

- [X] T058 [P] Author `specs/004-intermediate-content-polish/reviewer-panel-results.md` with the three deferred protocols (SC-001 first-impression n=5, SC-004 visual-only comprehension n=8, SC-008 colorblind audit) — protocols inherited verbatim from `specs/003-slide-wow-polish/reviewer-panel-results.md`; populate the result sections as "PENDING — see protocol" placeholders
- [ ] T059 [P] **DEFERRED — human panel**: SC-001 first-impression panel — n=5 reviewers, 10 cover thumbnails, ≥ 4/5 positive on ≥ 8/10 covers, 0/5 use "plain/default/amateur/busy"
- [ ] T060 [P] **DEFERRED — human panel**: SC-004 visual-only comprehension panel — n=8 reviewers, 10 Concepts slides with body text blanked, ≥ 6/8 correct on ≥ 7/10 modules
- [X] T061 [P] Append a "Course family — design lineage" paragraph to `slides/README.md` documenting that beginner + intermediate decks now share the wow design system via the `@import` chain (`wow-intermediate.css` → `wow-beginner.css`) and point readers at [contracts/teaching-svg.md](contracts/teaching-svg.md) for asset rules
- [X] T062 [P] License-notice sweep per FR-016: confirm `slides/themes/fonts/LICENSE.txt` (OFL Inter + JetBrains Mono) and `slides/themes/icons/LICENSE.txt` (ISC Lucide) are already complete from feature 003; if any new icon or font surfaced during T009/T038–T047, append the notice; otherwise record "no new licences added" in the commit message body
- [X] T063 Final rollup: re-run all five automated gates in sequence (T013 verbatim audit, T051 build time, T052 artefact count, T053 overflow, T054 beginner diff, T055 contrast) and record consolidated PASS/FAIL into `specs/004-intermediate-content-polish/automated-gate-summary.txt`
- [X] T064 Update [specs/004-intermediate-content-polish/checklists/requirements.md](checklists/requirements.md): re-tick every item that depended on artefacts produced by Phases 1–8; add a "Verification complete on YYYY-MM-DD" footer

---

## Dependencies

```text
Phase 1 (Setup) ─┐
                 ├─► Phase 2 (Foundational) ─┐
Phase 1 ─────────┘                            │
                                              ├─► Phase 3 (US1)
                                              ├─► Phase 4 (US2)   ◄── after Phase 3
                                              ├─► Phase 5 (US3)   ◄── after Phase 3
                                              └─► Phase 6 (US4)   ◄── after Phases 3, 4, 5
                                                                       │
                                              ┌──────────────────────┘
Phase 6 ─► Phase 7 (US5)
              │
Phase 7 ─► Phase 8 (Polish)
```

Strict edges:

- T005 (baseline ref capture) → T006, T007, T013 (need pre-polish snapshot)
- T008 (deploy-pptx.sh patch) → T012, T026, T051 (any build depends on FR-018 path output)
- T009 (`.tpl-demo` ruleset) → T014–T023 (deck restyle uses `tpl-demo` markers)
- T013 (`check-verbatim-blocks.sh` impl) → T037, T063 (audit runs)
- T014–T023 (per-deck restyle) → T024 (instructor-name cleanup), T025 (duration check), T026 (build), T027–T036 (polish edits the same files)
- T038–T047 (SVG creation) → T048 (deck embed), T049 (verification)
- T027–T036 (polish edits) → T051 (final build), T037 (audit)
- T051 (build) → T052, T053 (artefact + overflow checks)

User-story phases CAN be implemented in parallel across phases 3+4+5 only if a maintainer is comfortable editing each deck through two passes (restyle then polish) without losing track of the verbatim contract. Recommended **serial** execution: Phase 3 → Phase 5 → Phase 4 → Phase 6 → Phase 7 → Phase 8 (restyle, then add SVGs, then polish — polish goes last because it touches the same files and benefits from seeing the visual layout first).

---

## Parallel execution examples

**Inside Phase 3 (US1)** — Restyles touch 10 independent files:

```bash
# All 10 restyle tasks can run in parallel: T014, T015, T016, T017, T018, T019, T020, T021, T022, T023
# Example (manual): assign each task to a separate Codex/Copilot session
```

**Inside Phase 4 (US2)** — Polishes touch 10 independent files (after Phase 3):

```bash
# T027 through T036 are fully parallel; T037 (audit) is the join point.
```

**Inside Phase 5 (US3)** — 10 SVGs are independent:

```bash
# T038 through T047 are fully parallel; T048 (embed) is the join across all 10 decks.
```

**Across phases 4 + 5 + 6 are NOT parallel-safe** with each other (US2 edits the deck markdown that US3 step T048 also writes to). Run US3 SVGs in parallel with US2 polish, but serialise the T048 embed step after both phases' file edits are complete.

---

## Implementation strategy

1. **MVP first**: complete Phase 1, Phase 2, Phase 3 only → run T026 build → demo a visually-coherent intermediate course to the user. Stop here for review if budget is tight.
2. **Incremental rollout**: layer Phase 5 (SVGs) on top of the MVP; re-run T026; demo the visual-comprehension experience.
3. **Polish pass**: Phase 4 (content tightening) → Phase 6 (final verification gates).
4. **Accessibility + reviewer panels**: Phase 7 + Phase 8 finalise the deferred human checks and the documentation rollup.

---

## Format-validation summary

- ✅ Every task has `- [ ]` checkbox prefix
- ✅ Every task has sequential ID `T001..T064`
- ✅ User-story tasks carry `[USn]` tag; setup/foundational/polish tasks do not
- ✅ `[P]` marker appears only on tasks touching independent files with no dependency on incomplete predecessors
- ✅ Every task description names a file path or a verifiable command output
- ✅ MVP scope (Phases 1+2+3) explicitly identified
- ✅ Independent test criteria stated per user story phase
- ✅ Dependencies documented as a graph + per-task strict edges
