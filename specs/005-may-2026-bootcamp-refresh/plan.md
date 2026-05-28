# Implementation Plan: May 2026 Bootcamp Refresh

**Branch**: `005-may-2026-bootcamp-refresh` | **Date**: 2026-05-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-may-2026-bootcamp-refresh/spec.md`

## Summary

Land the May 2026 upgrade pack (Skills, MCP, Hooks, GitHub Actions, Multi-agent + 5 supporting topics) inside the existing 10-part bootcamp **and** make the whole repo "robust for students" by (a) archiving off-agenda beginner content, (b) closing the agenda with a Part 11 Q&A/exam deck, (c) ensuring every agenda part is a complete bundle (deck + exercise + reference solution + skill links + assessment coverage), and (d) shipping a single `scripts/preflight.sh` audit that enforces 15 gates before every cohort.

Technical approach: content-only feature. No runtime code is added. The "implementation" is markdown authoring + a Bash audit + a slide rebuild. All design decisions resolved in [research.md](./research.md); enforced surface defined in [contracts/preflight-audit.contract.md](./contracts/preflight-audit.contract.md).

## Technical Context

**Language/Version**: Markdown (Marp-flavored) + Bash 3.2+. Reference solutions use Python 3.11+ OR Node 20+ (student choice).

**Primary Dependencies**: Marp CLI via `npx --yes @marp-team/marp-cli@latest` (slide build); Chromium auto-fetched by Marp (PDF/PPTX export); Git (≥ 2.30); Claude Code (external SaaS, used by students at delivery time).

**Storage**: File system only. No databases. Build artefacts under `slides/dist/{pdf,pptx,html}/` (R-006: tracked in-tree by existing convention).

**Testing**: `scripts/preflight.sh` composes 15 audit gates (block + warn). Existing audits preserved: `check-slide-overflow.sh`, `check-contrast.sh`, `check-verbatim-blocks.sh`. No unit-test framework — content correctness is gate-based.

**Target Platform**: macOS + Linux developer laptops (pre-work supported). Students may use Windows via WSL but is not a primary target.

**Project Type**: Bootcamp content repository (single project; no `src/`, `apps/`, `packages/`). Authoring artefacts live alongside published artefacts.

**Performance Goals**: `scripts/preflight.sh` (full run) ≤ 10 s; `scripts/preflight.sh --quick` ≤ 2 s. `slides/deploy-pptx.sh --all` ≤ 10 minutes for 11 decks × 3 formats = 33 artefacts (SC-003).

**Constraints**: Offline-capable audit (R-003); no SaaS lock-in beyond Claude Code (Constitution X); slide artefacts must regenerate without manual fixup (Constitution III); duration sum 240 ± 5 min (Constitution Authoring).

**Scale/Scope**: 11 slide decks, 10 exercises, 10 reference solutions, 12 skills, 5 assessment files, 15 audit gates, 1 archive directory, 1 new audit script. Estimated ~80–120 file changes (mostly new content under `archive/`, `exercises/part-NN/solution/`, and `slides/part-11-*.md`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against [.specify/memory/constitution.md](../../.specify/memory/constitution.md) v1.0.0.

| Principle | Check | Status |
|---|---|---|
| I — Practical, Project-Based Learning | Every module retains its mini-project + reference solution; Part 11 is a closing block with no mini-project (allowed: it's not a teaching module). | ✅ PASS |
| II — Standardized Module Anatomy (14 deck / 9 exercise sections) | Enforced by `audit.slide-anatomy` + `audit.exercise-anatomy`. R-004 reconciled spec's abbreviated lists with the full constitutional anatomy. | ✅ PASS |
| III — Marp-Flavored Markdown for slides | Existing build path preserved. **Sub-clause "dist MUST be gitignored" diverges** — see Complexity Tracking row 1. | ⚠ JUSTIFIED |
| IV — Beginner-to-Intermediate Accessibility | Audience and pre-work explicit in spec assumptions; warm-up content archived but accessible. | ✅ PASS |
| V — Build, Review, Teach in Under 30 Minutes | `scripts/preflight.sh` ≤ 10 s; `quickstart.md` end-to-end ≤ 5 min. | ✅ PASS |
| VI — Concrete, Verifiable Deliverables | Every gate produces RC + file pointer. Exercise DoD remains pass/fail. | ✅ PASS |
| VII — No Motivational Filler | Spec is operational; all new slide copy is task-driven (Part 11 reframes as "common mistakes + cert rules + next Monday"). | ✅ PASS |
| VIII — Assessment & Certification First-Class | FR-010 + `audit.assessment-coverage` keep 5 assessment files in sync; new May-2026 topics get explicit rubric items. | ✅ PASS |
| IX — Cross-Artefact Consistency | `audit.cross-links` + `audit.bundle-coverage` + `audit.archive-isolation`. | ✅ PASS |
| X — Minimal External Dependencies | Only Bash + Marp/Chromium (existing) + Claude Code (existing). No new deps. | ✅ PASS |

### Constitution-derived gate threshold updates

- **Duration tolerance**: spec FR-009 / SC-005 said ±10; constitution says ±5. Plan adopts ±5 (R-005). Spec will be aligned in a follow-up clarification pass.
- **Section anatomy**: spec FR-003 listed 13 deck sections (missing "Review checkpoint"). Plan's `audit.slide-anatomy` enforces all 14 (R-004).
- **Exercise anatomy**: spec FR-005 listed 6 fields. Plan's `audit.exercise-anatomy` enforces all 9 (R-004).

These are tightenings, not violations — the spec is a superset of the constitution.

## Project Structure

### Documentation (this feature)

```text
specs/005-may-2026-bootcamp-refresh/
├── plan.md                                # This file
├── spec.md                                # Feature spec (Q1–Q3 resolved by research.md)
├── research.md                            # Phase 0 — decisions R-001..R-010
├── data-model.md                          # Phase 1 — entities, gates, counts
├── quickstart.md                          # Phase 1 — how a new maintainer verifies end-state
├── contracts/
│   ├── preflight-audit.contract.md        # Phase 1 — scripts/preflight.sh wire contract
│   └── student-experience.contract.md     # Phase 1 — README/slides/exercises promises
└── checklists/
    └── requirements.md                    # Spec-quality checklist (11/12 green; 3 NEEDS-CLARIFICATION resolved in research.md)
```

### Repository structure (after this feature lands)

```text
Training-Claude-Code-Extended/
├── README.md                              # Updated: 10-part agenda + Part 11 + archive section
├── student-guide.md                       # Updated: same agenda; archive section
├── instructor-guide.md                    # Updated: cut-lines per module
├── slides/
│   ├── themes/                            # wow-beginner.css only (Constitution III)
│   ├── intermediate/assets/               # 10 SVGs (h≤320 in decks)
│   ├── part-01-setup-mindset.md           # +"Claude Code surfaces" slide (already landed in feature 004 refresh)
│   ├── part-02-prompting.md               # +Unix-pipe composability
│   ├── part-03-claude-md.md
│   ├── part-04-best-of-n.md
│   ├── part-05-testing-debugging.md       # +bundled skills (/debug /verify /code-review /loop /batch)
│   ├── part-06-git-workflows.md           # +@claude in GitHub Actions
│   ├── part-07-multimodal.md
│   ├── part-08-refactor-docs.md           # +bundled /code-review reinforcement
│   ├── part-09-skills-workflows.md        # Rewritten: Skills · Hooks · MCP · Multi-agent
│   ├── part-10-production-readiness.md    # +overeager-agent safety + modern checklist
│   ├── part-11-qa-exam-next-steps.md      # NEW (R-002)
│   └── dist/{pdf,pptx,html}/              # 33 artefacts after rebuild
├── exercises/
│   ├── part-01/ … part-10/                # Each: README.md + solution/
│   │   └── solution/                      # NEW or refreshed: runnable reference
│   └── (no part-11 — closing block)
├── skills/
│   ├── code-review/ … release-notes/      # 10 existing
│   ├── release-readiness/SKILL.md         # NEW (FR-012)
│   └── mcp-context-brief/SKILL.md         # NEW (FR-013)
├── assessments/
│   ├── knowledge-quiz.md                  # +May-2026 coverage items
│   ├── practical-task.md                  # +Skills/MCP/Hooks/Actions/Multi-agent task variants
│   ├── code-review-reflection.md
│   ├── rubric.md                          # +modern production-readiness checklist
│   └── answer-key.md
├── scripts/
│   ├── preflight.sh                       # NEW (FR-016 + contract)
│   ├── check-slide-overflow.sh            # existing
│   ├── check-contrast.sh                  # existing
│   ├── check-verbatim-blocks.sh           # existing
│   └── gates/                             # optional split-files for per-gate impl
└── archive/
    └── beginner/                          # NEW (R-001) — moved from slides/beginner/, exercises/beginner/, etc.
        ├── slides/
        ├── exercises/
        ├── assessments/
        └── README.md                      # explains the archive policy
```

**Structure Decision**: Existing single-project content layout retained (Constitution X: minimal deps). The only structural additions are `archive/` (off-agenda content) and `scripts/preflight.sh` (audit composition). No new source roots, no new languages, no new frameworks.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| **`slides/dist/` tracked in-tree** (Constitution III sub-clause: "MUST be gitignored") | Students download published PDFs directly from the repo without installing `npx`/Chromium. Existing repo convention since 001; baseline (`6f486a05`) for feature 004 FR-012 references dist artefacts. | Gitignore-dist alternative (publish via GitHub Pages or release tarball) requires CI + release pipeline — out of scope for this feature; tracked as 006 follow-up in R-006. |

No other principle-level violations.

---

## Phases (status snapshot)

- **Phase 0 — Outline & Research**: ✅ DONE — `research.md` resolves all 3 spec `NEEDS CLARIFICATION` markers (R-001 archive, R-002 Part 11, R-003 audit scope) plus 7 derived decisions (R-004..R-010).
- **Phase 1 — Design & Contracts**: ✅ DONE — `data-model.md` (9 entities, 15 gates, counts), `contracts/preflight-audit.contract.md` (the wire interface), `contracts/student-experience.contract.md` (the user-facing promises), `quickstart.md` (5-min verification recipe). Agent context updated below.
- **Phase 2 — Tasks** (NOT executed by `/speckit.plan`): to be produced by `/speckit.tasks`.

## Post-Design Constitution Re-check

After Phase 1 design:

- **II (anatomy)**: Confirmed by `audit.slide-anatomy` (14 sections) + `audit.exercise-anatomy` (9 sections) → ✅
- **III (Marp + gitignore)**: Marp path unchanged ✅; gitignore divergence remains under Complexity Tracking ⚠ JUSTIFIED.
- **VIII (assessments)**: `audit.assessment-coverage` enforces 40/40/20 weighting + 70% threshold + May-2026 coverage items → ✅
- **IX (consistency)**: `audit.cross-links` + `audit.bundle-coverage` + `audit.archive-isolation` → ✅
- **X (deps)**: No new runtime deps in design; Bash audit is portable → ✅

No new violations surfaced by the design.

## Branch / agent-context update

The `.github/copilot-instructions.md` SPECKIT block now points at this plan. See updated section below the file's `<!-- SPECKIT START -->` marker.

---

## Report

- **Branch**: `005-may-2026-bootcamp-refresh`
- **Plan**: [specs/005-may-2026-bootcamp-refresh/plan.md](./plan.md)
- **Phase 0**: [research.md](./research.md)
- **Phase 1**:
  - [data-model.md](./data-model.md)
  - [contracts/preflight-audit.contract.md](./contracts/preflight-audit.contract.md)
  - [contracts/student-experience.contract.md](./contracts/student-experience.contract.md)
  - [quickstart.md](./quickstart.md)
- **Constitution**: all gates either PASS or JUSTIFIED (1 row in Complexity Tracking).
- **Ready for**: `/speckit.tasks`.
