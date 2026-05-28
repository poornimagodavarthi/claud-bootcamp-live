# Phase 0 Research — May 2026 Bootcamp Refresh

**Feature**: 005-may-2026-bootcamp-refresh
**Date**: 2026-05-28
**Status**: Resolves all `NEEDS CLARIFICATION` from `spec.md`.

---

## R-001 — Beginner content retention (spec Q1)

- **Decision**: Option A — move beginner content under `archive/beginner/`. The bootcamp's published agenda is the 10-part intermediate course; off-agenda material lives in `archive/` and is linked from `README.md` under a single "Optional pre-bootcamp warm-up (archived)" heading.
- **Rationale**: Cleanest student experience; honours Constitution Principle IX (cross-artefact consistency: one agenda, one navigation path). Keeps history and lets cohorts that want a longer ramp-up use the warm-up content.
- **Targets to move**: `slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, `slides/dist/{pdf,pptx,html}/<beginner-deck-names>` (if any leak back), and `beginner-{student,instructor,certificate}-{guide,template}.md` at repo root.
- **Targets to keep in place**: `specs/002-claude-beginner-course/` (specs are historical artefacts; do not move under archive/).
- **Alternatives considered**: (B) banner-in-place — rejected: relies on banners students skip; (C) delete — rejected: loses warm-up material some cohorts will want.

## R-002 — Part 11 (Q&A · exam briefing · next steps) (spec Q2)

- **Decision**: Option A — add `slides/part-11-qa-exam-next-steps.md` matching the canonical deck shape.
- **Rationale**: Completes the agenda; gives students a closing reference; aligns with Constitution Principle II (standardised module anatomy) — although Part 11 has no mini-project, its slide deck still earns a Promise, Concepts (common mistakes / prompting anti-patterns), Definition of done (certification rules understood), and Transition (homework + survey).
- **Constraint**: Part 11 has no exercise / no reference solution (it's a closing block). FR-002 / FR-005 / FR-006 / FR-019 explicitly scope to parts 01–10; Part 11 is enumerated as "closing block" only.
- **Build impact**: +~6 s for the slide build; +1 PDF, +1 PPTX, +1 HTML (total 33 artefacts in `slides/dist/`).

## R-003 — Pre-flight audit external-URL scope (spec Q3)

- **Decision**: Option A — intra-repo links only. External URLs are validated at human-review time, not at audit time.
- **Rationale**: Fast (≤ 1 s), deterministic, runs offline (matches Edge Case "network-restricted venue"). Constitution Principle V (Build/Review/Teach in under 30 minutes) discourages flaky network deps in CI-style gates.
- **Implementation hint**: parse `(./x)`, `(specs/y)`, `(slides/z.md)` etc. from all `.md` files; resolve against the workspace root; fail on first missing target with `<file>:<line>: <link>`.
- **Future**: a `--with-network` flag (Option B) can be added in a follow-up if cohorts complain about external link rot.

## R-004 — Constitution gate gaps surfaced in spec.md

The constitution requires **14 slide sections** (Principle II) and **9 exercise sections**. `spec.md` initially listed shorter sets. Reconciled:

- **Slide deck (14)**: Title · Promise · Why this matters · Concepts · Live demo flow · Mini project · Step-by-step lab · Suggested Claude Code prompts · Deliverable checklist · Definition of done · **Review checkpoint** · Common mistakes · Instructor notes · Transition. FR-003 in spec is to be read as the abbreviated shape; the audit gate **`audit.slide-anatomy`** (data-model.md) enforces all 14.
- **Exercise (9)**: Goal · Scenario · Starter instructions · Claude Code prompt to use · Manual validation steps · Expected deliverable · Definition of done · Stretch challenge · Troubleshooting. FR-005 in spec lists the student-facing summary fields; the audit gate **`audit.exercise-anatomy`** enforces all 9.

This is not a spec defect — the spec captures the *visible* requirement set; the constitution mandates the *complete* anatomy. The plan inherits both.

## R-005 — Duration tolerance: ±10 (spec) vs ±5 (constitution)

- **Decision**: Tighten to **±5 minutes** per Constitution Authoring & Delivery Workflow ("schedule integrity: sum of module instruction times MUST equal 240 minutes (±5 minutes)").
- **Action**: Plan's `audit.duration-sum` uses `240 ± 5`. Spec FR-009 / SC-005 will be brought into line in the next clarification pass; this is recorded here so planning is not blocked.

## R-006 — `slides/dist/` committed despite Constitution III ("MUST be gitignored")

- **Status**: Existing repo convention since features 001–004. 30 dist artefacts currently tracked (FR-012 of feature 004 enforces byte-identical PDFs for beginner decks against baseline `6f486a05`).
- **Decision**: Carry the existing convention forward; record it under **Complexity Tracking** in `plan.md`. Justification: students download published PDFs without running the build; constitution principle was authored before that workflow.
- **Risk**: Any deviation in the published dist creates a content-vs-binary diff in PRs. Mitigation: `audit.dist-freshness` gate compares MD5 of each source deck mtime vs dist artefact mtime and warns (does not fail) when stale.
- **Alternative considered**: Gitignore dist and publish PDFs via GitHub Pages or a release tarball. Rejected for this feature (out of scope); flagged as a possible 006 follow-up.

## R-007 — Bundled skills, MCP, GitHub Actions: rendering vs running

- **Decision**: For modules whose May-2026 upgrades require Anthropic-side features that may not be available in every student's environment (MCP connectors, `@claude` GitHub Action, multi-agent background sessions), provide a **recorded demo** in the `solution/` directory alongside any code, plus an **offline-mock exercise** the student can run without network access.
- **Rationale**: Edge case "Network-restricted venue" + Constitution Principle V (low setup friction). Avoids hard-coding a single Anthropic interface that may shift between cohorts.
- **Files**: `exercises/part-06/solution/asciinema-demo.cast` (GitHub Action), `exercises/part-09/solution/mcp-mock/` (local JSON-RPC stub for MCP), `exercises/part-09/solution/multi-agent-recording.md` (transcript).

## R-008 — Skills catalogue gaps

- **Inventory** (existing): code-review, test-generation, refactor, documentation-generation, git-workflow, security-checklist, production-readiness-review, release-notes, best-of-n, claude-md-template — 10 ✅.
- **New** (FR-012, FR-013): `release-readiness`, `mcp-context-brief` — 2 to add.
- **Contract**: `specs/001-bootcamp-course-materials/contracts/skill.contract.md` is the existing source of truth; new skills MUST conform.

## R-009 — Audit script design

- **Decision**: Single Bash script `scripts/preflight.sh` (POSIX-portable) composing existing checks plus new gates. Exits 0 on full pass, 1 on any violation, prints a one-page summary with offender pointers.
- **Composition**:
  - Re-uses `scripts/check-slide-overflow.sh` (already exists), `scripts/check-contrast.sh` (already exists), `scripts/check-verbatim-blocks.sh` (already exists, updated for feature 004).
  - Adds: `audit.cross-links`, `audit.slide-anatomy`, `audit.exercise-anatomy`, `audit.duration-sum`, `audit.bundle-coverage` (each may-2026 upgrade landed ≥1× in slides AND ≥1× in exercises), `audit.no-clarifications-in-published`, `audit.solution-presence`, `audit.archive-isolation` (no link from primary navigation into `archive/`).
- **Alternative**: Makefile target — rejected, redundant with a single script and adds a dep on `make` which the constitution does not require.

## R-010 — Modern production-readiness checklist content (FR-004j)

- **Source items** (from upgrade pack §9): secrets scan · dependency risk · auth/authz · logging/metrics · error handling · rollback · rate limits · CI status · test coverage · accessibility · cost/perf · generated-code ownership.
- **Integration**: 12 items mapped onto Part 10's existing **Five Axes** (Security · Observability · Deployment · Runbooks · Rollback) as sub-criteria. Part 10 keeps the 5-axis frame; the modern checklist becomes the rubric for each axis.
- **Skill linkage**: `skills/production-readiness-review/SKILL.md` body updated to enumerate the 12 items as the inputs the skill expects to see in the project.

---

## Dependencies / Stack confirmed

| Concern | Choice | Reason |
|---|---|---|
| Slide engine | Marp CLI via `npx` (Marp 4.x stream) | Constitution III + X; existing convention; no new install |
| Theme | `slides/themes/wow-beginner.css` (self-contained) | Marp does not resolve `@import` between `--theme-set` themes (verified in feature 004) |
| Demo languages | Python 3.11+ OR Node 20+ | Constitution IV ("at least one common choice") |
| Audit shell | Bash 3.2+ (macOS default) | POSIX-portable; no extra dep |
| Recording | asciinema for terminal flows | Plain text `.cast`, diffable |
| MCP mock | Static JSON-RPC stub in Python (`mcp_mock.py`) | Avoids Anthropic-side dependency for offline labs |

## Open Risks (carried into plan.md)

- **Anthropic interface drift** between recording and delivery → mitigated by polish-log + tolerant rubric (already in spec, Edge Cases).
- **Dist drift** if a slide source edit is merged without a re-build → `audit.dist-freshness` warns but does not block; CI follow-up tracked as 006.
- **Archive-move link breakage** when beginner content moves to `archive/` → `audit.cross-links` will detect; fix-up is part of the implement step.
