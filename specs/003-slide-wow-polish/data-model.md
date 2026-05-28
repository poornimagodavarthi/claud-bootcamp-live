# Phase 1 — Data Model

**Feature**: Slide Decks That Shine — Visual & Pedagogical Polish Pass
**Branch**: `003-slide-wow-polish`
**Date**: 28 May 2026

This is a documentation/content feature; "data model" here describes the **design-system entities** authored by this feature, their attributes, their relationships, and their validation rules. There is no runtime database, no application schema.

---

## Entity overview

```
DesignSystem (1) ── owns ──> Palette (1)
                  ── owns ──> TypographyPair (1)
                  ── owns ──> IconSet (1)
                  ── owns ──> SlideTemplate (7)
SlideTemplate (1) ── instantiated by ──> SlideInstance (many, across all decks)
Deck (8 beginner) ── declares ──> DesignSystem (via `theme:` front-matter)
                  ── contains ──> SlideInstance (many)
                  ── contains ──> TeachingVisual (≥ 1)
TeachingVisual (1) ── lives in ──> slides/beginner/assets/
BuildArtifactSet (3 formats × 8 decks) ── produced from ──> Deck
```

---

## Entity: DesignSystem

The single named source of truth for visual identity. **Cardinality**: exactly one instance in the repo (`wow-beginner`).

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | `wow-beginner` (matches Marp `@theme` directive in CSS) |
| `source_file` | path | yes | `slides/themes/wow-beginner.css` |
| `palette` | Palette | yes | embedded via CSS custom properties |
| `typography_pair` | TypographyPair | yes | embedded via `@font-face` |
| `icon_set` | IconSet | yes | referenced by path |
| `slide_templates` | SlideTemplate[7] | yes | one CSS class per template, see contracts |
| `documentation` | path | yes | `slides/themes/README.md` |

**Validation rules**:

- `name` MUST match the `@theme` value inside `source_file` (Marp requirement).
- `name` MUST be unique across `slides/themes/*.css`.
- Changing any field MUST propagate to all consuming decks on the next build (no per-deck override of palette/typography permitted).

---

## Entity: Palette

| Field | Type | Required | Value | Min contrast on `--bg` |
|---|---|---|---|---|
| `--bg` | hex color | yes | `#FAF7F2` | n/a |
| `--ink` | hex color | yes | `#1B1B1F` | 16.8:1 (AAA) |
| `--muted` | hex color | yes | `#5A5A66` | 6.9:1 (AAA) |
| `--accent` | hex color | yes | `#D9531E` | 4.9:1 (AA) |
| `--accent-soft` | hex color | yes | `#FCE6DA` | n/a (background only) |
| `--success` | hex color | yes | `#1F7A4D` | 5.0:1 (AA) — MUST pair with check icon |
| `--danger` | hex color | yes | `#9A2B2B` | 7.4:1 (AAA) — MUST pair with shield/warning icon |

**Validation rules**:

- Every color used as a text foreground MUST meet WCAG AA (≥ 4.5:1) against its background. Verified via `scripts/check-contrast.sh` (added in tasks) or manual contrast tool.
- `--success` and `--danger` MUST NEVER be the sole carrier of meaning — they MUST co-occur with their assigned icon and a text label (FR-006, SC-008).
- No additional colors may be introduced in deck Markdown (`color:` inline styles are forbidden by review).

---

## Entity: TypographyPair

| Field | Type | Required | Value |
|---|---|---|---|
| `body_family` | font family + fallbacks | yes | `Inter, "Helvetica Neue", Arial, sans-serif` |
| `mono_family` | font family + fallbacks | yes | `"JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace` |
| `body_file` | path | yes | `slides/themes/fonts/Inter-Variable.woff2` |
| `mono_file` | path | yes | `slides/themes/fonts/JetBrainsMono-Variable.woff2` |
| `body_license` | enum | yes | `SIL OFL 1.1` |
| `mono_license` | enum | yes | `SIL OFL 1.1` |
| `base_size_px` | integer | yes | 28 (body); 22 (caption); 56 (h1); 40 (h2); 32 (h3) |
| `line_height` | ratio | yes | 1.45 (body); 1.2 (headings); 1.5 (code) |

**Validation rules**:

- Fonts MUST be loaded via local `@font-face` in `wow-beginner.css`; no Google Fonts URL or other remote source (FR-008).
- Fallback chains MUST be present so a missing font file degrades to a system font of the same class without breaking layout (Edge Case "open in Keynote/LibreOffice").

---

## Entity: IconSet

| Field | Type | Required | Value |
|---|---|---|---|
| `family` | string | yes | `Lucide` |
| `license` | enum | yes | `ISC` |
| `source_dir` | path | yes | `slides/themes/icons/` |
| `stroke_weight_px` | number | yes | 1.75 |
| `size_class_px` | enum | yes | one of {24, 32, 48, 64} |
| `inventory` | string[] | yes | exactly the names listed under `slide-template-contracts.md §IconSet inventory` |

**Validation rules**:

- All icons MUST share `stroke_weight_px` and visual style; mixed families forbidden (FR-004, SC-002).
- An icon used in a deck MUST exist in `inventory`; ad-hoc new icons require an update to the inventory + a PR-time visual review.

---

## Entity: SlideTemplate

Recurring layout for a section type. Defined as a CSS class in `wow-beginner.css`. There are **exactly 7** templates in v1.

| Template name | CSS class | Recurrence per deck | Required slots | Optional slots |
|---|---|---|---|---|
| Cover | `.tpl-cover` | 1 | module-number, title, course-name, hero-visual | subtitle, instructor |
| Section Divider | `.tpl-divider` | 0–3 | label, accent-stripe | icon |
| What You'll Learn | `.tpl-objectives` | 1 | objectives-list (1–4 items) | duration-badge |
| Show Me | `.tpl-show` | 1–3 | code-or-terminal block, annotation | caption |
| Try It Yourself | `.tpl-try` | 1 | numbered-steps (1–5), success-criterion | icon |
| Reflect / Definition of Done | `.tpl-done` | 1 | checklist (1–6), reflection-prompt | icon |
| Closing / Next Up | `.tpl-next` | 1 | next-module-title, transition-prompt | icon |

**Validation rules** (per instance, enforced at PR review):

- Required slots MUST be present and non-empty.
- Optional slots MAY be omitted; if present, MUST match the type listed.
- A SlideInstance using a template CSS class MUST conform to that template's contract (see [contracts/slide-template-contracts.md](contracts/slide-template-contracts.md)).
- A deck MUST contain **exactly one** Cover, **exactly one** What You'll Learn, **at least one** Show Me, **exactly one** Try It Yourself, **exactly one** Reflect/Definition of Done, **exactly one** Closing/Next Up. Section Dividers are optional.

---

## Entity: TeachingVisual

A purposeful visual (not decoration) that carries lesson meaning. **Cardinality**: ≥ 1 per beginner deck (FR-003).

| Field | Type | Required | Notes |
|---|---|---|---|
| `module_number` | int (01–08) | yes | matches the deck it belongs to |
| `slug` | kebab-case string | yes | short content hint |
| `source_file` | path | yes | `slides/beginner/assets/<NN>-<slug>.svg` |
| `format` | enum | yes | `inline-svg` (only permitted format) |
| `width_px` | int | yes | matches slide template's visual slot (typically 960 or 1280) |
| `palette_compliance` | bool | yes | uses ONLY colors from Palette |
| `meaning_can_be_read_without_body_text` | bool | yes | required `true` (SC-004) |
| `replaces_text_slides` | int | optional | how many prose-heavy slides this visual lets us cut |

**Validation rules**:

- `source_file` MUST be valid SVG 1.1 (no `<script>`, no remote `<image>` refs).
- `palette_compliance` MUST be `true` (no rogue hex colors).
- The visual MUST pass the SC-004 panel test: ≥ 6 of 8 reviewers correctly state the slide's main idea from visual + title alone.

**State transitions**: none. A TeachingVisual is created once per module and edited in place if a reviewer panel fails SC-004; it does not have lifecycle states.

---

## Entity: Deck

Existing entity (defined by spec 002). This feature touches each beginner Deck's front-matter and per-slide layout but does NOT change Deck cardinality, module numbers, durations, or seat-time budgets.

| Field | Type | Required | Value | Mutability in this feature |
|---|---|---|---|---|
| `module_number` | int 01–08 | yes | per spec 002 | **frozen** |
| `duration_minutes` | int | yes | per spec 002 | **frozen** (FR-011) |
| `theme` | string | yes | `wow-beginner` (was `default`) | **mutated by this feature** |
| `learning_objectives` | string[] | yes | per spec 002 | **frozen verbatim** (FR-010, research §6) |
| `show_me_blocks` | code-or-terminal | yes | per spec 002 | **frozen verbatim** (research §6) |
| `try_steps` | string[] | yes | per spec 002 | **frozen verbatim** |
| `definition_of_done` | string[] | yes | per spec 002 | **frozen verbatim** |
| `prose_paragraphs` | string[] | yes | per spec 002 | **mutable** (tightening allowed, meaning preserved) |
| `slide_instances` | SlideInstance[] | yes | derived | **mutated** (re-templated) |

---

## Entity: BuildArtifactSet

Already implicit in spec; restated here for completeness.

| Field | Type | Required | Notes |
|---|---|---|---|
| `deck` | Deck | yes | one-to-one source |
| `pptx_path` | path | yes | `slides/dist/pptx/beginner/<deck>.pptx` |
| `pdf_path` | path | optional | `slides/dist/pdf/beginner/<deck>.pdf` (only if `--pdf`/`--all`) |
| `html_path` | path | optional | `slides/dist/html/beginner/<deck>.html` (only if `--html`/`--all`) |
| `build_status` | enum | yes | `success` \| `failure` |
| `overflow_count` | int | yes | MUST be 0 (FR-012, SC-007); verified by `check-slide-overflow.sh` against `html_path` |
| `build_seconds` | number | yes | per-deck wall-clock |

**Validation rules**:

- `build_status` MUST be `success` for all 8 beginner decks AND all 10 intermediate decks (FR-013).
- `overflow_count` MUST be 0 for all 8 beginner decks.
- Σ(`build_seconds` for all decks, `--all` mode) MUST be ≤ 1.5 × pre-polish baseline (SC-006).

---

## Cross-entity invariants

1. **Single source of truth (FR-001)**: changing one CSS variable in `DesignSystem.palette` MUST visually change all 8 decks on the next build, with no per-deck override required or permitted.
2. **No color-only meaning (FR-006, SC-008)**: every use of `--success` or `--danger` in any SlideInstance MUST co-occur with the matching icon from `IconSet`.
3. **Verbatim block preservation (FR-010, research §6)**: for every Deck, the union of `learning_objectives`, `show_me_blocks`, `try_steps`, and `definition_of_done` MUST be byte-identical before and after the polish pass (whitespace + Markdown-list-marker changes are tolerated; tokens are frozen).
4. **Asset locality (FR-008)**: every URL referenced inside `wow-beginner.css` or any `TeachingVisual` SVG MUST resolve to a relative path inside the repo. No `https://`, no `http://`, no `data:` external fetches.
5. **License notices**: every `slides/themes/fonts/LICENSE.txt` and `slides/themes/icons/LICENSE.txt` MUST be committed alongside their assets and named in the repo's main `LICENSE` consumption record.
