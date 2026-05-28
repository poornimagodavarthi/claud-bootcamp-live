# Feature Specification: Slide Decks That Shine — Visual & Pedagogical Polish Pass

**Feature Branch**: `003-slide-wow-polish`

**Created**: 28 May 2026

**Status**: Draft

**Input**: User description: "make the slide really shine and wow."

---

## Context (informed interpretation)

The user-provided phrase is short and visual in intent. Based on the workspace state at request time (active feature `002-claude-beginner-course`, the eight beginner Marp decks under `slides/beginner/`, and the rendering pipeline `slides/deploy-pptx.sh`), this feature is interpreted as a **dedicated visual + pedagogical polish pass on the beginner slide decks** so they look and feel like a premium, modern, "wow" workshop product — without changing the underlying curriculum, learning objectives, or seat-time budget defined by spec 002.

The intermediate decks (`slides/part-01..10-*.md`) are **out of scope for v1** but the design system produced here MUST be reusable for them in a future pass (see Assumptions).

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — A first-time learner opens deck 1 and is hooked in 10 seconds (Priority: P1)

A brand-new learner double-clicks `slides/dist/part-01-meet-claude-code.pptx` (or opens it in their browser via the rendered HTML). Within the first slide they feel "this looks like a real, polished course, not someone's lecture notes" — confident enough to keep going. By slide 3 they have understood the lesson promise visually, without having to read every word.

**Why this priority**: First-impression drop-off is the single biggest risk for a self-paced beginner course. If the cover slide looks plain, learners assume the content is plain and never reach Module 2. This is the WOW moment that justifies the entire feature.

**Independent Test**: Show the rendered cover + first three content slides of Module 1 to five people who have never seen the course. ≥ 4 of 5 describe it (unprompted) with at least one of: "polished", "professional", "modern", "fun", "premium", or equivalent. None describe it as "plain", "default", or "PowerPoint-looking".

**Acceptance Scenarios**:

1. **Given** the rendered PPTX of Module 1, **When** a non-technical reviewer sees the cover slide for the first time, **Then** the slide communicates the module title, module number, course name, and a single visual focal point (icon, illustration, or hero shape) without text crowding.
2. **Given** any content slide in Module 1, **When** the reviewer scans for ≤ 5 seconds, **Then** they can name the slide's one main point from the visual hierarchy alone (title size, accent color, single highlighted element).
3. **Given** the rendered HTML version, **When** a learner opens it on a 13-inch laptop screen, **Then** all text on every slide is legible without zooming and no element overflows the slide canvas.

---

### User Story 2 — Consistent design system across all 8 beginner modules (Priority: P1)

A learner moves from Module 1 to Module 8 over a weekend. Every deck shares the same visual identity: same fonts, same accent color, same cover-slide pattern, same "Show me" / "Try it yourself" / "Definition of done" slide treatments, same footer, same page-number style. The course feels like one book, not eight pamphlets.

**Why this priority**: Inconsistency is the second-fastest way to break the "premium" feeling. P1 because it is the only thing that turns eight one-off pretty decks into a real product.

**Independent Test**: Open all eight rendered PPTX files side-by-side in thumbnail view. A reviewer can confirm: same cover layout, same recurring section-divider style, same callout-box style for "Show me" / "Try it yourself" / "Reflect", same footer text + page numbers, same color palette, same typography pair.

**Acceptance Scenarios**:

1. **Given** all eight beginner decks, **When** rendered through the existing build pipeline, **Then** they share one named design system (theme + palette + typography + slide templates) defined in a single source so changes propagate to every deck.
2. **Given** the same recurring lesson section (e.g. "Show me", "Try it yourself", "Reflect", "Definition of done"), **When** it appears in any module, **Then** it uses the same slide template (background, accent stripe, icon, heading style).

---

### User Story 3 — Visuals carry meaning, not decoration (Priority: P1)

Every module's key concept is reinforced with at least one purposeful visual element (diagram, before/after, callout, code/output split, icon set) — not stock decoration. A learner who only looks at the visuals can still recall the module's main idea.

**Why this priority**: This is what separates "pretty" from "wow". Pretty = nice colors. Wow = the picture teaches the lesson.

**Independent Test**: For each of the 8 modules, identify at least one teaching visual (diagram, side-by-side, annotated terminal, callout) that did not exist before this feature. Remove all body text from that slide and ask a reviewer what the slide is teaching — they can answer correctly from the visual alone in ≥ 6 of 8 cases.

**Acceptance Scenarios**:

1. **Given** any beginner module, **When** the deck is reviewed, **Then** it contains at least one new purposeful visual element that teaches (not decorates).
2. **Given** the visuals across all 8 modules, **When** reviewed as a set, **Then** they use a shared visual vocabulary (same icon family, same diagram style, same annotated-terminal treatment) rather than mixed styles.

---

### User Story 4 — The build pipeline still works on the existing one command (Priority: P1)

A maintainer runs `./slides/deploy-pptx.sh` (and `--all` / `--pdf` / `--html`) on a clean machine and gets the same exit code 0 and the same set of output artifacts, only prettier. No new mandatory tooling, no new mandatory accounts, no new mandatory network calls beyond what the current pipeline already requires.

**Why this priority**: The course is shipped via this one script. If the polish pass breaks the build, the course breaks. P1 because regression here invalidates Stories 1–3.

**Independent Test**: On a clean checkout, `./slides/deploy-pptx.sh --all` produces PPTX + PDF + HTML for all eight beginner decks (and the existing intermediate decks) with no errors, in time ≤ 150% of the pre-polish baseline build time.

**Acceptance Scenarios**:

1. **Given** the post-polish repo, **When** `./slides/deploy-pptx.sh` is run, **Then** all eight beginner decks render to PPTX successfully.
2. **Given** the post-polish repo, **When** `./slides/deploy-pptx.sh --all` is run, **Then** PDF and HTML outputs also succeed and look visually identical to the PPTX (same fonts, same colors, same layout).
3. **Given** the post-polish repo, **When** the intermediate decks (`slides/part-01..10-*.md`) are rendered, **Then** they still render successfully even if they have not yet adopted the new design system.

---

### User Story 5 — Accessibility & projection-readiness (Priority: P2)

The polished decks remain readable in a room with a projector and a back-row attendee, and meet baseline accessibility for colorblind learners and screen-reader users of the PDF.

**Why this priority**: The course doubles as a live-workshop deliverable (per spec 002, User Story 3). P2 because the primary path is self-paced reading, but a deck that fails on a projector loses half the audience.

**Independent Test**: 
- Render any module to PDF, project at 1920×1080, walk to the back of an 8-meter room — body copy is still readable.
- Run the color palette through a colorblind simulator (deuteranopia + protanopia) — no information is conveyed by color alone.
- Body text contrast ratio against background ≥ 4.5:1 on every slide template.

**Acceptance Scenarios**:

1. **Given** any slide template, **When** body text is measured against its background, **Then** the contrast ratio is ≥ 4.5:1 (WCAG AA).
2. **Given** any slide that uses color to convey meaning (e.g. red = danger, green = ok), **When** viewed in grayscale, **Then** the meaning is still recoverable from shape, label, or position.

---

### Edge Cases

- A slide currently exceeds the canvas vertically (long code block, long bullet list). After polish, it MUST either fit, split into two slides, or scroll-shrink — never overflow silently.
- A learner running the build on a machine with no internet access (Marp's Chromium pre-cached): the build MUST still succeed; the new theme MUST NOT introduce a new mandatory network-fetched font or asset.
- A learner who opens the PPTX in Keynote or LibreOffice Impress (not PowerPoint): fonts MUST fall back gracefully to a system font of the same class (sans-serif / monospace) without breaking layout.
- A module's existing text content is already at the seat-time budget edge (per spec 002 SC-008). The polish pass MUST NOT add new required slides that push the module over budget; visual replacements of existing text slides are preferred.
- A facilitator projects the deck and presses "B" to black out the screen. The polished theme MUST NOT depend on any animation or transition that breaks when paused.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The beginner slide decks (`slides/beginner/part-01..08-*.md`) MUST adopt a single shared, named design system (theme + color palette + typography pair + slide templates + iconography) defined in one source location, so changes propagate to all eight decks.
- **FR-002**: The design system MUST define, at minimum, these reusable slide templates: cover/title, section divider, "What you'll learn" (learning objectives), "Show me" (annotated terminal / code+output), "Try it yourself" (steps), "Reflect" / "Definition of done", and closing/next-up.
- **FR-003**: Each of the eight beginner decks MUST gain at least one new purposeful teaching visual (diagram, before/after, annotated terminal, side-by-side, or icon-driven concept map) that did not exist before this feature.
- **FR-004**: The design system MUST use a consistent icon family (one source, one visual style) and a consistent diagram style across all 8 decks.
- **FR-005**: All slide templates MUST meet WCAG AA body-text contrast (≥ 4.5:1) against their background.
- **FR-006**: The design system MUST NOT rely on color alone to convey meaning; any color-coded element MUST also carry a shape, icon, label, or position cue.
- **FR-007**: All decks MUST continue to render successfully through the existing `slides/deploy-pptx.sh` pipeline in PPTX, PDF, and HTML modes with no new mandatory CLI flags.
- **FR-008**: The polish pass MUST NOT introduce new mandatory external network dependencies at build time beyond what the existing pipeline already requires (Marp CLI + bundled Chromium).
- **FR-009**: Fonts used by the design system MUST be either (a) bundled with the repository under a license compatible with MIT redistribution, or (b) standard system fonts with a documented fallback chain.
- **FR-010**: The polish pass MUST preserve the existing curriculum content of each beginner module: learning objectives, exercise instructions, terminal transcripts, and "Definition of done" criteria remain semantically identical (wording may be tightened for layout, but meaning is preserved).
- **FR-011**: The polish pass MUST NOT push any beginner module past its per-module minute budget defined in spec 002 (Module 01 = 20 min, 02 = 25 min, 03 = 30 min, 04 = 25 min, 05 = 30 min, 06 = 25 min, 07 = 25 min, 08 = 30 min; total target 210 min, range 200–240).
- **FR-012**: Every slide MUST keep its content within the canvas at the deck's declared size (16:9) — no silent overflow.
- **FR-013**: The intermediate decks (`slides/part-01..10-*.md`) MUST continue to render through the same pipeline without regression, even if they have not yet adopted the new design system.
- **FR-014**: The design system MUST be documented in a single short reference (location TBD by `/speckit.plan`) so a future contributor can apply it to the intermediate decks or to a new module without reverse-engineering the theme.
- **FR-015**: Every deck's cover slide MUST display, at minimum: module number, module title, course name, and one visual focal element (icon, illustration, or hero shape).
- **FR-016**: Every deck MUST carry a consistent footer/header treatment (course name + module number + page number) on all non-cover slides.
- **FR-017**: Recurring section types ("Show me", "Try it yourself", "Reflect") MUST be visually identifiable at a glance via a consistent template (background, accent stripe, or icon).

### Key Entities *(include if feature involves data)*

- **Design System**: The single, named source-of-truth bundle covering theme, color palette, typography pair, slide templates, iconography, and diagram style. Lives in one location in the repo; referenced by all eight beginner decks.
- **Slide Template**: A reusable layout for a recurring lesson section (cover, section divider, "Show me", "Try it yourself", "Reflect", "Definition of done", closing). Defined once in the design system, instantiated many times across decks.
- **Teaching Visual**: A purposeful visual element (diagram, before/after, annotated terminal, side-by-side, icon-driven concept map) that carries lesson meaning, not decoration. At least one per module.
- **Build Artifact Set**: The set of files produced by `slides/deploy-pptx.sh` for one deck — PPTX (always), PDF (optional), HTML (optional). The polish pass is judged against this rendered output, not the Markdown source.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a blind first-impression test of the rendered cover + first three content slides of Module 1, ≥ 4 of 5 reviewers describe the deck (unprompted) as "polished", "professional", "modern", "premium", or equivalent — and 0 of 5 describe it as "plain" or "default-looking".
- **SC-002**: 100% of the eight beginner decks share the same named design system (theme + palette + typography + recurring slide templates) verifiable by side-by-side thumbnail review.
- **SC-003**: Each of the eight beginner decks contains ≥ 1 new purposeful teaching visual that did not exist before this feature (8 of 8 modules covered).
- **SC-004**: When body text from any one chosen "teaching visual" slide per module is hidden, ≥ 6 of 8 reviewers can correctly state the slide's main idea from the visual alone.
- **SC-005**: 100% of slide templates meet WCAG AA body-text contrast (≥ 4.5:1).
- **SC-006**: The build command `./slides/deploy-pptx.sh --all` completes successfully on a clean checkout in ≤ 150% of the pre-polish baseline wall-clock time.
- **SC-007**: 0 slides across all eight beginner decks overflow the 16:9 canvas in the rendered PPTX.
- **SC-008**: 100% of color-coded UI elements remain interpretable in grayscale (verified by simulator pass on at least one slide per template).
- **SC-009**: Total seat-time per module, as estimated against spec 002's per-module budget, is unchanged (±0 minutes target; ±2 minutes tolerance per module; never above the original ceiling).
- **SC-010**: A new contributor can read the design-system reference doc once and produce a compliant ninth-module deck without further guidance, verified by one dry-run with a non-author.

---

## Assumptions

- The polish target is **`slides/beginner/`** (the eight beginner Marp decks). The intermediate decks under `slides/*.md` are explicitly out of scope for v1 but the design system produced here MUST be reusable for them later (FR-014).
- The current toolchain stays: **Marp** Markdown source rendered by `slides/deploy-pptx.sh` to PPTX (primary), PDF and HTML (optional). No migration to a different slide tool is assumed.
- "Shine and wow" is interpreted as **a coherent premium visual identity + at least one purposeful teaching visual per module + WCAG AA accessibility + projection-readiness**, not flashy animations, video, or interactive widgets — the PPTX target rules those out.
- Curriculum, learning objectives, exercise content, and per-module minute budgets defined in spec 002 are **fixed inputs** to this polish pass. This feature is design + visual rewrites only, not a curriculum revision.
- The repo's MIT license applies; any new font, icon set, illustration, or asset added by this feature must be MIT-compatible (or public domain / SIL OFL / Apache-2.0 with attribution).
- Reviewers for the qualitative success criteria (SC-001, SC-004) can be sourced from at least five non-author readers; access to such reviewers is assumed available to the implementer.
- A "pre-polish baseline" build time exists or can be measured before any change is made (SC-006).
- The polish pass MAY tighten wording on existing slides where layout demands it, as long as meaning is preserved (FR-010). Substantive content changes are out of scope.

---

## Out of Scope (v1)

- Re-theming the **intermediate** decks (`slides/part-01..10-*.md`). They must keep building, but adopting the new design system for them is a follow-up feature.
- Animations, transitions, embedded video, or interactive widgets.
- Localization / translations of slide content.
- Re-recording or producing companion video walkthroughs.
- Generating presenter notes — unless they exist today; the polish pass does not invent new ones.
- Changing exercise content, quiz content, capstone scope, or any spec-002 acceptance criteria.
- Migrating away from Marp or from the PPTX output target.

---

## Dependencies

- Spec 002 (`specs/002-claude-beginner-course`) defines the curriculum, per-module minute budget, and the existence of the eight beginner decks under `slides/beginner/`. This feature consumes those as fixed inputs.
- The build pipeline `slides/deploy-pptx.sh` and its Marp-CLI / Chromium dependency chain.
- The repo-wide MIT license, which constrains acceptable third-party font / icon / illustration licenses.
