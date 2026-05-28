# Feature Specification: Intermediate Course Content Polish

**Feature Branch**: `004-intermediate-content-polish`

**Created**: 28 May 2026

**Status**: Draft

**Input**: User description: "this is the content of the course to enhance. I like the new design but this is the content, not anything else" — provided alongside the 10 intermediate Marp decks (`slides/part-01-setup-mindset.md` through `slides/part-10-production-readiness.md`).

## Clarifications

### Session 2026-05-28

- Q: How should build output artefacts be organised under `slides/dist/`? → A: Keep `slides/dist/` name; split by audience: `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/`.
- Q: How aggressively may editable prose sections be polished? → A: Tighten only — shorten, sharpen verbs, remove filler. No new examples, no reordering, no factual additions. Post-polish word count per editable section MUST be ≤ pre-polish word count.
- Q: How is the intermediate theme architected? → A: Sibling file `slides/themes/wow-intermediate.css` that `@import`s `wow-beginner.css` for palette/typography tokens, then adds exactly one new template class `tpl-demo` for the Live-demo-flow slide. All 10 intermediate decks declare `theme: wow-intermediate`.
- Q: How many teaching SVGs per intermediate module? → A: Exactly one SVG per module, mandatory on the Concepts slide. No second teaching SVG permitted; 10 SVGs total across the intermediate course.
- Q: Are Common-mistakes bullets verbatim-protected or editable? → A: Editable under the same tighten-only rule as the other prose sections (FR-010). No special verbatim carve-out; polish is trusted to preserve meaning.

## Summary

Feature 003 introduced a "wow" design system (palette, typography, 7 slide templates, teaching SVGs) and applied it to the 8 beginner decks. The user has confirmed they like the result and now wants the **same design treatment applied to the 10 intermediate Bootcamp decks, AND the prose content of those decks polished**. Scope is explicitly limited to the **slide content** (and the design layer that styles it). Exercises, skills, scripts, assessments, and student/instructor guides are **out of scope** for this feature.

The work is parallel in shape to feature 003 but targets a different audience: senior-leaning engineers running a 4-hour bootcamp, not absolute beginners. The pedagogical anatomy is denser (13 H2 sections per deck instead of 8), the prose is more technical, and the teaching visuals must convey engineering workflows (Plan→Implement→Test→Review→Commit loop, Best-of-N scoring, constrained refactor, 5-axis readiness) rather than first-touch UX flows.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Apply the WOW design system to every intermediate deck (Priority: P1)

A Bootcamp instructor opens any of the 10 intermediate decks in Marp and sees the same custom theme, palette, typography pair, header/footer treatment, and per-template slide treatments that the beginner course got in feature 003 — adapted for the denser intermediate anatomy. The cover slide carries a "Bootcamp · Day 1 · Block N of 10" chip; the closing slide signals the next module (or the wrap on Module 10).

**Why this priority**: This is the *named* user request ("I like the new design — apply it"). Without it the intermediate course visually lags the beginner course and the workshop loses its single visual identity. It is also the prerequisite for the content polish — the design templates create the slots the polished content fills.

**Independent Test**: Build the 10 intermediate decks (`./slides/deploy-pptx.sh`). Verify every deck declares `theme: wow-intermediate`, every cover slide renders the bootcamp chip + hero icon, every concept/show/try/recap slide picks up its `tpl-*` class, and the rendered PPTX/PDF/HTML are visually coherent as a 10-deck set when laid out as a thumbnail grid.

**Acceptance Scenarios**:

1. **Given** the current `slides/themes/` directory (containing `wow-beginner.css` and shared fonts/icons), **When** a maintainer runs `./slides/deploy-pptx.sh --all`, **Then** all 10 intermediate decks build with the intermediate theme variant and the 8 beginner decks remain visually unchanged (their `theme: wow-beginner` front-matter is untouched).
2. **Given** the 10 intermediate decks rendered to PNG thumbnails, **When** a reviewer compares them side-by-side, **Then** the cover, divider, concept, demo-flow, lab, prompts, checklist, DoD, review, and transition templates each appear with the same recurring treatment across all 10 modules.
3. **Given** an instructor projects any deck full-screen at 1920×1080, **When** they advance from cover to transition, **Then** the page-number indicator, the bootcamp footer (`Claude Code Bootcamp · Day 1 · Module NN`), and the palette remain stable.

---

### User Story 2 — Sharpen the prose content of every intermediate module (Priority: P1)

A bootcamp student opens any module and reads tighter, more memorable Promise / Why / Concepts / Common-mistakes sections than the pre-polish version, while every verbatim-protected block (learning objectives, suggested Claude Code prompts, deliverable checklists, definition-of-done lines) appears **bit-identical** to the pre-polish text. The polish never widens scope; it tightens, sharpens, and adds memorable framings.

**Why this priority**: The user said "this is the content … to enhance" — content polish is explicitly named alongside the design carry-over. The intermediate decks were drafted quickly during spec 001; many Promise lines, demo flows, and transitions can be sharper without changing the curriculum or breaking exercise/assessment alignment.

**Independent Test**: For each of the 10 decks, diff post-polish vs pre-polish source. The diff must (a) leave the 5 verbatim-block categories byte-identical (Objectives lists, Suggested Claude Code prompt fences, Deliverable checklists, Definition-of-done lines, Step-by-step lab numbered steps), and (b) show tightened prose in at least Promise, Why-this-matters, Concepts, Common-mistakes, and Transition sections.

**Acceptance Scenarios**:

1. **Given** a student reads the Promise of Module 4 ("Build Faster with Best-of-N"), **When** the student finishes the 3 numbered Promise items, **Then** they can predict the lab deliverable (3 candidate folders + scoring.md + winner) in one sentence without scrolling.
2. **Given** the instructor opens Module 8 ("Refactoring & Documentation at Scale"), **When** they read the Why-this-matters section, **Then** every sentence either names a concrete production risk or proposes a measurable engineering practice — no filler.
3. **Given** an automated audit script greps for the verbatim-protected phrases (e.g., "GOAL\nBuild a single-binary CLI Task Manager", "Use the production-readiness-review skill"), **When** it runs against the post-polish decks, **Then** every protected phrase still appears with the original wording.

---

### User Story 3 — Every intermediate module has at least one teaching visual (Priority: P1)

A student who only sees the *one teaching visual per module* (cover hidden, body text blanked) can name the module's main idea in one sentence. Teaching visuals are SVG-only, palette-compliant, and visualise the lesson's central engineering concept (the loop, GCOE, BoN scoring, refactor constraints, the 5 axes, etc.).

**Why this priority**: Spec 003 set this gate at SC-004 for the beginner course (≥ 6/8 visual-only comprehension); applying the same gate to intermediate is what makes the design system "the same treatment" rather than "just a theme swap".

**Independent Test**: A reviewer panel (n=8) is shown the 10 teaching-visual slides with body text blanked. ≥ 6 of 8 reviewers correctly name the module's main idea on ≥ 7 of 10 modules.

**Acceptance Scenarios**:

1. **Given** the 10 teaching SVGs ship under `slides/intermediate/assets/NN-*.svg`, **When** a reviewer sees Module 4's `04-bon-scoring.svg`, **Then** they correctly identify "generate multiple candidates, score, pick the winner" without prior briefing.
2. **Given** an SVG is embedded into a deck slide, **When** the deck is built to PPTX, **Then** the SVG renders inline (not as a broken image link) and its colors match the palette tokens declared in `wow-intermediate.css`.
3. **Given** every teaching visual is inspected, **When** rendered in grayscale, **Then** its meaning is recoverable (no information conveyed by color alone).

---

### User Story 4 — Build pipeline & non-regression integrity (Priority: P1)

The build pipeline continues to ship 10 intermediate + 8 beginner decks to PPTX, PDF, and HTML on one command, within 1.5× the pre-polish build time, with zero slides overflowing the 16:9 canvas. The 8 beginner decks (feature 003 output) remain byte-identical in their source markdown.

**Why this priority**: A polished deck that breaks the build pipeline or regresses the beginner course is a regression, not an enhancement. The constitutional principle of "Marp is the source of truth" requires that one script still produces everything.

**Independent Test**: A clean checkout build (`rm -rf slides/dist && ./slides/deploy-pptx.sh --all`) returns exit 0, produces all 54 output artefacts (18 decks × 3 formats) under the audience-first layout `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/`, runs in ≤ 1.5 × the baseline recorded for spec 003, and `scripts/check-slide-overflow.sh` reports 0 overflows for the intermediate decks (with an updated budget appropriate for the denser intermediate layout).

**Acceptance Scenarios**:

1. **Given** the build runs cleanly, **When** the wall-clock seconds are recorded, **Then** they are ≤ 1.5 × the value in `specs/003-slide-wow-polish/baseline-build-time.txt` (423.86 s → ceiling 635.79 s).
2. **Given** `scripts/check-slide-overflow.sh` is extended to also scan `slides/dist/html/*.html` (intermediate), **When** it runs against the post-polish build, **Then** it reports `OK` for all 18 decks.
3. **Given** `git diff --stat HEAD -- slides/beginner/` is inspected, **When** this feature's PR is reviewed, **Then** zero beginner-deck source files appear in the diff.

---

### User Story 5 — Accessibility & projection-readiness on the intermediate decks (Priority: P2)

Every template combination used in the intermediate decks meets WCAG 2.1 AA contrast on the same automated check used for the beginner course, every color-coded element pairs hue with an icon and a label, and the decks remain projection-readable at 1920×1080 from 8 m away.

**Why this priority**: P2 because the palette tokens are inherited from `wow-beginner.css` and were already verified at WCAG AA in spec 003 (`scripts/check-contrast.sh` PASS 9/9). The work here is to re-run the check against any new intermediate-specific palette extensions (e.g., a deeper accent for divider slides) and to spot-check the denser layouts under projection.

**Independent Test**: `scripts/check-contrast.sh` passes against the intermediate theme; one projection test confirms readability of the densest intermediate slide.

**Acceptance Scenarios**:

1. **Given** `wow-intermediate.css` introduces any new palette tokens, **When** `scripts/check-contrast.sh` runs, **Then** every new text/background pair meets the same minimums as the beginner palette.
2. **Given** Module 4's BoN-scoring slide (a known-dense layout), **When** projected at 1920×1080 from 8 m, **Then** body text remains legible.

---

### Edge Cases

- **A pre-polish deck contains content that exceeds the new tighter template's safe density.** Mitigation: split into two slides (allowed) or shorten prose to fit (allowed; verbatim blocks excluded). Adding new slides is allowed *only when* needed to honour FR-010 (verbatim preservation) without overflow.
- **A teaching SVG is needed for a concept that is genuinely abstract** (e.g., Module 10's "Go/No-Go verdict"). Allowed treatment: a decision-tree or a 5-axis radar; not allowed: a decorative icon with no informational content.
- **An intermediate deck references a path or asset that the beginner-course design carried over** (e.g., a Lucide icon). Allowed: reuse `slides/themes/icons/*.svg`. Not allowed: duplicate the icons under a new folder.
- **The instructor wants to override the new header/footer string for a guest session.** Marp's per-slide `<!-- _header: "" -->` directive remains available (same escape hatch as the beginner decks).
- **A pre-polish "Common mistakes" list captures a hard-won lesson.** The Common-mistakes section is editable under the FR-010 tighten-only rule (no special verbatim carve-out). The author MUST preserve the underlying warning when tightening: shorten phrasing without dropping the failure mode or the corrective action.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A new Marp theme `slides/themes/wow-intermediate.css` MUST exist as a sibling of `slides/themes/wow-beginner.css`. It MUST `@import` `wow-beginner.css` so that the palette tokens, typography pair, and the 7 base template classes (`tpl-cover`, `tpl-divider`, `tpl-objectives`, `tpl-show`, `tpl-try`, `tpl-done`, `tpl-next`) are inherited from a single source of truth. The intermediate theme MUST add exactly one new template class — `tpl-demo` — for the Live-demo-flow slide; cover-chip wording and footer string MAY also be overridden. No palette duplication; no fork of the base classes.
- **FR-002**: All 10 intermediate decks (`slides/part-01-setup-mindset.md` … `slides/part-10-production-readiness.md`) MUST declare `theme: wow-intermediate` in front-matter and `header: "Claude Code Bootcamp · Day 1 · Module NN"`.
- **FR-003**: Each intermediate deck MUST apply one slide-template class marker per relevant slide using Marp's `<!-- _class: ... -->` directive, drawn from this fixed vocabulary: `tpl-cover`, `tpl-divider`, `tpl-objectives`, `tpl-show`, `tpl-try`, `tpl-done`, `tpl-next` (inherited from wow-beginner) and `tpl-demo` (new in wow-intermediate, used for the Live-demo-flow slide). `tpl-demo` MUST appear at least once in every intermediate deck.
- **FR-004**: Each intermediate deck MUST embed **exactly one** teaching SVG, placed on the Concepts slide, stored at `slides/intermediate/assets/NN-<lesson-slug>.svg`. Total intermediate teaching SVGs across the course MUST equal 10. No second teaching SVG is permitted on any other slide (decorative icons drawn from `slides/themes/icons/` are not teaching SVGs and remain allowed). The SVG MUST carry the lesson by itself (per SC-004).
- **FR-005**: Teaching SVGs MUST use only palette tokens defined in the wow theme. No external palette. No embedded raster images.
- **FR-006**: Any color-coded indicator on intermediate slides (success ✓, warning ⚠, danger ✕, go / no-go) MUST pair the hue with an icon and a text label so the meaning is recoverable in grayscale (carry-over from feature 003 FR-006).
- **FR-007**: The cover slide of each intermediate deck MUST carry a "Bootcamp · Day 1 · Block N of 10" chip and a hero icon drawn from `slides/themes/icons/` (no new icon downloads).
- **FR-008**: The closing transition slide MUST visibly preview the next module's title; Module 10's closing slide MUST signal the workshop wrap explicitly (use the `is-finale` modifier introduced in feature 003).
- **FR-009**: The build script `slides/deploy-pptx.sh` MUST NOT need any new flags. The existing `--theme-set slides/themes/` patch from feature 003 must already handle the new theme by virtue of dropping `wow-intermediate.css` into the same directory.
- **FR-010**: For each intermediate deck, the following blocks MUST remain byte-identical to the pre-polish source: (a) Promise's numbered list, (b) every fenced block in "Suggested Claude Code prompts", (c) every line under "Deliverable checklist", (d) every line under "Definition of done", (e) every numbered step in "Step-by-step lab". Other prose sections (Why-this-matters, Concepts, Common mistakes, Instructor notes, Transition) MAY be **tightened only**: shorten wordy prose, sharpen verbs, remove filler. No new examples, no reordering of bullets, no new analogies, no factual additions, no splitting one section into multiple slides. For each editable section, the post-polish word count MUST be ≤ the pre-polish word count.
- **FR-011**: Total per-deck duration (declared in the `<!-- duration: NN min -->` directive at the top) MUST remain unchanged. The sum of all 10 declared durations MUST equal 240 minutes (the existing 4-hour bootcamp budget).
- **FR-012**: The 8 beginner decks MUST NOT be modified. A `git diff --stat HEAD -- slides/beginner/` against the merge base of this feature must be empty.
- **FR-013**: The clean-checkout build time MUST be ≤ 1.5 × the baseline value in `specs/003-slide-wow-polish/baseline-build-time.txt`.
- **FR-014**: `scripts/check-slide-overflow.sh` MUST be extended to also scan `slides/dist/html/*.html` (intermediate decks). Budget MAY be raised from 18 to 22 elements per slide to accommodate the denser intermediate anatomy, but the script MUST still flag any slide above that budget.
- **FR-015**: `slides/themes/README.md` MUST be updated to document the wow-intermediate theme, the `@import` relationship with wow-beginner, the new `tpl-demo` template, and the rule "intermediate decks live under `slides/`; their assets under `slides/intermediate/assets/`" (parallel to the beginner-asset rule).
- **FR-016**: License notices for any new icons or fonts pulled in for intermediate-specific needs MUST be appended to the existing `slides/themes/icons/LICENSE.txt` or `slides/themes/fonts/LICENSE.txt`. Preferred path: reuse what feature 003 already shipped.
- **FR-017**: Exercises (`exercises/`), skills (`skills/`), assessments (`assessments/`), student/instructor guides, and any spec-kit artefacts under `specs/00{1,2,3}/` MUST NOT be modified.
- **FR-018**: Build output MUST be organised as `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/<deck>.{pptx,pdf,html}`. The directory name `slides/dist/` is preserved (no rename); the audience split (`intermediate/` vs `beginner/`) comes first and the format split (`pptx/`, `pdf/`, `html/`) comes second. `slides/deploy-pptx.sh` MUST emit artefacts into the correct audience subtree based on the source deck's location (intermediate decks under `slides/part-NN-*.md`; beginner decks under `slides/beginner/part-NN-*.md`). A complete audience hand-off ("send me all the intermediate PDFs") MUST be possible by copying a single subdirectory.

### Key Entities *(if data involved)*

- **IntermediateDeck**: a Marp markdown file under `slides/part-NN-*.md` for N ∈ {01..10}. 13 H2 sections (Promise, Why-this-matters, Concepts, Live-demo-flow, Mini-project, Step-by-step-lab, Suggested-Claude-Code-prompts, Deliverable-checklist, Definition-of-done, Review-checkpoint, Common-mistakes, Instructor-notes, Transition).
- **WowIntermediateTheme**: `slides/themes/wow-intermediate.css`. Sibling of `wow-beginner.css`. `@import`s wow-beginner (single source of truth for palette, typography, and the 7 base `tpl-*` classes). Adds exactly one new class: `tpl-demo` for the Live-demo-flow slide. MAY override cover-chip wording and footer string; MUST NOT redefine palette tokens or fork base classes.
- **IntermediateTeachingVisual**: an SVG under `slides/intermediate/assets/NN-<lesson-slug>.svg`. Has a `<title>` and `<desc>` for screen readers; uses only palette tokens; conveys the lesson without body text.
- **VerbatimBlockSet**: per FR-010 — the 5 categories of content frozen for this feature (Promise list, Claude-Code prompt fences, Deliverable checklist, Definition of done, Step-by-step lab steps).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A 5-reviewer first-impression panel rates the new intermediate cover slides "polished / professional / focused / clear" (positive adjectives) on ≥ 4 of 5 responses for ≥ 8 of 10 covers; 0 of 5 reviewers say "plain / default / amateur / busy" on any cover.
- **SC-002**: When the 10 intermediate decks + 8 beginner decks are laid out as a thumbnail grid, a reviewer cannot identify which course the visual identity originated in: cover layout, palette, typography, header/footer, and template treatments are uniformly recognisable across all 18 decks.
- **SC-003**: 100% of intermediate decks (10/10) declare `theme: wow-intermediate` and successfully build to PPTX, PDF, and HTML on a single `./slides/deploy-pptx.sh --all` invocation.
- **SC-004**: An 8-reviewer visual-only comprehension panel correctly identifies the lesson's central concept from the teaching SVG (body text blanked) on ≥ 7 of 10 modules.
- **SC-005**: `scripts/check-contrast.sh` returns exit 0 against the intermediate theme; all text/background pairs meet WCAG 2.1 AA.
- **SC-006**: Clean-checkout build wall-clock ≤ 1.5 × the baseline in `specs/003-slide-wow-polish/baseline-build-time.txt` (≤ 635.79 s).
- **SC-007**: `scripts/check-slide-overflow.sh` reports 0 overflows across all 18 decks (10 intermediate + 8 beginner) with the intermediate budget set to 22 content elements per slide.
- **SC-008**: Color-blind audit (deuteranopia + protanopia simulation) of one slide per template class in the intermediate course confirms that the meaning of every color-coded element is recoverable from icon + label without hue.
- **SC-009**: Sum of `<!-- duration: NN min -->` directives across the 10 intermediate decks equals exactly 240 minutes (no module dropped or expanded a minute).
- **SC-010**: An automated verbatim-block audit script greps each protected phrase (FR-010 list) in the post-polish source; the count matches the pre-polish count for every deck (no block deleted or rewritten). The same audit MUST also report the per-section word-count delta for the 5 editable sections; every delta MUST be ≤ 0 (FR-010 tighten-only rule).

## Assumptions

- The wow design system shipped in feature 003 is the canonical visual identity for this course family; this feature inherits it rather than redesigning.
- "Content enhancement" means *tightening* prose (clearer Promise lines, sharper Why-this-matters, more memorable Concepts framings, denser Common-mistakes warnings). It does NOT mean adding new modules, changing the 10-module sequence, or altering exercises/assessments.
- The 13-section intermediate anatomy is the contract. Adding or removing top-level H2 sections is out of scope for this feature.
- The current intermediate decks already satisfy the bootcamp's 240-minute time budget; no module's duration may grow.
- One teaching SVG per module is sufficient for SC-004; richer infographics (multi-panel decks, animations) are out of scope for v1.
- The maintainer is comfortable running deferred human reviewer panels (SC-001, SC-004, SC-008) after the automated portion lands; protocols will be parallel to feature 003's `reviewer-panel-results.md`.

## Out of Scope

- Beginner decks (`slides/beginner/`) — already polished by feature 003; touching them in this feature is a regression.
- Exercises (`exercises/part-NN/`), skills (`skills/`), assessments (`assessments/`), student-guide.md, instructor-guide.md, certificate templates, GLOSSARY.md.
- Build infrastructure changes beyond the optional overflow-budget tweak in FR-014 (the `--theme-set` opt-in from feature 003 is already in place).
- New fonts or icon libraries. The existing bundled Inter + JetBrains Mono fonts and the 13 Lucide icons from feature 003 cover all known intermediate needs.
- Translation, localisation, or alternative language tracks.
- Animations, slide transitions, or speaker-notes embedding.
- Republishing existing reference PPTX/PDF artefacts under `slides/dist/` from prior commits — only the post-polish build output ships.

## Dependencies

- Feature 003 (`003-slide-wow-polish`) MUST be merged. This feature consumes:
  - `slides/themes/wow-beginner.css` (token source)
  - `slides/themes/fonts/` + `slides/themes/icons/` (asset library)
  - `slides/deploy-pptx.sh` patched with `--theme-set` opt-in
  - `scripts/check-slide-overflow.sh` and `scripts/check-contrast.sh` (extended here, not replaced)
- Marp CLI (latest) and Node ≥ 20 — already required by spec 001.
- No new third-party dependencies are introduced.

## Open Questions

- Should the intermediate teaching visuals cross-reference one another (e.g., Module 5's tests-and-debug visual could echo Module 4's BoN scoring rubric for continuity)? **Reasonable default**: yes, but only at the icon level (re-use the same icon vocabulary). Full cross-references add maintenance burden.
- Should the cover slides carry the instructor's name (currently embedded in Module 1's cover)? **Reasonable default**: keep it on Module 1 only as part of the workshop opening; remove from Modules 2–10 where it adds noise.
