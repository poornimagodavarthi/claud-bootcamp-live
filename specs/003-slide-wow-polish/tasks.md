---
description: "Task list for feature 003-slide-wow-polish"
---

# Tasks: Slide Decks That Shine — Visual & Pedagogical Polish Pass

**Input**: Design documents from [specs/003-slide-wow-polish/](.)

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts)

**Tests**: NOT explicitly requested in the spec. Test tasks are therefore omitted. **Automated verification scripts** ( `scripts/check-slide-overflow.sh`, `scripts/check-contrast.sh` ) are still included — they are explicit acceptance instruments named in plan.md / research.md / data-model.md, not unit tests.

**Organization**: Tasks grouped by user story (US1 – US5) to enable independent implementation and demo.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Different file, no dependency on incomplete tasks → safe to parallelize.
- **[Story]**: maps to a User Story in spec.md (US1, US2, US3, US4, US5). Omitted on Setup, Foundational, and Polish phases.

## Path Conventions

Content/docs feature. Paths are relative to repo root: [slides/](../../slides), [scripts/](../../scripts), [specs/003-slide-wow-polish/](.).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory scaffolding and capture the pre-polish baseline.

- [ ] T001 Create directory `slides/themes/` with subfolders `fonts/` and `icons/` (`mkdir -p slides/themes/fonts slides/themes/icons`).
- [ ] T002 Create directory `slides/beginner/assets/` (`mkdir -p slides/beginner/assets`).
- [ ] T003 Record the **pre-polish build-time baseline**: run `time ./slides/deploy-pptx.sh --all` on a clean checkout from `main` (or pre-feature commit) and save the wall-clock seconds to `specs/003-slide-wow-polish/baseline-build-time.txt` (one number, plus a one-line note: machine, Marp version, date). Required for SC-006 verification.
- [ ] T004 [P] Add the bundled OFL fonts (download once, commit binary): `slides/themes/fonts/Inter-Variable.woff2` (Latin subset) and `slides/themes/fonts/JetBrainsMono-Variable.woff2` (Latin subset). Each ≤ ~150 KB.
- [ ] T005 [P] Add the SIL OFL 1.1 license text covering both font families: `slides/themes/fonts/LICENSE.txt` (verbatim OFL 1.1 + copyright lines for Rasmus Andersson / The Inter Project / JetBrains).
- [ ] T006 [P] Add the 13 Lucide icons (ISC) as individual SVG files under `slides/themes/icons/`: `terminal.svg`, `lightbulb.svg`, `shield.svg`, `warning.svg`, `check.svg`, `play.svg`, `pencil.svg`, `eye.svg`, `book.svg`, `file.svg`, `folder.svg`, `arrow-right.svg`, `award.svg`. Source from `https://github.com/lucide-icons/lucide` (pinned commit; download once, commit). All MUST share stroke-width 1.75 per data-model §IconSet.
- [ ] T007 [P] Add the ISC license text for Lucide: `slides/themes/icons/LICENSE.txt` (verbatim ISC + Lucide copyright line + pinned commit SHA used for the 13 icons).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The design system + build-pipeline change that every user story depends on.

**⚠️ CRITICAL**: No user-story work may begin until this phase is complete.

- [ ] T008 Author the Marp custom theme `slides/themes/wow-beginner.css`. Declarations required (per data-model §DesignSystem and §Palette / §TypographyPair and §SlideTemplate): `/* @theme wow-beginner */` header pointing `@import url('default')` as fallback; `@font-face` for Inter Variable and JetBrains Mono Variable using relative paths `./fonts/...`; CSS custom properties for the full palette (`--bg`, `--ink`, `--muted`, `--accent`, `--accent-soft`, `--success`, `--danger`); base typography rules (h1 56 px, h2 40 px, h3 32 px, body 28 px Inter, code 22 px JetBrains Mono, line-heights per data-model); section classes `.tpl-cover`, `.tpl-divider`, `.tpl-objectives`, `.tpl-show`, `.tpl-try`, `.tpl-done`, `.tpl-next`; footer + paginate styling (course name + module number + page number); global page-margins / safe-area for 16:9.
- [ ] T009 Write `slides/themes/README.md` documenting the design system per FR-014: how to apply (`theme: wow-beginner` in front-matter), what each `.tpl-*` class slot expects, the full palette token table, the typography pair + fallbacks, the icon inventory, and the "things forbidden" list from [contracts/slide-template-contracts.md](contracts/slide-template-contracts.md).
- [ ] T010 Patch `slides/deploy-pptx.sh` per [contracts/build-pipeline-contract.md](contracts/build-pipeline-contract.md): immediately before the `for deck in "${DECKS[@]}"` loop, add the 4-line `THEME_DIR` / `THEME_ARGS` block (auto-detect `slides/themes/*.css`); add `"${THEME_ARGS[@]}"` to each of the three Marp invocations (PPTX, PDF, HTML). Must remain a no-op when `slides/themes/` is absent or empty (backward compatibility for intermediate decks).
- [ ] T011 Smoke-build to confirm the foundational layer: run `./slides/deploy-pptx.sh` and confirm exit code 0. Beginner decks at this point still declare `theme: default` (no opt-in yet) — the script change MUST NOT regress any deck. If any intermediate deck fails to render, stop and fix before proceeding.

**Checkpoint**: Foundation ready — User Stories may begin.

---

## Phase 3: User Story 1 — A first-time learner is hooked in 10 seconds (Priority: P1) 🎯 MVP

**Goal**: Module 01's cover + first three content slides feel premium enough that ≥ 4 of 5 first-impression reviewers (SC-001) use a positive aesthetic adjective unprompted.

**Independent Test**: Render `slides/beginner/part-01-meet-claude-code.md` to PPTX + PNG; run the SC-001 reviewer panel (n=5, protocol in [quickstart.md](quickstart.md#reviewer-set-r1-referenced-by-sc-001--sc-004)). PASS = ≥ 4/5 positive, 0/5 "plain"/"default"/"amateur".

### Implementation

- [ ] T012 [US1] Author the **Module 01 teaching visual** at `slides/beginner/assets/01-three-skills.svg` — an inline SVG concept map (palette-compliant per data-model §TeachingVisual invariants) that visualizes the lesson's three skills (open Claude Code → send a prompt → save the reply). Must teach the lesson with body text hidden (SC-004 prerequisite).
- [ ] T013 [US1] Restyle `slides/beginner/part-01-meet-claude-code.md`: change front-matter `theme: default` → `theme: wow-beginner`; apply `<!-- _class: tpl-cover -->` to the cover slide and fill its required slots (module-number, title, course-name, hero-visual referencing one icon from `slides/themes/icons/`); apply `<!-- _class: tpl-objectives -->`, `<!-- _class: tpl-show -->`, `<!-- _class: tpl-try -->`, `<!-- _class: tpl-done -->`, `<!-- _class: tpl-next -->` to the matching existing sections. Embed the SVG from T012 on the Show-Me or Why-this-matters slide. Tighten prose only where required for layout fit; **all verbatim-protected blocks (objectives, commands in Show-Me, Try-It steps, Definition-of-done checklist) MUST be byte-identical to pre-polish source** (FR-010, research §6).
- [ ] T014 [US1] Render and PNG-export the cover + first three content slides for the reviewer panel: `./slides/deploy-pptx.sh --html` then convert via Chromium headless or screenshot to `specs/003-slide-wow-polish/review-samples/module-01-{slide-1..4}.png`. (Use `npx playwright screenshot` opportunistically or any local screenshot tool; commit the PNGs.)
- [ ] T015 [US1] Run the **SC-001 reviewer panel** (n=5) per `quickstart.md` Reviewer Set R1. Record verbatim answers in `specs/003-slide-wow-polish/reviewer-panel-results.md` under heading "SC-001 (Module 01)". PASS gate: ≥ 4 positive adjectives, 0 "plain"/"default"/"amateur" mentions. If FAIL, iterate on T012–T013 and re-run T014–T015.

**Checkpoint**: Module 01 is the MVP — demo-able on its own as the "wow moment" for the polish pass.

---

## Phase 4: User Story 2 — Consistent design system across all 8 modules (Priority: P1)

**Goal**: Modules 02–08 inherit the same theme + recurring templates + footer/header treatment that Module 01 established.

**Independent Test**: Open all 8 rendered PPTX files in thumbnail view; reviewer confirms same cover layout, same recurring template treatments, same footer, same palette, same typography across all decks (SC-002).

### Implementation (modules 02–08 — one task per deck, parallelizable; each follows the same pattern as T013)

- [ ] T016 [P] [US2] Restyle `slides/beginner/part-02-first-conversation.md`: front-matter `theme: wow-beginner`; apply `tpl-cover`, `tpl-objectives`, `tpl-show`, `tpl-try`, `tpl-done`, `tpl-next` per [contracts/slide-template-contracts.md](contracts/slide-template-contracts.md); tighten prose only; verbatim-protect objectives + commands + steps + DoD checklist.
- [ ] T017 [P] [US2] Restyle `slides/beginner/part-03-asking-for-what-you-want.md` — same pattern as T016.
- [ ] T018 [P] [US2] Restyle `slides/beginner/part-04-reading-code-together.md` — same pattern as T016.
- [ ] T019 [P] [US2] Restyle `slides/beginner/part-05-editing-one-file-safely.md` — same pattern as T016. (Candidate for one `tpl-divider` between "edit" and "commit" halves per contract §Template 2.)
- [ ] T020 [P] [US2] Restyle `slides/beginner/part-06-claude-md-cheat-sheet.md` — same pattern as T016. (Use `book.svg` as cover hero per icon inventory.)
- [ ] T021 [P] [US2] Restyle `slides/beginner/part-07-safer-and-smarter.md` — same pattern as T016. (Use `shield.svg` and pair `--danger` color with `warning.svg` per FR-006.)
- [ ] T022 [P] [US2] Restyle `slides/beginner/part-08-putting-it-together.md` — same pattern as T016. (Closing slide uses `award.svg` and "You finished Claude Code 101" string per contract §Template 7.)
- [ ] T023 [US2] After T016–T022 land, render thumbnail-grid review: `./slides/deploy-pptx.sh --html`; open `slides/dist/html/beginner/*.html` side-by-side. Verify SC-002: same cover layout, same recurring template treatments, same footer string, same palette, same typography pair across all 8 decks. Record verdict in `specs/003-slide-wow-polish/reviewer-panel-results.md` under "SC-002 (consistency)".

**Checkpoint**: All 8 decks share the same design identity. Demo-able as a thumbnail grid.

---

## Phase 5: User Story 3 — Visuals carry meaning, not decoration (Priority: P1)

**Goal**: Every module has ≥ 1 purposeful teaching visual; ≥ 6 of 8 reviewers can name the lesson's main idea from visual + title alone (SC-004).

**Independent Test**: Run SC-004 reviewer panel (n=8) on the 8 chosen teaching-visual slides with body text blanked out.

**Note**: Module 01's visual (`01-three-skills.svg`) was authored in T012 as part of US1; the remaining 7 SVGs are authored here and wired into their decks. These tasks may be parallelized across modules (different SVG file + different deck file per task) — but each is sequenced *after* its US2 restyle task (T016–T022) so the deck has the templates ready to host the visual.

### Implementation

- [ ] T024 [P] [US3] Author `slides/beginner/assets/02-accept-reject-loop.svg` (the prompt → diff → accept|reject → next-turn loop) AND wire it into `slides/beginner/part-02-first-conversation.md` on the appropriate Show-Me / Concept slide. Palette-compliant per data-model invariants. *Depends on T016.*
- [ ] T025 [P] [US3] Author `slides/beginner/assets/03-prompt-anatomy.svg` (Role + Goal + Constraint + Format dissection) AND wire it into `slides/beginner/part-03-asking-for-what-you-want.md`. *Depends on T017.*
- [ ] T026 [P] [US3] Author `slides/beginner/assets/04-explain-flow.svg` (file → highlight → "explain" → plain-English bubble) AND wire it into `slides/beginner/part-04-reading-code-together.md`. *Depends on T018.*
- [ ] T027 [P] [US3] Author `slides/beginner/assets/05-edit-with-git-net.svg` (edit → diff → `git diff` / `git restore` safety net) AND wire it into `slides/beginner/part-05-editing-one-file-safely.md`. *Depends on T019.*
- [ ] T028 [P] [US3] Author `slides/beginner/assets/06-claude-md-anatomy.svg` (the 15-line CLAUDE.md broken into labeled regions) AND wire it into `slides/beginner/part-06-claude-md-cheat-sheet.md`. *Depends on T020.*
- [ ] T029 [P] [US3] Author `slides/beginner/assets/07-never-paste-matrix.svg` (a 2×3 grid of "secrets / PII / proprietary" × "safe / risky" with shield + warning icons) AND wire it into `slides/beginner/part-07-safer-and-smarter.md`. **Must use shield + warning icons + labels, not color alone** (FR-006 enforcement). *Depends on T021.*
- [ ] T030 [P] [US3] Author `slides/beginner/assets/08-capstone-pipeline.svg` (the `add` → `list` → `delete` → `list` smoke-check pipeline that the grader runs) AND wire it into `slides/beginner/part-08-putting-it-together.md`. *Depends on T022.*
- [ ] T031 [US3] Run the **SC-004 reviewer panel** (n=8) per `quickstart.md` Reviewer Set R1. For each of the 8 modules, show the chosen teaching-visual slide with body text mentally/visually blanked. Record results in `reviewer-panel-results.md` under "SC-004 (visual comprehension)". PASS gate: ≥ 6 / 8 correct on ≥ 6 of 8 modules. If any module fails, iterate on its SVG and re-test that module.

**Checkpoint**: Every module teaches at least once with pictures, not just words.

---

## Phase 6: User Story 4 — The build pipeline still works (Priority: P1)

**Goal**: `./slides/deploy-pptx.sh --all` succeeds on a clean checkout; intermediate decks unaffected; build-time within budget; no canvas overflow.

**Independent Test**: Clean checkout → `./slides/deploy-pptx.sh --all` returns exit 0; all 8 beginner + 10 intermediate decks produce PPTX + PDF + HTML; `scripts/check-slide-overflow.sh` reports 0 overflows; wall-clock ≤ 1.5 × baseline.

### Implementation

- [ ] T032 [US4] Author `scripts/check-slide-overflow.sh` per [contracts/build-pipeline-contract.md](contracts/build-pipeline-contract.md) "Out-of-script verification": iterate over `slides/dist/html/beginner/*.html`, grep each for the Marp overflow marker (per research §4), print `PASS — 0 overflows` and exit 0 if clean, otherwise print `<deck>:<slide-number>` for each offender and exit non-zero. Mark `chmod +x`. Document one-line usage at the top.
- [ ] T033 [US4] Run a full clean-checkout build: `rm -rf slides/dist && ./slides/deploy-pptx.sh --all`. Verify (a) exit 0, (b) `slides/dist/{pptx,pdf,html}/{beginner/,}*.{pptx,pdf,html}` all present for all 8 beginner + 10 intermediate decks, (c) wall-clock seconds ≤ 1.5 × the value in `baseline-build-time.txt`. Record the post-polish time in `specs/003-slide-wow-polish/post-polish-build-time.txt` with the same one-line context.
- [ ] T034 [US4] Run `./scripts/check-slide-overflow.sh slides/dist/html/beginner/`. Verify `0 overflows` reported. If any slide overflows, fix the offending deck (split the slide, tighten prose within FR-010 limits, or shrink an SVG) and re-run.
- [ ] T035 [US4] Visual regression spot-check on intermediate decks: open `slides/dist/pptx/part-01-setup-mindset.pptx` (and one mid-deck like part-05) and confirm they render with the default Marp theme exactly as they did pre-feature — no accidental inheritance from `wow-beginner` (which would indicate the foundational opt-in is broken).

**Checkpoint**: Pipeline integrity confirmed. SC-006 + SC-007 + FR-013 verified.

---

## Phase 7: User Story 5 — Accessibility & projection-readiness (Priority: P2)

**Goal**: WCAG AA contrast on every template; no color-only meaning; projection-readable; PDF accessible.

**Independent Test**: Run contrast script across all template combinations → all pairs ≥ 4.5:1; grayscale render of a slide using each color-coded element remains interpretable; PDF projected at 1920×1080 readable from 8 m.

### Implementation

- [ ] T036 [P] [US5] Author `scripts/check-contrast.sh` (or a small Node one-liner) that reads the palette tokens from `slides/themes/wow-beginner.css` and asserts every text/background pair in data-model §Palette meets ≥ 4.5:1. Exits non-zero with the offending pair if any fail. Run it; record result; commit script.
- [ ] T037 [P] [US5] **Color-blind audit**: render one slide from each of the 7 template classes (cover, divider, objectives, show, try, done, next) — choose slides that exercise `--success` (DoD checklist) and `--danger` (Module 07 warning). Pipe their PNGs through a deuteranopia + protanopia simulator (any CLI or web tool; document which). For each, verify the slide's meaning is still recoverable in grayscale (FR-006, SC-008). Record evidence in `reviewer-panel-results.md` under "SC-008 (color-blind audit)".
- [ ] T038 [P] [US5] **Projection-readiness check**: open `slides/dist/pdf/beginner/part-01-meet-claude-code.pdf` full-screen at 1920×1080 and stand 8 m away (or scale equivalent on a 13-inch screen with the test described in spec edge cases). Confirm body text remains legible. If any template fails, increase its font size in `wow-beginner.css` and re-build. Record the verdict.
- [ ] T039 [US5] **Keynote / LibreOffice fallback check** (edge case): open `slides/dist/pptx/beginner/part-01-meet-claude-code.pptx` in Keynote (or LibreOffice Impress if Keynote unavailable). Verify fonts gracefully fall back to a system sans / mono of the same class with no layout overflow. If overflow appears, tune the `font-family` fallback chain in `wow-beginner.css`. Record verdict.

**Checkpoint**: Accessibility + projection + cross-app fallback confirmed.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final reviewer-panel rollup, repo hygiene, and seat-time / FR-010 verification.

- [ ] T040 [P] **Verbatim-block diff audit** (FR-010 / research §6): for each of the 8 beginner decks, produce a git diff filtered to the 5 verbatim-protected block types (objectives list, code/terminal fences in Show-Me, numbered steps in Try-It, checklist items in Definition-of-Done, Module 08 capstone scope strings). Confirm token-set is identical to pre-polish source. Save the verification log to `specs/003-slide-wow-polish/verbatim-audit.md`.
- [ ] T041 [P] **Seat-time invariant check** (FR-011 / SC-009): for each module, re-estimate seat-time using the same method spec 002 used (slide-count × per-slide minute factor) and compare to the per-module budget (Module 01 = 20, 02 = 25, 03 = 30, 04 = 25, 05 = 30, 06 = 25, 07 = 25, 08 = 30). Tolerance ± 2 min per module; never above the ceiling. Record in `specs/003-slide-wow-polish/seat-time-check.md`.
- [ ] T042 [P] **License-notice presence check**: confirm `slides/themes/fonts/LICENSE.txt` and `slides/themes/icons/LICENSE.txt` exist, name their families, and are referenced from `slides/themes/README.md`. Cross-check repo `LICENSE` does not contradict.
- [ ] T043 **Final reviewer-panel results rollup**: consolidate SC-001, SC-002, SC-004, SC-008 outcomes in `reviewer-panel-results.md` with an "Overall: PASS / FAIL" verdict for the feature. Each SC entry must show the threshold, the measured value, and the pass/fail decision.
- [ ] T044 **Quickstart dry-run (SC-010)**: ask one non-author to follow [quickstart.md](quickstart.md) from a clean checkout and produce a compliant ninth-module skeleton deck in ≤ 10 minutes. Record their elapsed time and any blockers in `specs/003-slide-wow-polish/quickstart-dryrun.md`. If they hit a blocker, fix `quickstart.md` (and possibly `slides/themes/README.md`) and re-run with a fresh reviewer.

---

## Dependencies & Story-Completion Order

```
Setup (T001–T007)
   └─► Foundational (T008–T011)        [BLOCKS ALL USER STORIES]
          ├─► US1: T012 → T013 → T014 → T015               (MVP — demo here)
          ├─► US2: T016..T022 [P] → T023
          ├─► US3: T024..T030 [P, each depends on its US2 task] → T031
          ├─► US4: T032, then T033 → T034, T035            (verifies US1–US3 + intermediate-deck non-regression)
          └─► US5: T036, T037, T038, T039 [P]              (independent once Foundational done; benefits from US2 finishing)
                 └─► Polish (T040–T044) [T040–T042 [P]; T043 → T044]
```

- **US1 is the MVP.** Stopping after T015 ships a single polished module (01) that demonstrates the design system end-to-end.
- **US2 unblocks US3** per-module: each US3 SVG task (T024–T030) depends on its matching US2 deck restyle (T016–T022) because the SVG is wired into the restyled deck.
- **US4 verifies everything**: run T033 *after* US1 + US2 + US3 land; run T032 (the script) at any point after Foundational.
- **US5 is largely independent** of US1–US3 once Foundational lands — but the contrast/projection/fallback checks are most meaningful after the design system has been exercised across all 8 decks (after US2).

## Parallel Execution Examples

**Setup parallel batch** (after T001–T003): launch T004, T005, T006, T007 together — all touch different files under `slides/themes/`.

**US2 parallel batch** (after Foundational + US1): launch T016, T017, T018, T019, T020, T021, T022 together — seven different deck files, no shared edits.

**US3 parallel batch** (after the matching US2 tasks land): launch T024, T025, T026, T027, T028, T029, T030 together — each touches its own SVG file plus a single deck file already restyled in US2.

**US5 parallel batch** (after Foundational): launch T036, T037, T038, T039 together — independent verification tasks against different artifacts.

**Polish parallel batch**: launch T040, T041, T042 together — independent audit logs.

## Implementation Strategy

1. **Burn the baseline first**: T003 captures the pre-polish build time. This number anchors SC-006 and cannot be recovered after the foundational change lands.
2. **Land Foundational (T008–T011) on one PR.** Smoke-build (T011) is the gate.
3. **Ship the MVP (US1)** on a second PR — Module 01 alone. Run the SC-001 panel (T015) before opening the PR for review; the panel result *is* the PR's "did this work?" evidence.
4. **Roll out US2 in parallel** (one PR or one PR per deck; either is fine because tasks are file-isolated). Land T023 (consistency review) once all 7 are merged.
5. **Land US3 SVGs incrementally** as each module's deck finishes US2. Run the SC-004 panel (T031) only when all 8 visuals are in.
6. **Verify with US4 + US5** before declaring done. T033's build-time check is the gate for SC-006; T034 for SC-007; T036–T039 for the accessibility SCs.
7. **Close with Polish**: T043 produces the feature-level PASS/FAIL verdict; T044 verifies the new-contributor experience (SC-010) and surfaces any docs gap.

## Format Validation

All 44 tasks above:

- start with `- [ ]`
- carry a sequential ID `T0NN`
- carry a `[P]` marker only when they are file-isolated and unblocked
- carry a `[US1]..[US5]` story label inside Phases 3–7 only; Setup, Foundational, and Polish phases carry no story label per the format rules
- name exact file paths in the description

Total tasks: 44.
- Setup: 7 (T001–T007).
- Foundational: 4 (T008–T011).
- US1: 4 (T012–T015).
- US2: 8 (T016–T023).
- US3: 8 (T024–T031).
- US4: 4 (T032–T035).
- US5: 4 (T036–T039).
- Polish: 5 (T040–T044).

Parallel opportunities: 4 setup tasks; 7 US2 deck restyles; 7 US3 SVG authoring tasks; 4 US5 audits; 3 polish audits. Sequential gates: Foundational smoke-build (T011), MVP panel (T015), US2 consistency review (T023), US3 visual panel (T031), build-time + overflow gates (T033, T034), final rollup (T043), quickstart dry-run (T044).

Suggested MVP: complete through T015 (Module 01 polished + SC-001 panel passed). That alone is demo-able and validates the design system end-to-end against the spec's biggest first-impression risk.
