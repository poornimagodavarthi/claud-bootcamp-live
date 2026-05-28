# Implementation Plan: Intermediate Course Content Polish

**Branch**: `004-intermediate-content-polish` | **Date**: 28 May 2026 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from [specs/004-intermediate-content-polish/spec.md](spec.md)

## Summary

Apply the wow design system shipped in feature 003 (`slides/themes/wow-beginner.css`, fonts, icons, 7 `tpl-*` templates, teaching-SVG approach) to the 10 intermediate Bootcamp decks (`slides/part-01-setup-mindset.md` … `slides/part-10-production-readiness.md`), and perform a tighten-only content polish on five editable prose sections per deck while preserving five categories of verbatim-protected content byte-identically. Introduce a sibling theme `slides/themes/wow-intermediate.css` that `@import`s wow-beginner and adds exactly one new template class (`tpl-demo`) for the Live-demo-flow slide. Ship exactly one teaching SVG per module on the Concepts slide. Reorganise build output to `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/`. The 8 beginner decks remain byte-identical. The build stays within 1.5× the feature-003 baseline (≤ 635.79 s) and no slide overflows its canvas.

## Technical Context

**Language/Version**: Markdown (Marp-flavored CommonMark) for slide source; CSS3 for themes; SVG 1.1 for teaching visuals; Bash (POSIX + zsh-compatible) for the build orchestrator; Node.js ≥ 20 for the Marp CLI runtime.

**Primary Dependencies**: `@marp-team/marp-cli@latest` (already pinned by feature 003 deploy script); Chromium (auto-fetched by Marp for PPTX/PDF export); the bundled assets shipped in feature 003 — `slides/themes/fonts/` (Inter + JetBrains Mono Variable, OFL) and `slides/themes/icons/` (13 Lucide icons, ISC).

**Storage**: Filesystem-only. No database. Source under `slides/`; build artefacts under `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/` (gitignored, per Constitution Principle III).

**Testing**: Five automated gates: (1) `scripts/check-slide-overflow.sh` (extended to scan both audience subtrees), (2) `scripts/check-contrast.sh` (re-run against `wow-intermediate.css`), (3) `scripts/check-verbatim-blocks.sh` (new — greps the 5 protected-block categories and computes editable-section word-count deltas), (4) full clean-checkout build via `./slides/deploy-pptx.sh --all`, (5) `git diff --stat HEAD -- slides/beginner/` non-regression check. Three deferred human gates: SC-001 (n=5 first-impression panel), SC-004 (n=8 visual-only comprehension), SC-008 (colorblind audit).

**Target Platform**: macOS + Linux developer workstations; PPTX viewers (PowerPoint 2019+, Keynote, LibreOffice Impress); PDF viewers; modern browsers for HTML output. Projection target: 1920×1080 from 8 m.

**Project Type**: Course-materials repository (not a software product). Single-project layout under `slides/` + helper scripts under `scripts/`.

**Performance Goals**: Clean-checkout build ≤ 635.79 s wall-clock (1.5 × the 423.86 s baseline from `specs/003-slide-wow-polish/baseline-build-time.txt`). 0 slides overflowing the 16:9 canvas (`scripts/check-slide-overflow.sh` budget = 22 content elements per intermediate slide; 18 for beginner — unchanged from feature 003).

**Constraints**:

- FR-010 verbatim preservation: 5 protected-block categories per deck must be byte-identical to the pre-polish source.
- FR-010 tighten-only: post-polish word count for every editable section MUST be ≤ pre-polish word count.
- FR-011 duration lock: sum of `<!-- duration: NN min -->` directives across the 10 decks = 240 min exactly.
- FR-012 beginner immutability: `git diff --stat HEAD -- slides/beginner/` must be empty.
- WCAG 2.1 AA contrast on every text/background pair (inherited from feature 003 palette; re-verified).
- No new third-party dependencies; reuse the fonts + icons bundled by feature 003.

**Scale/Scope**: 10 decks × 13 H2 sections + cover = 140 sections of source markdown; ~3500 lines of source; 10 new teaching SVGs; 1 new theme file (≤ 200 LOC); 1 new audit script (≤ 150 LOC); minor patches to `slides/deploy-pptx.sh` and `scripts/check-slide-overflow.sh`. Estimated 18 deck × 3 format = 54 build artefacts.

## Constitution Check

*Gate evaluation against [.specify/memory/constitution.md](../../.specify/memory/constitution.md) v1.0.0 — PASS before Phase 0 research; re-checked after Phase 1 design.*

| # | Principle | Status | Evidence |
|---|---|---|---|
| I | Practical, Project-Based Learning | **PASS** | Feature touches only slide content + design layer. Every intermediate module's Promise / Mini-project / Step-by-step lab / Deliverable checklist remain byte-identical (FR-010). The artefact each module produces is unchanged. |
| II | Standardized Module Anatomy (14 sections per deck) | **PASS** | 13 H2 sections + Title cover = 14 sections explicitly listed as the IntermediateDeck contract (spec Key Entities). FR-010 freezes the section list; Edge Cases constrain splits to verbatim-overflow rescue only. |
| III | Marp-Flavored Markdown for All Slides | **PASS** | Source remains Marp Markdown under `slides/`. FR-018 keeps `slides/dist/` as the build root (audience subtrees only). Decks build via `./slides/deploy-pptx.sh`. No proprietary slide formats introduced. |
| IV | Beginner-to-Intermediate Accessibility | **PASS** | Targets the intermediate course, polishing existing content; does not raise the entry bar. No new programming-fundamentals teaching introduced. |
| V | Build, Review, Teach in Under 30 Minutes | **PASS** | No new setup steps. `deploy-pptx.sh` self-bootstraps Marp via npx; the wow-intermediate theme is auto-detected by the existing `--theme-set slides/themes/` patch from feature 003 (FR-009). Plan adds a 1-line `@import` in `wow-intermediate.css`. |
| VI | Concrete, Verifiable Deliverables | **PASS** | Every spec SC has a numeric or boolean threshold (5-reviewer panel ≥ 4/5 positive, build ≤ 635.79 s, sum of durations = 240 min exact, word-count delta ≤ 0, etc.). No vague success criteria. |
| VII | No Motivational Filler | **PASS** | FR-010 tighten-only rule directly enforces this: editable sections MUST be tightened, word count MUST NOT increase. Polish removes filler; it cannot add it. |
| VIII | Assessment and Certification Are First-Class | **PASS** | Out of Scope explicitly excludes `assessments/`. The polish preserves Mini-project + Deliverable + DoD verbatim (FR-010), so every assessment item that maps to a module deliverable remains valid. |
| IX | Cross-Artifact Consistency | **PASS** | FR-010 preserves the deliverable + DoD strings the rubric grades against. FR-011 preserves declared module durations. FR-012 freezes the beginner decks. H1/Title is implicitly preserved by exclusion from the editable list. |
| X | Minimal External Dependencies | **PASS** | No new third-party dependencies. Fonts (Inter, JetBrains Mono) and icons (13 Lucide) reused from feature 003. Marp CLI + Chromium are already constitutional core. |

**Overall**: PASS — no violations, no Complexity Tracking entries needed.

## Project Structure

### Documentation (this feature)

```text
specs/004-intermediate-content-polish/
├── plan.md              # This file (/speckit.plan output)
├── spec.md              # Feature specification (already authored + clarified)
├── research.md          # Phase 0 output (/speckit.plan)
├── data-model.md        # Phase 1 output (/speckit.plan)
├── quickstart.md        # Phase 1 output (/speckit.plan)
├── contracts/           # Phase 1 output (/speckit.plan)
│   ├── verbatim-blocks.md       # Per-deck protected-phrase manifest (grep contract)
│   ├── build-output-layout.md   # FR-018 directory contract
│   └── teaching-svg.md          # Per-module SVG contract (file path, title/desc, palette)
├── checklists/
│   └── requirements.md  # Already authored
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
slides/
├── deploy-pptx.sh                          # Patched: emit to audience subtrees (FR-018)
├── part-01-setup-mindset.md                # Front-matter: theme: wow-intermediate
├── part-02-prompting.md                    # Front-matter: theme: wow-intermediate
├── part-03-claude-md.md                    # Front-matter: theme: wow-intermediate
├── part-04-best-of-n.md                    # Front-matter: theme: wow-intermediate
├── part-05-testing-debugging.md            # Front-matter: theme: wow-intermediate
├── part-06-git-workflows.md                # Front-matter: theme: wow-intermediate
├── part-07-multimodal.md                   # Front-matter: theme: wow-intermediate
├── part-08-refactor-docs.md                # Front-matter: theme: wow-intermediate
├── part-09-skills-workflows.md             # Front-matter: theme: wow-intermediate
├── part-10-production-readiness.md         # Front-matter: theme: wow-intermediate
├── beginner/                               # FROZEN (FR-012)
│   └── part-01..08-*.md
├── intermediate/
│   └── assets/                             # NEW directory
│       ├── 01-tcc-loop.svg
│       ├── 02-prompt-anatomy.svg
│       ├── 03-claude-md-cheatsheet.svg
│       ├── 04-bon-scoring.svg
│       ├── 05-test-debug-loop.svg
│       ├── 06-git-flow.svg
│       ├── 07-screenshot-to-ui.svg
│       ├── 08-refactor-constraints.svg
│       ├── 09-skills-catalogue.svg
│       └── 10-five-axes.svg
└── themes/
    ├── wow-beginner.css                    # UNCHANGED (token + base class source)
    ├── wow-intermediate.css                # NEW: @import wow-beginner; .tpl-demo block
    ├── README.md                           # Updated: document wow-intermediate + tpl-demo
    ├── fonts/                              # UNCHANGED (Inter + JetBrains Mono Variable)
    └── icons/                              # UNCHANGED (13 Lucide icons)

scripts/
├── check-slide-overflow.sh                 # Patched: scan both audience subtrees, intermediate budget=22
├── check-contrast.sh                       # UNCHANGED (palette inherited; re-runs clean)
└── check-verbatim-blocks.sh                # NEW: greps 5 protected categories + word-count deltas
```

**Structure Decision**: Single-project, content-and-assets layout. No language toolchain to scaffold. Build artefacts live under `slides/dist/{intermediate,beginner}/{pptx,pdf,html}/` (gitignored). All new files land in three locations: (1) `slides/themes/wow-intermediate.css` + `slides/themes/README.md` updates; (2) `slides/intermediate/assets/NN-*.svg` (10 files); (3) `scripts/check-verbatim-blocks.sh`. Existing files modified: 10 intermediate deck markdowns, `slides/deploy-pptx.sh`, `scripts/check-slide-overflow.sh`. Beginner decks and all other workshop artefacts (`exercises/`, `skills/`, `assessments/`, guides, `specs/00{1,2,3}/`) are immutable for this feature.

## Complexity Tracking

> Not required — Constitution Check returned 10/10 PASS with no violations.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _(none)_ | — | — |

## Phase 0 → Phase 1 Handoff

- Phase 0 artefacts: [research.md](research.md) — 10 decisions documented (theme architecture, per-module SVG concept, build-output rename strategy, audit-script approach, etc.).
- Phase 1 artefacts: [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/verbatim-blocks.md](contracts/verbatim-blocks.md), [contracts/build-output-layout.md](contracts/build-output-layout.md), [contracts/teaching-svg.md](contracts/teaching-svg.md).
- Agent context: `.github/copilot-instructions.md` updated to point the active plan reference at this file.

## Post-Design Re-evaluation

Re-running Constitution Check after Phase 1: **PASS** — design preserved all 10 principles. The only design choice that could have triggered Principle III (Marp source of truth) is the build-output rename (FR-018) — resolved by keeping `slides/dist/` as the root, adding only subdirectories. The only choice that could have triggered Principle IX (cross-artifact consistency) is the duration lock — resolved by FR-011 + SC-009 enforcing sum = 240 min.

## Stop & Report

- Branch: `004-intermediate-content-polish`
- Plan: [specs/004-intermediate-content-polish/plan.md](plan.md)
- Generated artefacts: [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/verbatim-blocks.md](contracts/verbatim-blocks.md), [contracts/build-output-layout.md](contracts/build-output-layout.md), [contracts/teaching-svg.md](contracts/teaching-svg.md)
- Next command: `/speckit.tasks`
