# Phase 1 — Data Model

**Feature**: 004 Intermediate Course Content Polish
**Date**: 28 May 2026

This is a content + assets feature (no runtime data, no database). The "data model" describes the structural entities that the spec, contracts, and audit tooling operate on. Each entity has fields, invariants, and the operations the feature performs on it.

---

## Entity: `IntermediateDeck`

A Marp Markdown source file representing one of the 10 intermediate course modules.

**Location**: `slides/part-NN-<slug>.md` for `NN ∈ {01..10}`.

**Fields**:

| Field | Type | Source | Mutability |
|---|---|---|---|
| `module_number` | integer 01..10 | filename `part-NN-*` | immutable |
| `slug` | kebab-case string | filename | immutable |
| `title` | string | H1 on cover slide | immutable (FR-012-style preservation by exclusion from editable list) |
| `theme` | enum `{wow-intermediate}` | front-matter `theme:` | set by FR-002 |
| `header` | string `"Claude Code Bootcamp · Day 1 · Module NN"` | front-matter `header:` | set by FR-002 |
| `duration_min` | integer | front-matter `<!-- duration: NN min -->` | immutable (FR-011) |
| `sections[14]` | ordered list of `DeckSection` | H2 anchors + cover | structurally immutable |
| `polish_log` | HTML comment at EOF | written by author | append-only |

**Invariants**:

- `sections.length == 14` (the 13 H2 sections + Title cover; Constitution Principle II).
- `sum(duration_min for deck in 1..10) == 240` (FR-011 + SC-009).
- Exactly one slide in each deck carries `<!-- _class: tpl-demo -->` (FR-003).
- Exactly one slide in each deck embeds a teaching SVG from `slides/intermediate/assets/NN-*.svg` (FR-004).
- Front-matter `theme: wow-intermediate` present (FR-002).

**Operations**:

1. **Restyle**: add front-matter `theme:` + `header:`, add `<!-- _class: tpl-* -->` directives to relevant slides, embed teaching SVG on Concepts slide.
2. **Polish**: rewrite the 5 editable sections under the tighten-only rule (FR-010 + Q2).
3. **Audit**: `check-verbatim-blocks.sh` verifies all invariants and SC-009/SC-010.

---

## Entity: `DeckSection`

One of the 14 structural sections inside an `IntermediateDeck`.

**Fields**:

| Field | Type | Notes |
|---|---|---|
| `kind` | enum (see below) | determines verbatim vs editable |
| `heading` | string | H1 for `Title`; H2 for the other 13 |
| `body` | string | the rendered text + any code/SVG between this heading and the next |
| `slide_index` | integer | 1-based position in the deck |
| `tpl_class` | enum `{tpl-cover, tpl-divider, tpl-objectives, tpl-show, tpl-try, tpl-done, tpl-next, tpl-demo, none}` | applied via `<!-- _class: -->` |

**`kind` enum** (14 values, fixed order):

1. `Title` — H1 cover slide. *Verbatim-preserved by exclusion from editable list.*
2. `Promise` — numbered list. **Verbatim-protected (FR-010 a)**.
3. `WhyThisMatters` — prose. **Editable (FR-010 tighten-only)**.
4. `Concepts` — prose + the teaching SVG embed. **Editable** (prose tighten-only; SVG added).
5. `LiveDemoFlow` — numbered procedure. **Editable** (becomes a `tpl-demo` slide).
6. `MiniProject` — prose framing + GOAL block. *Verbatim-preserved by exclusion.*
7. `StepByStepLab` — numbered steps. **Verbatim-protected (FR-010 e)**.
8. `SuggestedClaudeCodePrompts` — fenced ` ```text` blocks. **Verbatim-protected (FR-010 b)**.
9. `DeliverableChecklist` — `- [ ]` bullets. **Verbatim-protected (FR-010 c)**.
10. `DefinitionOfDone` — ✅-prefixed lines. **Verbatim-protected (FR-010 d)**.
11. `ReviewCheckpoint` — prose. *Verbatim-preserved by exclusion.*
12. `CommonMistakes` — bullets. **Editable (FR-010 tighten-only; Q5 = A)**.
13. `InstructorNotes` — prose. **Editable (FR-010 tighten-only)**.
14. `TransitionToNext` — prose. **Editable (FR-010 tighten-only)**.

**Invariants**:

- Every editable `kind` MUST satisfy `wc -w(body_post) ≤ wc -w(body_pre)`.
- Every verbatim-protected `kind` MUST satisfy `body_post == body_pre` byte-for-byte (modulo trailing whitespace normalisation).
- `slide_index` ordering MUST match the canonical 14-section sequence above (no reordering).

---

## Entity: `WowIntermediateTheme`

The new Marp theme CSS file.

**Location**: `slides/themes/wow-intermediate.css`.

**Fields**:

| Field | Type | Source |
|---|---|---|
| `import` | CSS at-rule | first line: `@import url('./wow-beginner.css');` |
| `tpl_demo_block` | CSS ruleset | `.tpl-demo` + descendant selectors |
| `cover_chip_override` | optional CSS | overrides `.tpl-cover .module-chip` content/colour |
| `footer_override` | optional CSS | overrides `footer` text/colour |

**Invariants**:

- MUST start with the `@import` rule (Decision 1).
- MUST NOT redefine palette tokens (`--bg`, `--ink`, `--muted`, `--accent`, `--accent-soft`, `--success`, `--danger`, `--rule`).
- MUST NOT redefine the 7 base `tpl-*` classes (only inherit them).
- MUST add `.tpl-demo` and nothing else as new template classes.

---

## Entity: `IntermediateTeachingVisual`

An SVG asset embodying one module's central concept.

**Location**: `slides/intermediate/assets/NN-<lesson-slug>.svg`.

**Fields**:

| Field | Type | Constraint |
|---|---|---|
| `viewBox` | string | `"0 0 800 450"` (16:9 content area) |
| `title` | string | inside `<title>` — one-sentence lesson statement |
| `desc` | string | inside `<desc>` — screen-reader description (≥ 1 sentence, ≤ 4 sentences) |
| `palette_tokens_used` | set of CSS var names | ⊆ the 8 palette tokens declared in wow-beginner |
| `embedded_raster` | boolean | MUST be `false` (FR-005) |
| `module_number` | integer 01..10 | MUST equal the deck it embeds in |

**Invariants** (machine-checked by Decision 2 contract):

- Exactly 10 files exist matching `slides/intermediate/assets/[0-1][0-9]-*.svg`.
- Every file's first non-`<?xml ?>` element is `<svg>`.
- Every file contains exactly one `<title>` direct-child of `<svg>` and one `<desc>` direct-child of `<svg>`.
- No `<image>` element references a raster (no `xlink:href` ending in `.png` `.jpg` `.gif` `.webp`).
- Every `fill=` / `stroke=` value is either `none`, a `#`-hex from the palette token list, or a `var(--token)` reference.

---

## Entity: `VerbatimBlockManifest`

The per-deck list of byte-identical protected blocks used by `check-verbatim-blocks.sh`.

**Location**: `specs/004-intermediate-content-polish/contracts/verbatim-blocks.md` (human-readable) + the audit script's awk patterns (machine-readable).

**Fields**:

| Field | Type | Notes |
|---|---|---|
| `deck` | filename | e.g., `slides/part-04-best-of-n.md` |
| `protected_categories[5]` | list of `(section_kind, extraction_pattern)` | the 5 categories from FR-010 |
| `editable_categories[5]` | list of `(section_kind, extraction_pattern)` | the 5 categories from Q2 |
| `baseline_ref` | git ref | merge-base of `004-intermediate-content-polish` with `main` |

**Invariants**:

- Five protected categories per deck, no fewer no more.
- Extraction patterns MUST be unambiguous (single H2 anchor + fenced/list region).

---

## Entity: `BuildArtefact`

A rendered deck output file.

**Location**: `slides/dist/<audience>/<format>/<deck-basename>.<format>`.

**Fields**:

| Field | Type | Constraint |
|---|---|---|
| `audience` | enum `{intermediate, beginner}` | derived from source path (FR-018) |
| `format` | enum `{pptx, pdf, html}` | derived from Marp invocation flag |
| `deck_basename` | string | matches source filename without `.md` |
| `source_deck` | path | one-to-one mapping |

**Invariants**:

- Total count per clean build: `18 decks × 3 formats = 54` artefacts.
- Audience subtree MUST be the first directory level under `slides/dist/` (FR-018).
- Format subtree MUST be the second directory level (FR-018).
- A complete audience hand-off MUST be a single `cp -r slides/dist/<audience>/ ...` operation.

---

## Relationships

```text
IntermediateDeck (1) ─── has ──── (14) DeckSection
IntermediateDeck (1) ─── declares ─ (1) WowIntermediateTheme
IntermediateDeck (1) ─── embeds ──── (1) IntermediateTeachingVisual
IntermediateDeck (1) ─── validated by  (1) VerbatimBlockManifest
IntermediateDeck (1) ─── produces ──── (3) BuildArtefact   (one per format)

WowIntermediateTheme (1) ── @imports ─ (1) wow-beginner.css

VerbatimBlockManifest (1) ─ partitions ─ (10) DeckSection.kind values
                                          (5 protected + 5 editable)
```

---

## State transitions

Only `IntermediateDeck` has a meaningful state machine:

```text
[pre-polish, theme: default]
    │
    │ (1) front-matter rewrite (theme: wow-intermediate, header set)
    ▼
[restyled, content unchanged]
    │
    │ (2) tpl-* class markers added to relevant slides
    │ (3) teaching SVG embedded on Concepts slide
    ▼
[restyled + visualised]
    │
    │ (4) editable sections tightened (5 sections per deck)
    │ (5) polish-log HTML comment appended
    ▼
[polish-complete]
    │
    │ (6) check-verbatim-blocks.sh → exit 0
    │ (7) deploy-pptx.sh --all → 3 artefacts under slides/dist/intermediate/<format>/
    ▼
[shipped]
```

Each transition is reversible until step (7); after build, rollback = `git revert`.

---

## What this model does NOT cover

- Exercise data, assessment data, skill data — out of scope per FR-017.
- Student progress, certificate issuance — handled by `assessments/` + `certificate-template.md`, which are immutable here.
- Runtime configuration — there is none; Marp is the only runtime, configured by front-matter.
