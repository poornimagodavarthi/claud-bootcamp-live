# Slide Deck Contract

**Audience**: authors of `slides/part-NN-*.md`; reviewers; `scripts/validate.sh`.
**Source rules**: Constitution Principles II, III, VII; spec FR-002, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011.

A "deck" is one Marp Markdown file under `slides/` representing exactly
one workshop module.

## File naming

```
slides/part-NN-<slug>.md
```

Where `NN` is zero-padded 01–10 and `<slug>` is fixed per module:

| NN | Slug | Module |
|---|---|---|
| 01 | `setup-mindset` | Welcome, Setup & AI-First Mindset |
| 02 | `prompting` | Prompting Like a Tech Lead |
| 03 | `claude-md` | Project Context with CLAUDE.md |
| 04 | `best-of-n` | Build Faster with Best-of-N |
| 05 | `testing-debugging` | Testing, Debugging & Self-Review |
| 06 | `git-workflows` | Git Workflows for Safe AI Dev |
| 07 | `multimodal` | Multimodal: Screenshot to UI |
| 08 | `refactor-docs` | Refactoring & Documentation at Scale |
| 09 | `skills-workflows` | Commands, Hooks & Reusable Workflows |
| 10 | `production-readiness` | Production Readiness |

> Modules 9 and 10 are **renames** of the existing `part-09-automation.md`
> and `part-10-production.md` respectively (see plan project structure).

## Required frontmatter

```yaml
---
marp: true
theme: default
paginate: true
size: 16:9
title: <Module N — Title>
description: <one-line module promise; matches the deck's "## Promise" content>
---
```

`title` MUST start with `Module N — ` (em dash).
`description` MUST be a single line ≤ 120 characters and MUST be the
same one-line promise statement as the deck's `## Promise` body's first
sentence.

## Required duration marker

Immediately after the frontmatter, an HTML comment:

```html
<!-- duration: NN min -->
```

`NN` MUST equal the module's published time budget (one of 20, 25, 30,
35). `scripts/validate.sh` parses this comment and verifies the sum
across all 10 decks equals 240 ± 5 (constitution Schedule integrity).

## Required sections (14, in order)

Each section MUST be a top-level Marp slide and MUST appear in this
exact sequence. Section headings MUST use H1 (`#`) for the deck title
and H2 (`##`) for everything else, with text matching the canonical
section name listed below (case-insensitive, exact words):

| # | Heading level | Heading text | Notes |
|---|---|---|---|
| 1 | `# ` | **Title** slide — `# Module N — <Title>` | + subtitle line w/ duration + presenter |
| 2 | `## ` | **Promise** | testable learner capabilities (verb-led) |
| 3 | `## ` | **Why this matters** | 3–5 bullets, no motivational filler |
| 4 | `## ` | **Concepts** | the teachable theory; min 3 sub-slides allowed |
| 5 | `## ` | **Live demo flow** | numbered list the instructor walks through |
| 6 | `## ` | **Mini project** | one-paragraph description of the lab deliverable |
| 7 | `## ` | **Step-by-step lab** | numbered steps mirroring the exercise README |
| 8 | `## ` | **Suggested Claude Code prompts** | ≥ 2 copy-paste prompts (FR-008) |
| 9 | `## ` | **Deliverable checklist** | bulleted, file-level |
| 10 | `## ` | **Definition of done** | pass/fail self-checklist (FR-009) |
| 11 | `## ` | **Review checkpoint** | what the instructor verifies before advancing |
| 12 | `## ` | **Common mistakes** | ≥ 3 entries, each with the fix |
| 13 | `## ` | **Instructor notes** | timing cues, cuts if running short, AV tips |
| 14 | `## ` | **Transition to next module** | one-line bridge to module N+1 (or "End of workshop" for module 10) |

`scripts/validate.sh` checks for the **presence** of each heading in
this **order** by scanning the file top-to-bottom.

## Pagination & length

- Recommended slide count per deck: 12–25 slides.
- Each `## ` section MAY span multiple slides via `---` Marp page
  breaks; ordering of section headings (above) is what matters, not
  slide count.

## Code fences

- Always tag code fences with a language: `bash`, `python`,
  `typescript`, `markdown`, `text`, `yaml`, `json`.
- Suggested Claude Code prompts (section 8) MUST use a fenced code
  block tagged ```` ```text ```` so they paste cleanly.

## Images

- Module 7 references the canonical wireframe via:
  ```markdown
  ![w:600](../exercises/part-07/wireframe.png)
  ```
- Other decks SHOULD avoid embedded images for v1 (keeps Chromium-free
  HTML preview cheap).

## Build

The deck MUST build under both `marp slides/part-NN-<slug>.md --pptx`
and `slides/deploy-pptx.sh` without manual fix-up. Failed builds block
release (constitution Authoring & Delivery Workflow → Build before
merge).

## Acceptance test (manual, per deck)

1. Frontmatter validates (Marp doesn't error).
2. `<!-- duration: NN min -->` present and matches module budget.
3. All 14 required headings appear in order.
4. Section 8 contains ≥ 2 fenced ```` ```text ```` blocks.
5. Section 10 (Definition of done) is bulleted pass/fail.
6. Section 12 (Common mistakes) has ≥ 3 entries.
7. Build produces a PPTX under `slides/dist/pptx/`.
