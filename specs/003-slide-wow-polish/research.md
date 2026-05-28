# Phase 0 — Research

**Feature**: Slide Decks That Shine — Visual & Pedagogical Polish Pass
**Branch**: `003-slide-wow-polish`
**Date**: 28 May 2026

Resolves every unknown raised by `Technical Context` in [plan.md](plan.md). Each entry follows: **Decision → Rationale → Alternatives considered**.

---

## 1. How to attach a custom theme to Marp decks without breaking the existing build

**Decision**: Add `--theme-set` to the Marp CLI invocations inside [slides/deploy-pptx.sh](../../slides/deploy-pptx.sh), pointing at the directory `slides/themes/`. Each beginner deck opts in via front-matter `theme: wow-beginner` (the `@theme` name declared inside `slides/themes/wow-beginner.css`). Intermediate decks keep `theme: default` and are unaffected.

**Rationale**:

- `--theme-set` is Marp CLI's official mechanism for registering one-or-more custom themes; the theme is selected per deck via front-matter, which is exactly the opt-in model spec FR-013 requires (intermediate decks must keep building).
- The flag is backward-compatible: passing `--theme-set <dir>` on a deck that declares `theme: default` is a no-op.
- One script edit (3 lines) is the minimum change that delivers FR-001 (single source of truth) across all 8 beginner decks.

**Alternatives considered**:

- *Inline `<style>` blocks in each deck*: rejected — duplicates the design system across 8 files, breaks FR-001 (single source of truth).
- *Build a Marp theme npm package and publish it*: rejected — introduces a new runtime dependency and a new release artifact, violates Constitution Principle X.
- *Switch to Reveal.js / Slidev / Spectacle*: rejected — out of scope per spec Out-of-Scope §, breaks Constitution Principle III.

---

## 2. Color palette + typography pair (the "premium look" decision)

**Decision**: A three-color palette plus one accent, paired with **Inter** (body & headings) and **JetBrains Mono** (code/terminal):

| Token | Hex | Role | Contrast vs. background |
|---|---|---|---|
| `--bg` | `#FAF7F2` (warm cream) | Slide background | — |
| `--ink` | `#1B1B1F` (near-black) | Body & headings | 16.8:1 (AAA) |
| `--muted` | `#5A5A66` | Secondary text, captions | 6.9:1 (AAA) |
| `--accent` | `#D9531E` (Anthropic-aligned coral) | Highlights, accent stripes, focus elements | 4.9:1 (AA) on `--bg` |
| `--accent-soft` | `#FCE6DA` | Callout backgrounds | — |
| `--success` | `#1F7A4D` | "OK" / done state (paired with check icon) | 5.0:1 (AA) |
| `--danger` | `#9A2B2B` | "Never paste this" / warning (paired with shield icon) | 7.4:1 (AAA) |

Typography pair:

- **Inter Variable** (SIL OFL 1.1) — body, headings, captions.
- **JetBrains Mono Variable** (SIL OFL 1.1) — code, terminal transcripts, file paths.

Both fonts shipped as `.woff2` under `slides/themes/fonts/` and referenced via local `@font-face` declarations in `wow-beginner.css` using relative URLs that work under Marp's `--allow-local-files`.

**Rationale**:

- Warm cream + near-black ink + single coral accent gives the "premium book" feel that satisfies SC-001 ("polished / professional / premium" unprompted) without looking like a generic SaaS slide template.
- Inter + JetBrains Mono is the dominant modern dev-content pair (used by Linear, Vercel, GitHub docs, Stripe docs). Both are free, libre, and OFL-licensed — compatible with the repo's MIT license per FR-009.
- Every text token's contrast is verified ≥ 4.5:1, satisfying FR-005 and SC-005. `--success` and `--danger` carry icons + labels in templates, so meaning is never color-only (FR-006, SC-008).
- Variable fonts ship as one file each (~120 KB woff2 subsetted to Latin) — total bundled font weight ≈ 240 KB, negligible repo-size cost.

**Alternatives considered**:

- *Google Fonts via CDN*: rejected — adds a build-time network call, violates FR-008.
- *System-font-only stack* (no bundled font): rejected — fails the "premium" first-impression target (SC-001) because output varies wildly between presenter machines (San Francisco on macOS vs. Segoe UI on Windows vs. DejaVu on Linux).
- *Anthropic's official typeface (e.g., Styrene)*: rejected — proprietary, not freely redistributable under MIT.
- *Pure-black background "dark mode"*: rejected — fails projection-readiness for many lecture rooms with high ambient light; warm cream reads better in mixed lighting and prints cleaner.

---

## 3. Iconography & diagram style

**Decision**: 

- **Icons**: Lucide (ISC license), bundled as inline SVG files under `slides/themes/icons/`. Single stroke weight (1.75px), single style across all decks. ~12 icons selected upfront (terminal, lightbulb, shield, warning, check, play, pencil, eye, book, file, folder, arrow-right).
- **Diagrams**: hand-authored inline SVG per module, stored under `slides/beginner/assets/<NN>-<slug>.svg`. One shared visual vocabulary documented in [contracts/slide-template-contracts.md](contracts/slide-template-contracts.md): rounded rectangles (8 px radius), 2 px strokes in `--ink`, fills in `--accent-soft` or `--bg`, arrows with simple triangular heads.

**Rationale**:

- Lucide is the de-facto modern icon family; one consistent visual style across all 8 decks satisfies FR-004 and SC-002.
- Inline SVG renders identically in PPTX, PDF, and HTML (Marp embeds SVG via Chromium → no rasterization surprises), satisfying SC-007 and the build-pipeline contract.
- Hand-authored SVG diagrams avoid pulling Mermaid CLI or PlantUML into the toolchain — both would violate Constitution Principle X. One SVG per module (8 total) is a tractable authoring budget.

**Alternatives considered**:

- *Phosphor Icons (MIT)*: tied with Lucide — Lucide picked for slightly tighter visual weight at slide scale.
- *Heroicons*: rejected — limited single style, less coverage of the dev/security iconography we need ("shield", "terminal").
- *Mermaid diagrams*: rejected — would require either pre-rendering (extra build step) or a Marp plugin (extra dep). Inline SVG is one less moving part.
- *Stock illustrations (unDraw, Storyset)*: rejected — visual style varies, breaks FR-004 "one icon family / one diagram style".

---

## 4. How to verify "no slide overflows the canvas"

**Decision**: Ship `scripts/check-slide-overflow.sh` — a small Bash script that:

1. Runs `slides/deploy-pptx.sh --html` (HTML build is required for inspection).
2. For each rendered HTML file under `slides/dist/html/beginner/`, greps for the inline CSS marker Marp adds to slides whose content was forced to overflow.
3. Exits non-zero with a list of offending `<deck>:<slide-number>` pairs if any overflow is found.

This satisfies SC-007 ("0 slides overflow") as an automatable check.

**Rationale**:

- Marp's HTML output is the only render target that exposes per-slide layout in a grep-able form. PPTX is binary; PDF requires a PDF parser.
- A Bash + grep check has zero dependencies beyond what the existing pipeline already needs.
- Run by maintainers (and optionally by future CI) before merging any deck change.

**Alternatives considered**:

- *Visual diff via Playwright screenshots*: rejected — adds Playwright as a dev dep, overkill for one boolean check.
- *Manual review only*: rejected — SC-007 says "0 slides" across 140+ slides; humans miss one. Automation is cheap.

---

## 5. Reviewer-panel methodology for qualitative SCs (SC-001, SC-004)

**Decision**:

- **SC-001 (first-impression panel)**: 5 reviewers, mix of technical + non-technical, never seen the deck before. Shown the cover + first three content slides of Module 1, rendered to PNG at 1920×1080. Asked one open question: "Describe this in three adjectives." Recorded verbatim. PASS if ≥ 4 of 5 mention at least one of {polished, professional, modern, premium, fun, clean, polished, sharp}; FAIL if any mention "plain", "default", "powerpointy", "amateur".
- **SC-004 (visual-only comprehension panel)**: 8 reviewers, technical literacy assumed. For each of the 8 modules, the chosen "teaching visual" slide is shown with body text blanked out (only the visual + slide title visible). Reviewer asked: "What is this slide teaching?" PASS if ≥ 6 of 8 reviewers state the lesson's main idea correctly.

Reviewer pool: drawn from non-author colleagues, target-audience peers, or technical-writing/UX reviewers available to the implementer. Documented as Reviewer Set R1 in [quickstart.md](quickstart.md).

**Rationale**:

- "Shine and wow" is inherently a perception target; the only honest measurement is a reviewer panel. Numeric thresholds (≥ 4 of 5, ≥ 6 of 8) keep the SCs verifiable.
- Open-question protocol prevents leading the witness. Adjective recording lets the SC be re-run by anyone.
- Panel sizes (5 and 8) are small enough to be feasible, large enough to give a defensible signal.

**Alternatives considered**:

- *A/B test in production*: rejected — no telemetry on slide reception; out of scope.
- *Single-author self-review*: rejected — invalidates the "shine and wow" claim; reviewer must not be the polish author.
- *Statistical survey (n=50+)*: rejected — overkill for a course of this size.

---

## 6. How to keep meaning preserved while tightening layout (FR-010 enforcement)

**Decision**: For every text edit to a beginner deck during the polish pass, the author MUST preserve, verbatim: (a) the deck's stated learning objectives in "What you'll learn", (b) every command in "Show me", (c) every step in "Try it yourself", (d) every item in "Definition of done", (e) the capstone scope of Module 08 (per spec 002 clarification). All other prose MAY be tightened — but the implementer keeps a side-by-side diff on every PR and the reviewer's first check is "do the verbatim-protected blocks match?"

**Rationale**:

- FR-010 forbids semantic content change. The listed five blocks are the spec-002-anchored contracts cross-checked by the assessment artifacts (quiz, capstone smoke check). They cannot drift.
- Prose tightening is the dominant editing operation needed to fit polished layouts; banning it would block the feature.

**Alternatives considered**:

- *Forbid all prose changes*: rejected — leaves wordy slides crammed in tight layouts, defeating the polish goal.
- *Allow any change at author's discretion*: rejected — would break cross-artifact consistency (Constitution Principle IX).

---

## 7. Build-time performance budget

**Decision**: Measure the **pre-polish baseline** wall-clock time of `./slides/deploy-pptx.sh --all` on a clean checkout *before* any change is committed. Record in `specs/003-slide-wow-polish/baseline-build-time.txt` (one number, in seconds). Target: post-polish build ≤ 150% of baseline (SC-006).

**Rationale**:

- The pipeline runs Chromium per deck for PPTX/PDF export — this dominates wall-clock time and is unaffected by theme size. Adding ~240 KB of bundled fonts + ~16 SVGs has negligible impact in the expected regime. A 1.5× ceiling leaves ample headroom while still catching pathological regressions (e.g., accidentally fetching a remote asset per slide).

**Alternatives considered**:

- *No performance budget*: rejected — leaves SC-006 unverifiable.
- *Tighter ceiling (1.1×)*: rejected — Chromium startup variance per run can exceed 10%.

---

## Summary of resolved unknowns

| Source unknown | Resolution |
|---|---|
| Custom-theme attachment mechanism | `--theme-set slides/themes/` + per-deck `theme:` front-matter |
| Color palette / typography | Cream-ink-coral + Inter + JetBrains Mono, all OFL/local |
| Iconography / diagrams | Lucide ISC bundled + hand-authored inline SVG |
| Overflow verification | `scripts/check-slide-overflow.sh` on rendered HTML |
| Reviewer-panel protocol | n=5 (SC-001) and n=8 (SC-004) open-question protocols |
| Meaning-preservation enforcement | 5 verbatim-protected blocks per deck; diff review |
| Build-time budget | Record baseline; post-polish ≤ 150% |

No `NEEDS CLARIFICATION` entries remain.
