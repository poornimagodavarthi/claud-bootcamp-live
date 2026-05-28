# Contract — `student-experience.contract.md`

**Feature**: 005-may-2026-bootcamp-refresh
**Date**: 2026-05-28

This contract describes the observable surface a **student** interacts with. It defines what the README, slides, and exercises promise — independent of implementation.

## I/O

| Input (what the student brings) | Output (what they get back) |
|---|---|
| Fresh git clone | Working repo on disk |
| Pre-work installed (Claude Code, Python 3.11+, Node 20+, Git, IDE) | All exercises runnable |
| Browser | Readable PDFs in `slides/dist/pdf/` |
| Time budget: ~4 h | 10 deliverables in `module-NN/` working directories + 1 readiness report |

## Promises (testable)

### P1 — 60-second orientation

- **Given** a fresh clone, **When** the student opens `README.md`, **Then** within the first viewport they see: agenda (10 parts + Part 11), pre-work checklist, "Where do I start?" pointer to Part 1's slide + exercise.
- **Tested by**: SC-001 (manual stopwatch with a naïve student) + `audit.cross-links` (the pointer resolves).

### P2 — One bundle per agenda part

- For NN in 01..10, the student finds:
  - One slide deck: `slides/part-NN-*.md` (and PDF/PPTX/HTML in `slides/dist/`).
  - One exercise brief: `exercises/part-NN/README.md`.
  - One reference solution: `exercises/part-NN/solution/`.
- **Tested by**: `audit.module-bundle`.

### P3 — Exercise self-sufficiency

- Each exercise README contains the 9 canonical sections (Constitution II) such that the student can attempt the task **without opening the slide deck**.
- **Tested by**: `audit.exercise-anatomy`.

### P4 — Reference solution comparability

- Each `solution/` runs on the documented pre-work in ≤ 5 minutes and produces the deliverable matching the exercise's "Expected deliverable" section.
- **Tested by**: SC-007 (dress rehearsal); no automated gate (deliberate — Anthropic interface drift makes runtime checks flaky).

### P5 — Closing summary

- Part 11 deck (`slides/part-11-qa-exam-next-steps.md`) summarises common mistakes, prompting anti-patterns, certification rules, and "what to do Monday".
- **Tested by**: presence in `audit.module-bundle` (extended to include Part 11 as deck-only entry).

### P6 — Optional warm-up is clearly optional

- `archive/beginner/` (if present) is reachable only through the single README section "Optional pre-bootcamp warm-up (archived)". No bootcamp module links into it.
- **Tested by**: `audit.archive-isolation`.

## Failure modes (what student-experience BREAKS look like)

| Symptom | Likely violation | Audit gate |
|---|---|---|
| Student can't find their first task in 60 s | README missing "Where do I start?" / dead link | `audit.cross-links` + SC-001 manual |
| Student tries to follow exercise but lacks a step | Exercise missing one of 9 canonical sections | `audit.exercise-anatomy` |
| Student compares output to `solution/` and they look unrelated | Solution drift or wrong link target | manual + dress rehearsal |
| Student opens beginner deck thinking it's today's agenda | Archive isolation broken | `audit.archive-isolation` |
| Student sees `[NEEDS CLARIFICATION]` on a slide | Internal marker leaked | `audit.no-clarifications-in-published` |
| Slide image is half off the frame | Overflow regression | `audit.slide-overflow` |

## Non-promises (what this feature explicitly does NOT guarantee)

- The student's Claude Code session produces byte-identical output to the reference solution. (LLM nondeterminism.)
- Network-only labs (MCP, GitHub Action) work offline as-is. (Offline-mock fallback provided per R-007.)
- The reference solution survives Anthropic interface changes after the cohort date without polish-log updates. (Mitigation: dated polish-log per deck — FR-020.)
