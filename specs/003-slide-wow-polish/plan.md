# Implementation Plan: Slide Decks That Shine — Visual & Pedagogical Polish Pass

**Branch**: `003-slide-wow-polish` | **Date**: 28 May 2026 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from [specs/003-slide-wow-polish/spec.md](spec.md)

## Summary

Apply a coherent, premium visual + pedagogical polish pass to the eight beginner Marp decks under [slides/beginner/](../../slides/beginner). The pass introduces a single shared **design system** (custom Marp theme, color palette, typography pair, recurring slide templates, icon family, diagram style) defined once and inherited by every beginner deck via Marp's `theme:` directive. Each module gains **≥ 1 purposeful teaching visual** (annotated terminal, before/after, side-by-side, diagram, concept map) authored as inline SVG so it renders identically in PPTX, PDF, and HTML. The existing build pipeline ([slides/deploy-pptx.sh](../../slides/deploy-pptx.sh)) is extended with a single backward-compatible flag (`--theme-set slides/themes/`) so all decks — beginner *and* intermediate — keep building, with the new theme available only to decks that opt in via front-matter. No new mandatory runtime tooling, no new network calls at build time, all fonts and icons bundled under MIT-compatible licenses.

## Technical Context

**Language/Version**: Marp-flavored Markdown + CSS3 (theme) + inline SVG 1.1 (teaching visuals). No application code.

**Primary Dependencies**: Existing only — Marp CLI (`@marp-team/marp-cli`, run via `npx`) and bundled Chromium. No new npm packages, no PostCSS, no Sass, no JS build step.

**Storage**: Static files in the repo. New directories: [slides/themes/](../../slides/themes) (CSS + bundled fonts + shared icon SVGs), [slides/beginner/assets/](../../slides/beginner/assets) (per-module SVG diagrams).

**Testing**: Visual regression via `slides/deploy-pptx.sh --all` build + manual review against the spec's measurable success criteria. Automated checks: (a) build exit code 0, (b) `0` slides overflow the 16:9 canvas (verified by `scripts/check-slide-overflow.sh` reading rendered HTML), (c) blind first-impression reviewer panel (SC-001) and visual-only comprehension panel (SC-004) run manually with ≥ 5 / ≥ 8 reviewers.

**Target Platform**: PPTX (primary), PDF, HTML — all produced by Marp CLI from one Markdown source. Target screen / projector / print.

**Project Type**: Documentation & content (slide decks). No application code, no services, no schema. Project structure reflects this — `src/` and `tests/` placeholders from the generic template are intentionally omitted.

**Performance Goals**: `./slides/deploy-pptx.sh --all` completes in ≤ 150% of the pre-polish baseline wall-clock time on a clean checkout (SC-006).

**Constraints**:
- No new mandatory network dependency at build time (FR-008).
- Fonts and icons bundled and MIT-compatible / OFL / Apache-2.0 (FR-009).
- WCAG AA body-text contrast ≥ 4.5:1 (FR-005, SC-005).
- No reliance on color alone to convey meaning (FR-006, SC-008).
- 0 silent canvas overflow (FR-012, SC-007).
- Intermediate decks under `slides/part-*.md` MUST keep building unchanged (FR-013).
- Per-module seat-time budget unchanged (FR-011, SC-009).

**Scale/Scope**: 8 beginner decks; ~140–180 individual slides total across the set; 1 shared theme; 7 recurring slide templates; ~8–16 new inline-SVG teaching visuals.

## Constitution Check

Constitution reference: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (v1.0.0, ratified 2026-05-21).

| # | Principle | Verdict | Notes |
|---|---|---|---|
| I | Practical, Project-Based Learning | **PASS** | This feature does not alter any module's project deliverable; it polishes the slides that frame each project. No theory-only slides are introduced. |
| II | Standardized Module Anatomy (14-section deck) | **PASS (scoped)** | Principle II's 14-section anatomy is the intermediate-bootcamp standard. Spec 002 (already on `main`) approved a simpler beginner anatomy (What you'll learn / Why this matters / The one concept / Show me / Try it yourself / Reflect / Definition of done). This feature inherits 002's anatomy unchanged; it does not add or remove sections. **No constitutional deviation introduced by feature 003**; any anatomy reconciliation question belongs to a future amendment to Principle II, not to this feature. |
| III | Marp-Flavored Markdown for All Slides | **PASS** | The new theme is a Marp custom theme CSS file consumed via `--theme-set`. Source stays Markdown. Build still goes through `slides/deploy-pptx.sh` to `slides/dist/`. |
| IV | Beginner-to-Intermediate Accessibility | **PASS** | Polish adds visual scaffolding (icons, diagrams, annotated terminals) which *lowers* cognitive load. No prerequisite knowledge added. |
| V | Build, Review, Teach in Under 30 Minutes | **PASS** | No new mandatory tools. The one script edit is a backward-compatible flag addition that auto-discovers `slides/themes/*.css`. New instructor onboarding flow is unchanged. |
| VI | Concrete, Verifiable Deliverables | **PASS** | Every SC in the spec is pass/fail or numeric. SC-001 / SC-004 use defined reviewer panels with ≥-thresholds. |
| VII | No Motivational Filler | **PASS** | Polish removes text where a visual conveys the same point; it does not add inspirational copy. FR-010 forbids changing meaning. |
| VIII | Assessment and Certification Are First-Class | **N/A** | Feature does not touch `assessments/` or `certificate-template.md`. |
| IX | Cross-Artifact Consistency | **PASS** | FR-010 fixes content meaning; cross-artifact terminology (module numbers, deliverable names, capstone scope) cannot drift because slide source text is preserved (wording tightening only). |
| X | Minimal External Dependencies | **PASS** | No new runtime deps. Fonts (Inter, JetBrains Mono — both SIL OFL) and icons (Lucide — ISC) are **bundled** as static files, not fetched at build or runtime. Documented in [research.md](research.md). |

**Result**: 9 PASS, 1 N/A, 0 FAIL. Constitution gate passes. No entries in Complexity Tracking.

Post-Phase-1 re-check: see end of plan.

## Project Structure

### Documentation (this feature)

```text
specs/003-slide-wow-polish/
├── plan.md              # This file
├── spec.md              # Feature spec (already exists)
├── research.md          # Phase 0 output (this command)
├── data-model.md        # Phase 1 output — design-system entities
├── quickstart.md        # Phase 1 output — how a contributor applies the design system
├── contracts/
│   ├── slide-template-contracts.md  # Phase 1 — recurring slide templates as contracts
│   └── build-pipeline-contract.md   # Phase 1 — what deploy-pptx.sh must keep guaranteeing
└── checklists/
    └── requirements.md  # From /speckit.specify
```

### Source Content (repository root)

This is a content/docs feature, not an application. The repo gains a new theme tree and per-module asset tree; no application source layout applies.

```text
slides/
├── deploy-pptx.sh                       # MODIFIED: auto-pick up slides/themes/*.css via --theme-set
├── themes/                              # NEW — single source of truth for the design system
│   ├── wow-beginner.css                 # NEW — Marp custom theme (the design system)
│   ├── README.md                        # NEW — how to apply, extend, and lint the theme
│   ├── fonts/                           # NEW — bundled OFL fonts (Inter, JetBrains Mono subsets)
│   │   ├── Inter-Variable.woff2
│   │   ├── JetBrainsMono-Variable.woff2
│   │   └── LICENSE.txt                  # SIL OFL 1.1 notice for both families
│   └── icons/                           # NEW — shared icon SVGs used across modules
│       ├── LICENSE.txt                  # Lucide ISC notice
│       ├── terminal.svg
│       ├── lightbulb.svg
│       ├── shield.svg
│       ├── warning.svg
│       ├── check.svg
│       ├── play.svg
│       └── … (≈12 icons total)
└── beginner/
    ├── part-01-meet-claude-code.md      # MODIFIED: theme: wow-beginner + tightened layout
    ├── part-02-first-conversation.md    # MODIFIED
    ├── part-03-asking-for-what-you-want.md  # MODIFIED
    ├── part-04-reading-code-together.md # MODIFIED
    ├── part-05-editing-one-file-safely.md   # MODIFIED
    ├── part-06-claude-md-cheat-sheet.md # MODIFIED
    ├── part-07-safer-and-smarter.md     # MODIFIED
    ├── part-08-putting-it-together.md   # MODIFIED
    └── assets/                          # NEW — per-module inline-SVG teaching visuals
        ├── 01-three-skills.svg
        ├── 02-accept-reject-loop.svg
        ├── 03-prompt-anatomy.svg
        ├── 04-explain-flow.svg
        ├── 05-edit-with-git-net.svg
        ├── 06-claude-md-anatomy.svg
        ├── 07-never-paste-matrix.svg
        └── 08-capstone-pipeline.svg

scripts/
└── check-slide-overflow.sh              # NEW — small grep on rendered HTML to assert no overflow
```

**Structure Decision**: Documentation/content feature. All artifacts live under [slides/](../../slides) (existing root). The design system is a single self-contained subtree at [slides/themes/](../../slides/themes) — one CSS file + bundled fonts + bundled icons — referenced by every beginner deck via Marp's `theme:` front-matter directive. Per-module SVG visuals live under [slides/beginner/assets/](../../slides/beginner/assets) (one SVG per module, named by module number). The intermediate decks remain untouched and continue to declare `theme: default`.

## Complexity Tracking

No constitution violations. Table intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *(none)* | | |

---

## Phase 0 — Research

See [research.md](research.md). All Technical Context items above are resolved — no `NEEDS CLARIFICATION` entries remain.

## Phase 1 — Design & Contracts

- [data-model.md](data-model.md) — design-system entities (Theme, Palette, Typography Pair, Slide Template, Teaching Visual, Build Artifact Set) with attributes and relationships, plus the per-template required-fields validation rules.
- [contracts/slide-template-contracts.md](contracts/slide-template-contracts.md) — the 7 recurring slide templates as contracts (Cover, Section Divider, What You'll Learn, Show Me, Try It Yourself, Reflect / Definition of Done, Closing / Next Up). Each contract specifies required slots, optional slots, accessibility constraints, and what a deck author MUST and MUST NOT do.
- [contracts/build-pipeline-contract.md](contracts/build-pipeline-contract.md) — the input/output contract `slides/deploy-pptx.sh` must continue to honor post-feature.
- [quickstart.md](quickstart.md) — a 10-minute walkthrough: how a contributor wires the new theme into a new deck and adds one teaching visual.

### Agent context update

[.github/copilot-instructions.md](../../.github/copilot-instructions.md) is updated to point the active feature reference at this plan (between the `<!-- SPECKIT START -->` and `<!-- SPECKIT END -->` markers).

## Post-Design Constitution Re-Check

After completing Phase 1 artifacts:

- **Principle III (Marp source of truth)**: confirmed — every contract output is Markdown + CSS + SVG. No binary slide source introduced.
- **Principle V (≤ 30 min onboarding)**: confirmed — quickstart shows a contributor adding a new deck in ≤ 10 minutes using the theme.
- **Principle X (minimal deps)**: confirmed — the only build-script change is a `--theme-set` flag pointing at a path that already lives in the repo. No npm install, no font download at build, no remote CDN.
- **Principle VI (verifiable deliverables)**: confirmed — `scripts/check-slide-overflow.sh` makes SC-007 automatable; SC-001 / SC-004 have reviewer-panel thresholds.

**Result**: gate still passes. No new entries in Complexity Tracking. Ready for `/speckit.tasks`.
