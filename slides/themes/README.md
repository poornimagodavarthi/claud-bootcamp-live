# `wow-beginner` — Slide Design System

The single source of truth for the visual identity of every deck in this repo.

- **All decks** (`slides/part-01..11-*.md`) → `theme: wow-beginner`

Source files:

- [`wow-beginner.css`](./wow-beginner.css) — the (self-contained) Marp custom theme. All `tpl-*` classes live here.
- [`fonts/`](./fonts) — bundled SIL OFL 1.1 fonts (Inter, JetBrains Mono).
- [`icons/`](./icons) — bundled ISC-licensed Lucide icons (13 files).
- Teaching SVGs live in [`slides/intermediate/assets/`](../intermediate/assets) (10 files, one per agenda module).

> **History**: an earlier `wow-intermediate.css` `@import`ed this theme. Marp CLI does **not** resolve `@import` between themes registered via `--theme-set`, which produced unstyled exports. The intermediate theme was therefore folded into `wow-beginner.css` and deleted. Do **not** reintroduce a multi-file theme split.

Feature specs (historical):

- [`specs/003-slide-wow-polish/`](../../specs/003-slide-wow-polish/)
- [`specs/004-intermediate-content-polish/`](../../specs/004-intermediate-content-polish/)
- [`specs/005-may-2026-bootcamp-refresh/`](../../specs/005-may-2026-bootcamp-refresh/)

---

## How a deck adopts the design system

Two changes per deck — in the front-matter:

```yaml
---
marp: true
theme: wow-beginner          # ← opt in
paginate: true
size: 16:9
header: "Claude Code 101 · Module NN"   # ← course footer text (shows on all non-cover slides)
title: "..."
description: "..."
---
```

The `slides/deploy-pptx.sh` script auto-registers any `*.css` under `slides/themes/` via `--theme-set`, so no script edit is needed.

---

## Slide templates

Each recurring lesson section uses a CSS class applied via Marp's per-slide directive:

```markdown
<!-- _class: tpl-cover -->
```

| CSS class | Use case | Required slots |
|---|---|---|
| `tpl-cover` | First slide of every deck | module-chip, h1 title, course-name line, hero icon |
| `tpl-divider` | Mid-deck section break (optional) | h2 label |
| `tpl-objectives` | "What you'll learn" | numbered list (1–4 items) |
| `tpl-show` | "Show me" — code/terminal + annotation | pre block + caption blockquote |
| `tpl-try` | "Try it yourself" — steps | numbered list + success-criterion blockquote |
| `tpl-done` | "Definition of done" — checklist | unordered list + reflection blockquote |
| `tpl-next` | Closing / next module | h2 title (final module: add `is-finale` class for ★) |
| `tpl-demo` | Live demo flow procedure | h2 + numbered steps (oversized mono numerals on accent-soft strip); optional `play` hero-icon |

Detailed contracts per template: see [`specs/003-slide-wow-polish/contracts/slide-template-contracts.md`](../../specs/003-slide-wow-polish/contracts/slide-template-contracts.md).

---

## Palette tokens

All colors are exposed as CSS custom properties on `:root` so the design system has a single source of truth.

| Token | Hex | Use | Contrast on `--bg` |
|---|---|---|---|
| `--bg` | `#FAF7F2` | Slide background | — |
| `--ink` | `#1B1B1F` | Body text + headings | 16.8:1 (AAA) |
| `--muted` | `#5A5A66` | Captions, footer, secondary text | 6.9:1 (AAA) |
| `--accent` | `#D9531E` | Highlights, accent stripes, numbered markers | 4.9:1 (AA) |
| `--accent-soft` | `#FCE6DA` | Callout backgrounds, inline-code chip | n/a |
| `--success` | `#1F7A4D` | DoD checkmark — **MUST pair with check icon** | 5.0:1 (AA) |
| `--danger` | `#9A2B2B` | Warnings — **MUST pair with shield/warning icon** | 7.4:1 (AAA) |
| `--rule` | `#E7E1D6` | Hairline rule, subtle dividers | n/a |

**Forbidden**: inline `style="color: …"` overrides; introducing new hex colors in deck Markdown; using `--success` or `--danger` without their paired icon (FR-006).

---

## Typography pair

| Family | File | License | Used for |
|---|---|---|---|
| **Inter** (variable) | `fonts/Inter-Variable.woff2` | SIL OFL 1.1 | Headings, body, captions |
| **JetBrains Mono** (variable) | `fonts/JetBrainsMono-Variable.woff2` | SIL OFL 1.1 | Code, terminal, file paths |

Both fonts are loaded via local `@font-face` (no remote fetch). Fallback chains degrade gracefully to system sans / mono if a renderer can't load the woff2.

Sizes: h1 56 px (cover h1 72 px) · h2 40 px · h3 32 px · body 28 px · code 22 px · caption 22 px.

---

## Icon inventory (Lucide v0.477.0, ISC)

13 icons live under `icons/`. Use them inline in deck Markdown:

```markdown
<img src="../themes/icons/terminal.svg" alt="" class="inline-icon" />
```

Or as a cover hero:

```markdown
<img src="../themes/icons/lightbulb.svg" alt="" class="hero-icon" />
```

| File | Suggested use |
|---|---|
| `terminal.svg` | Show-Me, cover (modules 01/02/04/08) |
| `lightbulb.svg` | Concept / aha moments (modules 03/06) |
| `shield.svg` | Safety (module 07) |
| `warning.svg` | Risk / warning callouts (modules 05/07) |
| `check.svg` | Definition of done |
| `play.svg` | Try-it-yourself |
| `pencil.svg` | Editing (modules 05/06) |
| `eye.svg` | Reading / inspecting (module 04) |
| `book.svg` | Reference (module 06 cover) |
| `file.svg` | File operations |
| `folder.svg` | Directory operations |
| `arrow-right.svg` | Closing / next-up |
| `award.svg` | Finale (module 08 closer only) |

---

## Things forbidden in any deck using this theme

- Inline `style="..."` attributes overriding palette colors.
- `<font>`, `<center>`, or other deprecated HTML.
- Remote URLs in `<img src="https://…">` or `url(https://…)` CSS values.
- Emoji used as load-bearing UI elements (icons MUST be SVG from the inventory; emoji are OK inside verbatim spec-002 prose if they were already there).
- CSS `@keyframes` or animation directives.
- Per-deck overrides of the palette or typography pair (change the theme file or open a PR amending the design system).

---

## Adding a new deck

The 10-minute walkthrough: [`specs/003-slide-wow-polish/quickstart.md`](../../specs/003-slide-wow-polish/quickstart.md).
