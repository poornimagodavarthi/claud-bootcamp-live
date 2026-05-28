# Phase 0 — Research & Decisions

**Feature**: 004 Intermediate Course Content Polish
**Date**: 28 May 2026

All five `/speckit.clarify` questions were resolved before planning. This document records the remaining design decisions, the chosen approach, the rationale, and the alternatives considered.

---

## Decision 1 — Theme architecture

**Decision**: Sibling file `slides/themes/wow-intermediate.css` that begins with `@import url('./wow-beginner.css');` and then adds a single new block: the `.tpl-demo` template class for the Live-demo-flow slide.

**Rationale**: The clarification answer (Q3 = A) forces this shape. Single source of truth for palette + typography prevents drift; adding only `tpl-demo` minimises new CSS surface area; intermediate decks switch audience with a one-line front-matter change (`theme: wow-intermediate`).

**Alternatives considered**:

- Unified theme with body-class modifier (`.audience-intermediate`): rejected because Marp's `theme:` directive is the canonical audience switch in this project; mixing a single theme with class-based audience switching makes deck source less self-describing.
- Two fully independent themes: rejected because palette drift would break SC-002 (uniform visual identity across 18 decks).

**Implementation note**: The `tpl-demo` class targets the Live-demo-flow slide — a numbered procedure with a hero icon (the `play` Lucide icon). Visual treatment: monospace step numbers on a soft-accent strip down the left edge; the demo's title in the heading slot; sub-points as muted body text.

---

## Decision 2 — Per-module teaching SVG concepts

**Decision**: 10 SVGs, one per module, placed on each module's Concepts slide. Concept matrix:

| Module | Title | Visual concept | Hero icon |
|---|---|---|---|
| 01 | Welcome / Setup / Mindset | The TCC pair-programming loop: human-as-PM → Claude-as-engineer → review → merge | `terminal` |
| 02 | Prompting Like a Tech Lead | 4-part prompt anatomy: Context → Constraints → Examples → Output spec | `pencil` |
| 03 | CLAUDE.md | CLAUDE.md cheat-sheet card: 5 stacked sections with one-line purpose each | `book` |
| 04 | Best-of-N | 3 candidate folders → scorecard rubric → winner badge | `play` |
| 05 | Testing & Debugging | Red → Green → Refactor cycle with bug-report arrow into Red | `shield` |
| 06 | Git Workflows | Branch tree: main → feature/* → review badge → merge commit | `folder` |
| 07 | Multimodal / Screenshot-to-UI | Three-pane: PNG mock → mermaid wireframe → rendered UI | `eye` |
| 08 | Refactoring & Docs | Dead-code map (faded boxes) → constrained-refactor arrow → tightened module + doc badge | `file` |
| 09 | Skills & Workflows | Skill catalogue tiles (3×2 grid) → GCOE checkmark on each | `lightbulb` |
| 10 | Production Readiness | 5-axis radar chart with axes labelled: Security, Reliability, Performance, Observability, Operability | `award` |

**Rationale**: Each visual captures the module's single most-important mental model. The visuals are independent (no cross-references that would couple modules) per the spec Open Question default. Hero icons are drawn from the 13 already shipped in `slides/themes/icons/`.

**Alternatives considered**:

- Two visuals per module (one for Concepts + one for Live-demo-flow): rejected per Q4 = A.
- Cross-referencing visuals (Module 5's debug loop echoing Module 4's BoN rubric): rejected per Open Questions default — maintenance burden too high for the carry value.

**SVG technical specs**:

- viewBox `0 0 800 450` (16:9 at slide content area)
- Colours: only palette tokens declared in wow-beginner (`--bg`, `--ink`, `--muted`, `--accent`, `--accent-soft`, `--success`, `--danger`, `--rule`).
- Typography: inline `<text>` uses `font-family="Inter Variable, system-ui, sans-serif"` to match deck body type.
- Accessibility: every SVG carries `<title>` (one-sentence lesson statement) and `<desc>` (longer screen-reader description).
- Grayscale recoverability: every element conveys meaning via shape + label, never hue alone.

---

## Decision 3 — Content polish boundary enforcement

**Decision**: Author a new audit script `scripts/check-verbatim-blocks.sh` that runs two passes per deck:

1. **Verbatim grep pass**: For each of the 5 protected-block categories (Promise numbered list, Suggested-Claude-Code-prompts fences, Deliverable checklist, Definition-of-done lines, Step-by-step-lab numbered steps), extract the pre-polish text from `git show HEAD:slides/part-NN-*.md` and assert exact substring match in the working-tree version. Exit non-zero on any mismatch.
2. **Word-count delta pass**: For each of the 5 editable sections (Why-this-matters, Concepts, Common-mistakes, Instructor-notes, Transition), compute `wc -w` on the pre-polish vs post-polish extracted blocks. Assert delta ≤ 0. Print the table.

**Rationale**: Q2 (tighten-only) and Q5 (Common-mistakes editable) together create a precise pass/fail line; a single audit script captures both rules and runs in <2 s per deck. The script's output table is the evidence for SC-010.

**Alternatives considered**:

- Use `git diff --word-diff` and manual review: rejected because human review of 10 decks × 13 sections is slow and error-prone.
- Per-bullet `<!-- verbatim -->` markup: rejected per Q5 — adds source-markdown noise for negligible safety gain.

**Implementation note**: The script extracts section content using awk patterns anchored on the H2 headers (each deck uses a stable set of H2 strings; this is what makes the 14-section constitutional anatomy machine-readable). The pre-polish baseline is `git show HEAD:` at the merge-base of branch `004-intermediate-content-polish` with `main`.

---

## Decision 4 — Build output reorganisation strategy

**Decision**: Patch `slides/deploy-pptx.sh` so that the 3 Marp invocations write directly into `slides/dist/<audience>/<format>/` using a small case-distinction: if the input deck path matches `slides/beginner/part-*.md` the audience is `beginner`; otherwise (`slides/part-*.md`) the audience is `intermediate`. Each format invocation (`--pptx`, `--pdf`, `--html`) gets a `--output` flag pointing at the per-format subdirectory.

**Rationale**: Q1 (= A) chose the audience-first layout. Patching at the Marp-invocation level is minimally invasive; no glob or post-build mv step is needed; and the patch is reviewable as 3 hunks in `deploy-pptx.sh`.

**Alternatives considered**:

- Build into the existing flat `slides/dist/` and post-build `mv` into the new layout: rejected because partial failure leaves the directory in an inconsistent state.
- Two separate top-level invocations (one for each audience): rejected because it doubles the Chromium launch cost (~6 s × 2) and would push build time past the 1.5× ceiling.

---

## Decision 5 — Overflow-check extension

**Decision**: Extend `scripts/check-slide-overflow.sh` so it accepts an optional `--budget N` flag and scans both `slides/dist/intermediate/html/*.html` and `slides/dist/beginner/html/*.html`. The intermediate budget defaults to 22 content elements per slide; the beginner budget stays at 18 (unchanged).

**Rationale**: The intermediate decks pack 13 H2 sections of denser content (e.g., 8-step labs, 6-row scoring tables). The feature-003 budget of 18 was sized for beginner density; raising the intermediate ceiling to 22 reflects measured pre-polish content, not a relaxation of standards. SC-007 still requires 0 overflows at that budget.

**Alternatives considered**:

- Keep one global budget: rejected — beginner decks would gain unnecessary headroom (false-negative risk on overflow).
- Budget per template class (`tpl-show` → 18, `tpl-demo` → 22): rejected — too granular; per-audience is the smallest meaningful split.

---

## Decision 6 — Beginner-deck immutability enforcement

**Decision**: Add a pre-commit check (informal, run by hand at PR time, not a git hook): `git diff --stat $(git merge-base HEAD main) -- slides/beginner/` MUST return zero lines. The audit script (`check-verbatim-blocks.sh`) runs this check as a "phase 0" before scanning intermediate decks; non-zero diff aborts.

**Rationale**: FR-012 + SC-002 require the 8 beginner decks to remain byte-identical. Putting the check inside the audit script means every contributor running the audit catches an accidental beginner edit before opening a PR.

**Alternatives considered**:

- Git pre-commit hook: rejected — workshop authors include non-Git-comfortable instructors; adding mandatory hooks is friction.
- CI-only enforcement: deferred (no CI configured today); local audit covers the gap.

---

## Decision 7 — Module 1 cover instructor-name treatment

**Decision**: Per the spec Open Questions default, keep the instructor name on the Module-1 cover only as part of the workshop opening; remove from Modules 2–10 covers (where pre-polish drafts include it).

**Rationale**: Repeated instructor credit across 10 covers is visual noise. The opening (Module 1) sets the speaker; subsequent modules use the bootcamp footer (`Claude Code Bootcamp · Day 1 · Module NN`) as the persistent attribution.

**Alternatives considered**:

- Keep on every cover: rejected — repetition adds no information; SC-002 visual coherence prefers a single header treatment.
- Remove entirely (none of 10 covers): rejected — Module 1 cover is the deck of record for "who is teaching today" and is the natural place.

---

## Decision 8 — Polish change-log capture

**Decision**: For each deck, append a `<!-- polish-log:` HTML comment at the very bottom (after the last H2 section, before EOF) listing the editable sections touched. Format:
```
<!-- polish-log: 2026-05-29
  why-this-matters: -47 words, -2 filler clauses
  concepts: -23 words, -1 redundant analogy
-->
```
This is metadata for the audit script to cross-check against its computed deltas.

**Rationale**: Lightweight provenance; survives Marp build (HTML comments are stripped from rendered output); makes the verbatim-audit pass two consistency check possible.

**Alternatives considered**:

- Separate `polish-log.md` per deck: rejected — duplicates the source-of-truth principle.
- No log at all: rejected — the audit's word-count deltas would lose human-readable rationale.

---

## Decision 9 — `tpl-demo` visual treatment

**Decision**: `tpl-demo` styles a numbered procedure with: heading slot at top, hero `play` icon at top-right, an accent-soft vertical strip down the left edge containing oversized step numbers, and the step description in body type to the right of each number. No code blocks within `tpl-demo` slides — demo flow stays at the conceptual level; code lives in `tpl-show` slides.

**Rationale**: The Live-demo-flow section is the one structural difference between intermediate and beginner anatomies. Giving it its own template (a) makes the deck self-describing in the source, (b) prevents the demo from being mistaken for a static checklist (tpl-done style), and (c) keeps tpl-show reserved for code/transcript content.

**Alternatives considered**:

- Reuse `tpl-objectives` (numbered list visual): rejected — objectives are *promises*, demo flow is *procedure*; reusing the visual would muddle the rhetorical role.
- Reuse `tpl-show`: rejected per Q3 = A (the chosen Option introduces exactly one new class for a reason).

---

## Decision 10 — Reviewer-panel protocol carry-over

**Decision**: Reuse the protocols from `specs/003-slide-wow-polish/reviewer-panel-results.md` verbatim for SC-001 (n=5 first-impression), SC-004 (n=8 visual-only comprehension), SC-008 (deuteranopia/protanopia simulation). Substitute the intermediate cover deck and the 10 teaching SVGs as the artefacts under review.

**Rationale**: The protocols were designed in feature 003 to be reusable for any future course. Re-authoring them here would risk methodological drift across the two courses. The protocols live in `specs/003-…` and are referenced by `specs/004-…/quickstart.md` rather than copied — keeps a single source of truth.

**Alternatives considered**:

- Re-author protocols inside this feature: rejected — duplication.
- Skip human panels entirely and rely on auto-checks alone: rejected — SC-001 and SC-004 require subjective judgement that no automated tool delivers reliably.

---

## All NEEDS CLARIFICATION resolved

None remain. The Open Questions section in the spec carries two low-impact items, both with documented defaults applied (Decision 7 above; Decision 2 for visual cross-referencing).
