# Contract: Slide Templates (the 7 recurring layouts)

**Feature**: Slide Decks That Shine
**Branch**: `003-slide-wow-polish`
**Date**: 28 May 2026

Each contract below defines what a deck author MUST and MUST NOT do when instantiating a recurring slide template from the `wow-beginner` design system. Contracts are enforced by PR-time review and (where listed) by automated checks.

## Conventions

- **CSS class**: how the template is invoked in deck Markdown (Marp supports `<!-- _class: tpl-name -->` directives per slide).
- **Required slots**: content that MUST appear; missing slots = template violation.
- **Optional slots**: content that MAY appear.
- **Forbidden**: things explicitly out of bounds for this template.
- **A11y**: accessibility constraint this template adds beyond the global Palette contract.
- **Verification**: how a reviewer (or script) confirms conformance.

---

## Template 1 — Cover (`.tpl-cover`)

The first slide of every deck. The "wow" moment (SC-001).

**Required slots**:
- `module-number`: e.g. "Module 01"
- `title`: the module title from spec 002
- `course-name`: literal string "Claude Code 101 · Beginner Workshop"
- `hero-visual`: one icon (from `IconSet`) at `size_class_px=64` OR one inline-SVG illustration occupying the right ~40% of the canvas

**Optional slots**:
- `subtitle`: ≤ 12 words, derived from the deck's existing intro line
- `instructor`: name + endorsement (mirrors intermediate-deck convention)

**Forbidden**:
- Bulleted lists.
- More than one hero visual.
- Body paragraphs (anything > one subtitle line).
- Use of `--success` or `--danger` (cover is neutral).

**A11y**:
- Title font-size MUST be ≥ 56 px.
- Hero visual MUST have an SVG `<title>` element OR be marked decorative (`aria-hidden="true"`).

**Verification**:
- Manual: looks like a book cover, not a bullet slide.
- SC-001 reviewer panel runs on Module 01's cover.

---

## Template 2 — Section Divider (`.tpl-divider`)

Optional. Used to mark a transition inside a longer module (Modules 05 and 08 likely candidates).

**Required slots**:
- `label`: ≤ 6 words, all-caps small, in `--muted`
- `accent-stripe`: the design-system accent stripe, top or left edge

**Optional slots**:
- `icon`: one Lucide icon, `size_class_px=48`

**Forbidden**:
- Body text other than `label`.
- More than 3 dividers in any single deck (would fragment the lesson).

**A11y**: stripe MUST NOT be the only navigation cue — the `label` text carries the meaning.

**Verification**: visual check; no more than 3 per deck.

---

## Template 3 — What You'll Learn (`.tpl-objectives`)

Exactly one per deck. Contains the deck's stated learning objectives (verbatim from spec 002 — FR-010, research §6).

**Required slots**:
- `objectives-list`: a numbered list with 1–4 items, each ≤ 16 words. **Verbatim** copy from the deck's pre-polish "What you'll learn" section (or "Promise" in the case of decks that used that section name).

**Optional slots**:
- `duration-badge`: e.g. "20 min" — pulled from spec 002's per-module budget.

**Forbidden**:
- Adding, removing, or substantively rewording any objective.
- Mixing numbered and bulleted items.
- More than 4 objectives (would exceed pedagogical load defined in spec 002).

**A11y**: list items MUST be in semantic `<ol>` order; the numbered chips next to each item are decorative and MUST be `aria-hidden`.

**Verification**: diff against pre-polish source — token set MUST match.

---

## Template 4 — Show Me (`.tpl-show`)

One or more per deck. The annotated terminal / code+output layout. This is where the "teaching visual" often lives.

**Required slots**:
- `code-or-terminal block`: a fenced block (text or language-tagged), preserved verbatim.
- `annotation`: a short caption (≤ 20 words) explaining what to notice — placed in the right-rail callout, in `--muted`.

**Optional slots**:
- `caption`: a footer line crediting the demo source (e.g. "from `module-00-setup/`").

**Forbidden**:
- Modifying any command, output line, or path inside the verbatim block.
- More than 80 lines of code/terminal text per single Show-Me slide (split into two if needed).
- Inline images in place of code (code blocks remain text for searchability).

**A11y**:
- Terminal text MUST use `mono_family` at ≥ 22 px.
- The `$` prompt and the typed input MUST be visually distinguishable from output via weight or color (using `--ink` vs. `--muted`), with `$` consistently bold across all decks.

**Verification**:
- Diff: code/terminal block byte-identical to pre-polish.
- Slide-overflow check (SC-007).

---

## Template 5 — Try It Yourself (`.tpl-try`)

Exactly one per deck. The hands-on step list.

**Required slots**:
- `numbered-steps`: 1–5 items, each ≤ 14 words. **Verbatim** from the deck's pre-polish "Try it yourself" section.
- `success-criterion`: one sentence stating how the learner knows they're done — derived from the deck's existing "Definition of done" line for the relevant step.

**Optional slots**:
- `icon`: the `play` icon, top-right.

**Forbidden**:
- More than 5 steps (cognitive load ceiling).
- Adding steps not present pre-polish (FR-010).
- Removing a step's verbatim command (commands are part of the verbatim contract).

**A11y**: steps MUST be a semantic `<ol>`.

**Verification**: diff against pre-polish source for step text + commands.

---

## Template 6 — Reflect / Definition of Done (`.tpl-done`)

Exactly one per deck. The pass/fail self-check (Constitution Principle VI).

**Required slots**:
- `checklist`: 1–6 items, each ≤ 12 words. **Verbatim** copy from the deck's pre-polish "Definition of done" / "Reflect" section.
- `reflection-prompt`: one sentence inviting the learner to journal or note their takeaway — derived from existing source; new prompts forbidden.

**Optional slots**:
- `icon`: the `check` icon, top-right.

**Forbidden**:
- Adding or removing checklist items.
- Reordering checklist items (order is semantic — earlier items gate later ones).
- Using `--success` color until the learner ticks the box (the printed slide MUST render with neutral checkboxes; the green tint is reserved for live-presenter mode if any).

**A11y**: checkboxes MUST be `<input type="checkbox">` semantics in HTML (not plain Unicode dingbats) so screen readers announce them; in PPTX, equivalent unchecked-box glyphs are acceptable.

**Verification**: diff against pre-polish source; SC-005 contrast check.

---

## Template 7 — Closing / Next Up (`.tpl-next`)

Exactly one per deck. Bridges to the next module.

**Required slots**:
- `next-module-title`: the next module's title from spec 002. Module 08 (capstone) shows "You finished Claude Code 101" instead.
- `transition-prompt`: one sentence connecting this module's deliverable to the next module's promise — derived from spec 002 cross-module narrative; net-new prose forbidden.

**Optional slots**:
- `icon`: the `arrow-right` icon (or `award` for Module 08).

**Forbidden**:
- Calls-to-action unrelated to the next module (no marketing).
- More than two lines of text.

**A11y**: arrow icons MUST have `aria-label="Next module"` (or `aria-hidden="true"` if the title text already conveys it).

**Verification**: cross-reference next-module title against spec 002 module list.

---

## IconSet inventory (v1)

Exactly these 12 icons from Lucide (ISC), bundled under `slides/themes/icons/`:

| File | Used by template(s) | Used by module(s) |
|---|---|---|
| `terminal.svg` | tpl-show | 01, 02, 04, 08 |
| `lightbulb.svg` | tpl-show, tpl-divider | 03, 06 |
| `shield.svg` | tpl-show | 07 |
| `warning.svg` | tpl-show, tpl-done | 05, 07 |
| `check.svg` | tpl-done | all |
| `play.svg` | tpl-try | all |
| `pencil.svg` | tpl-show | 05, 06 |
| `eye.svg` | tpl-show | 04 |
| `book.svg` | tpl-cover | 06 |
| `file.svg` | tpl-show | 01, 04, 06 |
| `folder.svg` | tpl-show | 04, 08 |
| `arrow-right.svg` | tpl-next | all (except 08) |
| `award.svg` | tpl-next | 08 only |

(13 icons listed — `award.svg` is the Module-08 closer variant.)

---

## Global contract: things forbidden in any template

- Inline `style="..."` attributes overriding palette colors.
- `<font>` tags, `<center>` tags, or other HTML you wouldn't put in 2026 web.
- Remote URLs in `<img src="...">` or `url(...)` CSS values.
- Emoji used as load-bearing UI (icons must be SVG; emoji may appear inside verbatim spec-002 prose if they were already there).
- Animation directives (CSS `@keyframes`, Marp transition front-matter beyond the default).
- Per-deck overrides of the `palette` or `typography_pair`.
