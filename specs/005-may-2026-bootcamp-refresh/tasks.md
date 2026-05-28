---
description: "Task list for May 2026 Bootcamp Refresh (feature 005)"
---

# Tasks: May 2026 Bootcamp Refresh

**Input**: Design documents from `/specs/005-may-2026-bootcamp-refresh/`
**Plan**: [plan.md](./plan.md) · **Spec**: [spec.md](./spec.md)
**Available docs**: research.md, data-model.md, contracts/, quickstart.md

**Tests**: Spec did not request unit/integration tests. Verification is gate-based via `scripts/preflight.sh` (built in Phase 2). No `tests/` directory is created.

**Organization**: Tasks grouped by user story. US1, US2, US3 are all P1; US4, US5 are P2.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: parallelizable (different file, no incomplete dependency)
- **[Story]**: US1..US5 (only for story-phase tasks)
- Every task includes an explicit file path

## Path Conventions

Content repository (single-project layout per plan.md): `slides/`, `exercises/`, `skills/`, `assessments/`, `scripts/`, `archive/`, `specs/`. No `src/`, no `tests/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare directory shape and baseline scaffolding shared by every user story.

- [X] T001 Create `archive/` and `archive/beginner/` directories with a placeholder `archive/README.md` describing the archive policy (R-001, FR-015)
- [X] T002 [P] Create `scripts/gates/` directory with a `.gitkeep` to host per-gate helpers used by `scripts/preflight.sh` (plan.md project structure)
- [X] T003 [P] Update root `.gitignore` to keep tracking `slides/dist/{pdf,pptx,html}/` (existing exception) but ignore `slides/dist/.cache/` and any `scripts/gates/*.log` (R-006)
- [X] T004 [P] Create `skills/release-readiness/` and `skills/mcp-context-brief/` directory placeholders with empty `SKILL.md` stubs to be filled in US2 (FR-012, FR-013)

**Checkpoint**: Directory tree matches plan.md "Repository structure (after this feature lands)".

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ship `scripts/preflight.sh` with all 15 gates implemented. Every user story below uses these gates as its definition of done. Without Phase 2, no story can prove correctness.

**⚠️ CRITICAL**: All US1–US5 acceptance criteria are validated by gates created here. No user-story work in Phase 3+ may be marked done until its referenced gates pass.

- [X] T005 Implement `scripts/preflight.sh` skeleton with flag parsing (`--quick`, `--verbose`, `--gate`), RC table (0/1/2/64), and report header per `contracts/preflight-audit.contract.md`
- [X] T006 [P] Implement `gate_module-bundle` in `scripts/gates/module-bundle.sh` (assert for NN in 01..10 that `slides/part-NN-*.md`, `exercises/part-NN/README.md`, `exercises/part-NN/solution/` all exist)
- [X] T007 [P] Implement `gate_slide-anatomy` in `scripts/gates/slide-anatomy.sh` (assert 14 canonical H2 sections per data-model.md SlideDeck.sections; applies to `slides/part-*.md` including Part 11)
- [X] T008 [P] Implement `gate_slide-theme` in `scripts/gates/slide-theme.sh` (wrap existing `scripts/check-verbatim-blocks.sh` frontmatter check; assert `theme: wow-beginner`)
- [X] T009 [P] Implement `gate_slide-overflow` in `scripts/gates/slide-overflow.sh` (delegate to `scripts/check-slide-overflow.sh --budget 22 slides/dist/html`; honour `--quick` skip)
- [X] T010 [P] Implement `gate_duration-sum` in `scripts/gates/duration-sum.sh` (sum `<!-- duration: NN min -->` across part-01..10; assert `235 ≤ Σ ≤ 245`)
- [X] T011 [P] Implement `gate_exercise-anatomy` in `scripts/gates/exercise-anatomy.sh` (assert 9 canonical H2 sections per data-model.md Exercise.sections)
- [X] T012 [P] Implement `gate_solution-presence` in `scripts/gates/solution-presence.sh` (assert `exercises/part-NN/solution/` contains at least one of README.md/run.sh/solution.{py,js,ts,md})
- [X] T013 [P] Implement `gate_skill-contract` in `scripts/gates/skill-contract.sh` (validate `skills/*/SKILL.md` against `specs/001-bootcamp-course-materials/contracts/skill.contract.md`; assert exactly the 12 expected slugs)
- [X] T014 [P] Implement `gate_assessment-coverage` in `scripts/gates/assessment-coverage.sh` (assert 5 assessment files exist; rubric.md references each module 01–10; each of Skills/MCP/Hooks/GitHub Actions/Multi-agent appears ≥1×)
- [X] T015 [P] Implement `gate_cross-links` in `scripts/gates/cross-links.sh` (extract relative markdown links from every `.md` outside `.git/`, `node_modules/`, `slides/dist/`; resolve; report `<file>:<line> -> <link>` for unresolved; skip http/https/anchor-only links — R-003)
- [X] T016 [P] Implement `gate_bundle-coverage` in `scripts/gates/bundle-coverage.sh` (for each of Skills/MCP/Hooks/GitHub Actions/Multi-agent: assert ≥1 occurrence in `slides/part-*.md` AND ≥1 in `exercises/part-*/README.md`)
- [X] T017 [P] Implement `gate_no-clarifications-in-published` in `scripts/gates/no-clarifications.sh` (grep `\[NEEDS CLARIFICATION` and `^TODO\b` across README, slide decks, exercise READMEs, SKILL.md files)
- [X] T018 [P] Implement `gate_archive-isolation` in `scripts/gates/archive-isolation.sh` (when `archive/` exists, assert no markdown link into it exists outside the single allowed section `## Optional pre-bootcamp warm-up (archived)` in README.md)
- [X] T019 [P] Implement `gate_dist-freshness` in `scripts/gates/dist-freshness.sh` (warn-severity: compare mtime of each `slides/part-*.md` against its `slides/dist/pdf/<basename>.pdf`)
- [X] T020 [P] Implement `gate_contrast` in `scripts/gates/contrast.sh` (delegate to existing `scripts/check-contrast.sh`)
- [X] T021 Wire all 15 gates into `scripts/preflight.sh` registry (source files from `scripts/gates/`, iterate, honour `--gate <name>` filter, aggregate RC per severity)
- [X] T022 Add execute bits and run a smoke pass: `bash scripts/preflight.sh --gate audit.cross-links` returns 0 or 1 with no tooling error (RC≠2/64)

**Checkpoint**: `scripts/preflight.sh` runs end-to-end against current repo state. Failing gates point at actual gaps that US1–US5 will close.

---

## Phase 3: User Story 1 — 60-second onboarding (Priority: P1) 🎯 MVP

**Goal**: A new student lands on `README.md`, finds the agenda + pre-work + "where do I start?" within the first viewport, and reaches `exercises/part-01/README.md` in under 60 seconds.

**Independent Test**: Stopwatch test with a colleague who has not seen the repo (SC-001 in spec); `bash scripts/preflight.sh --gate audit.cross-links` returns 0 for README's link set.

- [X] T023 [US1] Rewrite the top of `README.md` so the first viewport (~30 lines) contains: one-paragraph promise, pre-work checklist (Python 3.11+, Node 20+, Git, Claude Code, IDE), 10-row agenda table (part / title / minutes / deck link / exercise link), and a "Where do I start?" callout pointing at `exercises/part-01/README.md` (FR-001, FR-007)
- [X] T024 [US1] Add the section `## Optional pre-bootcamp warm-up (archived)` near the bottom of `README.md` linking to `archive/beginner/README.md` (single allowed entry per `audit.archive-isolation`; FR-015)
- [X] T025 [US1] Refresh `student-guide.md` so its agenda + pre-work mirror `README.md` exactly (Constitution IX consistency; FR-001)
- [X] T026 [P] [US1] Audit and fix all README → slides/exercises links so `bash scripts/preflight.sh --gate audit.cross-links` passes
- [X] T027 [US1] Manual stopwatch validation against SC-001 (write the result + cohort date as a polish-log entry in `README.md` if a comment marker exists, or skip if not applicable)

**Checkpoint**: `audit.cross-links` green for README + student-guide. Manual SC-001 ≤ 60 s.

---

## Phase 4: User Story 2 — Instructor can deliver the full 4 h with May 2026 story landed (Priority: P1)

**Goal**: Every module 01–10 deck carries the May 2026 upgrade pack (Skills, MCP, Hooks, GitHub Actions, Multi-agent + 5 supporting), the closing Part 11 deck exists, duration sum is 240 ± 5 min, two new skills are published.

**Independent Test**: `bash scripts/preflight.sh --gate audit.slide-anatomy --gate audit.slide-theme --gate audit.duration-sum --gate audit.bundle-coverage --gate audit.skill-contract` returns 0; dress rehearsal walks all 11 decks without drift.

### Part 11 closing deck (NEW)

- [X] T028 [US2] Create `slides/part-11-qa-exam-next-steps.md` (theme `wow-beginner`, paginate true, size 16:9) with all 14 canonical H2 sections; content covers common-mistakes recap, prompting anti-patterns, certification rules (40/40/20, 70% pass), and "what to do Monday" (R-002, FR-009)

### May 2026 content landing across modules 01–10

- [X] T029 [P] [US2] Verify `slides/part-01-setup-mindset.md` already carries the "Claude Code is everywhere (May 2026)" + speaker slides from feature 004; add a one-line callout in the Concepts section referencing the agentic shift (FR-004)
- [X] T030 [P] [US2] Add Unix-pipe composability beat to `slides/part-02-prompting.md` Concepts section + Suggested prompts section (FR-004)
- [X] T031 [P] [US2] Verify Part 3 `slides/part-03-claude-md.md` includes a CLAUDE.md "skills/hooks/mcp pointers" subsection; add if missing (FR-004)
- [X] T032 [P] [US2] Verify Part 4 `slides/part-04-best-of-n.md` mentions multi-agent fan-out as an alternative to best-of-N (FR-004)
- [X] T033 [P] [US2] Verify `slides/part-05-testing-debugging.md` carries the "Bundled skills do the heavy lifting" slide (`/debug` `/verify` `/code-review` `/loop` `/batch`) from feature 004 (FR-004)
- [X] T034 [P] [US2] Verify `slides/part-06-git-workflows.md` carries the "@claude in GitHub Actions" slide referencing `anthropics/claude-code-action` from feature 004 (FR-004)
- [X] T035 [P] [US2] Add a "Multimodal review with @claude" beat to `slides/part-07-multimodal.md` Live demo flow (FR-004)
- [X] T036 [P] [US2] Add a `/code-review` skill reinforcement beat to `slides/part-08-refactor-docs.md` Suggested prompts (FR-004)
- [X] T037 [US2] Verify `slides/part-09-skills-workflows.md` is titled "Skills, Hooks, MCP & Multi-Agent Workflows" with the 4-pillar slide structure from feature 004; add a Transition + Review checkpoint section if any of the 14 canonical sections are missing (FR-004)
- [X] T038 [P] [US2] Verify `slides/part-10-production-readiness.md` carries the "Overeager agents" slide + the modern 12-item readiness checklist from feature 004 (FR-004)
- [X] T039 [US2] Adjust `<!-- duration: NN min -->` markers across part-01..10 so Σ = 240 ± 5 (run `scripts/preflight.sh --gate audit.duration-sum` until green; R-005)

### Two new skills (FR-012, FR-013)

- [X] T040 [P] [US2] Write `skills/release-readiness/SKILL.md` with the 6 required H2 sections (Purpose, When to use, Body, Inputs, Outputs, Worked example); project-agnostic (no `module-NN/` paths); content covers running the 12-item readiness checklist before a release (FR-012)
- [X] T041 [P] [US2] Write `skills/mcp-context-brief/SKILL.md` with the 6 required H2 sections; content covers preparing a context brief for an MCP-connected tool (Jira/Slack/GitHub) before invoking it (FR-013)

### Assessment coverage (FR-010)

- [X] T042 [P] [US2] Update `assessments/knowledge-quiz.md` with ≥1 item per May-2026 topic (Skills, MCP, Hooks, GitHub Actions, Multi-agent)
- [X] T043 [P] [US2] Update `assessments/practical-task.md` with ≥1 task variant per May-2026 topic
- [X] T044 [P] [US2] Update `assessments/rubric.md` to keep 40/40/20 weighting + 70% pass while adding modern readiness-checklist criteria (Constitution VIII)
- [X] T045 [P] [US2] Update `assessments/answer-key.md` to match new quiz + task items
- [X] T046 [P] [US2] Update `assessments/code-review-reflection.md` with a Skills/MCP-aware reflection prompt

### Build & verify

- [X] T047 [US2] Run `( cd slides && ./deploy-pptx.sh --all )` to produce 33 artefacts under `slides/dist/{pdf,pptx,html}/` (SC-003)
- [X] T048 [US2] Run `scripts/preflight.sh --gate audit.slide-anatomy --gate audit.slide-theme --gate audit.duration-sum --gate audit.bundle-coverage --gate audit.skill-contract --gate audit.assessment-coverage` and resolve until all green

**Checkpoint**: 11 decks build, 5 May-2026 topics land in slides + exercises, duration sums to 240 ± 5, two new skills exist, assessments cover May-2026.

---

## Phase 5: User Story 3 — Every exercise has a working reference solution (Priority: P1)

**Goal**: For NN in 01..10, `exercises/part-NN/solution/` exists with a runnable entry point and matches the exercise's "Expected deliverable".

**Independent Test**: `bash scripts/preflight.sh --gate audit.module-bundle --gate audit.exercise-anatomy --gate audit.solution-presence` returns 0; dress rehearsal walks every solution in ≤ 5 min each (SC-007).

- [X] T049 [P] [US3] Audit `exercises/part-01/README.md` against 9 canonical sections; fill missing sections; ensure runnable `exercises/part-01/solution/` with README + entry point
- [X] T050 [P] [US3] Audit `exercises/part-02/README.md` + ensure `exercises/part-02/solution/` is runnable
- [X] T051 [P] [US3] Audit `exercises/part-03/README.md` + ensure `exercises/part-03/solution/` is runnable
- [X] T052 [P] [US3] Audit `exercises/part-04/README.md` + ensure `exercises/part-04/solution/` is runnable
- [X] T053 [P] [US3] Audit `exercises/part-05/README.md` + ensure `exercises/part-05/solution/` is runnable (per code-review-rubric.md)
- [X] T054 [P] [US3] Audit `exercises/part-06/README.md` + ensure `exercises/part-06/solution/` exists (CREATE if missing — currently no solution dir per workspace structure)
- [X] T055 [P] [US3] Audit `exercises/part-07/README.md` + ensure `exercises/part-07/solution/` is runnable (Mermaid wireframe rendering)
- [X] T056 [P] [US3] Audit `exercises/part-08/README.md` + ensure `exercises/part-08/solution/` is runnable
- [X] T057 [P] [US3] Audit `exercises/part-09/README.md` + CREATE `exercises/part-09/solution/` (currently missing per workspace structure); solution must demonstrate one of Skills/Hooks/MCP/Multi-agent (FR-005, FR-008)
- [X] T058 [P] [US3] Audit `exercises/part-10/README.md` + CREATE `exercises/part-10/solution/` (currently missing); solution must produce a readiness report against the 12-item checklist (FR-006, FR-008)
- [X] T059 [US3] For each exercise, add an inline link in its `README.md` "Expected deliverable" section pointing at the corresponding `solution/` README (FR-005)
- [X] T060 [US3] Run `scripts/preflight.sh --gate audit.module-bundle --gate audit.exercise-anatomy --gate audit.solution-presence` and resolve until all green
- [X] T061 [US3] Dress-rehearsal each solution end-to-end; if any solution takes > 5 min, simplify it (SC-007)

**Checkpoint**: 10 exercises × 9 sections; 10 solutions present with entry points; dress rehearsal passes.

---

## Phase 6: User Story 4 — Pre-flight audit catches breakage before delivery (Priority: P2)

**Goal**: `scripts/preflight.sh` is documented, scripted, and produces actionable output. The instructor runs it as the standard pre-cohort gate.

**Independent Test**: `bash scripts/preflight.sh` returns RC=0 against the published repo state; injecting a synthetic break (e.g., delete an H2 section, add a `[NEEDS CLARIFICATION]` token) produces an RC=1 with a precise file:line offender.

- [X] T062 [US4] Add a "Pre-delivery audit" section to `instructor-guide.md` documenting `scripts/preflight.sh` invocation, RC table, and the 15 gates with their severity (FR-016, contract)
- [X] T063 [P] [US4] Add a "Run the audit" subsection to `README.md` (one-liner: `scripts/preflight.sh`) and link to the instructor-guide section
- [X] T064 [US4] Inject a synthetic break (temporarily delete a canonical H2 from one deck) and verify `scripts/preflight.sh` fails with a file:line pointer; revert the break
- [X] T065 [US4] Inject a synthetic `[NEEDS CLARIFICATION]` token in a README and verify `audit.no-clarifications-in-published` fires; revert
- [X] T066 [US4] Final full-run: `bash scripts/preflight.sh` returns RC=0; record stdout snapshot in `specs/005-may-2026-bootcamp-refresh/quickstart.md` polish-log block

**Checkpoint**: Audit is the standard pre-cohort gate, documented and proven.

---

## Phase 7: User Story 5 — Off-agenda content archived, not in student's path (Priority: P2)

**Goal**: All beginner / pre-bootcamp content lives under `archive/beginner/` with a single labelled entry from README; no primary-navigation link enters the archive.

**Independent Test**: `bash scripts/preflight.sh --gate audit.archive-isolation` returns 0; visual inspection confirms only the labelled section links to the archive.

- [X] T067 [US5] Move `slides/beginner/` (if present) → `archive/beginner/slides/` using `git mv` to preserve history (R-001, FR-015)
- [X] T068 [US5] Move `exercises/beginner/` → `archive/beginner/exercises/` (R-001, FR-015)
- [X] T069 [US5] Move `assessments/beginner/` → `archive/beginner/assessments/` (R-001, FR-015)
- [X] T070 [US5] Move root `beginner-instructor-guide.md`, `beginner-student-guide.md`, `beginner-certificate-template.md` → `archive/beginner/` (R-001, FR-015)
- [X] T071 [US5] Write `archive/beginner/README.md` explaining: this content is an optional pre-bootcamp warm-up, not part of the 4-hour bootcamp, kept for historical reference (R-001)
- [X] T072 [P] [US5] Sweep `instructor-guide.md`, `student-guide.md`, every `slides/part-*.md`, every `exercises/part-*/README.md` removing any inline link into `slides/beginner/`, `exercises/beginner/`, or root `beginner-*.md` files (`audit.archive-isolation`)
- [X] T073 [US5] Verify the only remaining link into `archive/` originates from the single README section `## Optional pre-bootcamp warm-up (archived)` (added in T024)
- [X] T074 [US5] Run `scripts/preflight.sh --gate audit.archive-isolation` until green

**Checkpoint**: Archive is fully isolated; one labelled entry; gate green.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, full-repo verification, polish-log seeding, and dist rebuild.

- [X] T075 [P] Update `GLOSSARY.md` with new terms: "skill", "hook", "MCP", "GitHub Action `@claude`", "multi-agent fan-out", "overeager agent" (Constitution IX)
- [X] T076 [P] Add a dated polish-log entry to each `slides/part-*.md` EOF HTML comment block recording the May-2026 refresh date + cohort tag (FR-020)
- [X] T077 [P] Run `scripts/check-slide-overflow.sh --budget 22 slides/dist/html`; fix any overflow regressions (Constitution III)
- [X] T078 [P] Run `scripts/check-contrast.sh`; fix any contrast regressions (Constitution III)
- [X] T079 Re-run `( cd slides && ./deploy-pptx.sh --all )` to refresh all 33 artefacts after every content change above (SC-003)
- [X] T080 Full final pass: `bash scripts/preflight.sh` returns RC=0 with no FAIL and at most the `audit.dist-freshness` warning resolved
- [X] T081 Run the [quickstart.md](./quickstart.md) end-to-end as a fresh maintainer; record actual elapsed minutes
- [X] T082 Update the spec.md `[NEEDS CLARIFICATION]` markers (Q1/Q2/Q3) to "Resolved: see research.md R-001/R-002/R-003" so `audit.no-clarifications-in-published` stays green on published surfaces

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: no deps — start immediately
- **Phase 2 (Foundational)**: depends on Phase 1 — BLOCKS US1..US5
- **Phase 3 (US1)**: depends on Phase 2 — uses `audit.cross-links`
- **Phase 4 (US2)**: depends on Phase 2 — uses 6 gates
- **Phase 5 (US3)**: depends on Phase 2 — uses 3 gates
- **Phase 6 (US4)**: depends on Phases 3+4+5 (because injection tests assume content exists) — final gate documentation
- **Phase 7 (US5)**: depends on Phase 2 and on T024 (the single archive entry in README from US1) — physically safe to start earlier, but `audit.archive-isolation` only goes green after T024
- **Phase 8 (Polish)**: depends on all user stories complete

### User Story Dependencies

- US1 (P1) — README/student-guide rewrite. Depends only on Foundational.
- US2 (P1) — Slide/skill/assessment content. Depends only on Foundational. Independent of US1, US3.
- US3 (P1) — Exercise + solution content. Depends only on Foundational. Independent of US1, US2.
- US4 (P2) — Audit documentation + injection tests. Soft dependency on US1/US2/US3 having produced content for the gates to evaluate.
- US5 (P2) — Archive isolation. Shares only T024 with US1; otherwise independent.

### Within Each Story

- Anatomy fixes before solution refresh (US3): T049–T058 each do anatomy then solution presence within the same task scope.
- Content additions before duration tuning (US2): T029–T038 before T039.
- Builds after content (US2): T047 after T028–T046.
- Documentation last (US4): T062 after gates exist (Phase 2).

### Parallel Opportunities

- **Phase 1**: T002 [P], T003 [P], T004 [P] in parallel after T001.
- **Phase 2**: T006–T020 are all [P] and can be written in parallel after T005. Sequential: T005 → (T006..T020 in parallel) → T021 → T022.
- **Phase 3 (US1)**: T026 [P] runs in parallel with T023/T025; T024 and T027 are sequential after T023.
- **Phase 4 (US2)**: T029–T038 (slide beats) are 10× [P]; T040–T041 (new skills) are 2× [P]; T042–T046 (assessments) are 5× [P]; T028 (Part 11) and T039 (duration tuning) are sequential. T047 (build) and T048 (verify) sequential after content.
- **Phase 5 (US3)**: T049–T058 are 10× [P] (different exercise directories).
- **Phase 7 (US5)**: T072 [P] sweep can run in parallel with the moves T067–T070.
- **Phase 8 (Polish)**: T075/T076/T077/T078 are 4× [P]; T079 sequential after content; T080/T081/T082 sequential at the end.

### Critical Path

T001 → T005 → T021 → T022 → (US2 longest spine: T028 → T037 → T039 → T047 → T048) → T080 → T081 → T082.

---

## Parallel Example: User Story 2 slide beats

```text
# After Phase 2 + T028 complete, fan out the 10 slide-beat tasks:
T029 [P] [US2] add agentic-shift one-liner to part-01
T030 [P] [US2] add Unix-pipe beat to part-02
T031 [P] [US2] verify part-03 skills-pointer subsection
T032 [P] [US2] verify part-04 multi-agent alternative
T033 [P] [US2] verify part-05 bundled-skills slide
T034 [P] [US2] verify part-06 @claude-actions slide
T035 [P] [US2] add multimodal-@claude beat to part-07
T036 [P] [US2] add /code-review beat to part-08
T037     [US2] verify part-09 four-pillar structure  (sequential — biggest deck)
T038 [P] [US2] verify part-10 overeager + checklist
```

## Implementation Strategy

### MVP First

1. Phase 1 Setup → Phase 2 Foundational (audit script with 15 gates).
2. Phase 3 US1 — 60-second onboarding.
3. **STOP & VALIDATE**: Hand the repo to a colleague; stopwatch SC-001.

The MVP delivers a navigable repo with a passing audit; even without US2–US5 content updates, the existing 10 decks from feature 004 keep the bootcamp deliverable today.

### Incremental Delivery

1. MVP (US1) → Repo orientation works.
2. + US2 → May-2026 story landed in decks + skills + assessments.
3. + US3 → Every exercise has a runnable solution.
4. + US4 → Audit is the standard pre-cohort gate.
5. + US5 → Archive is isolated.
6. + Polish → 33-artefact rebuild + dress rehearsal.

### Parallel Team Strategy

- One author owns Phase 2 (audit) — gating dependency.
- Once Phase 2 done: Author A → US1 (README/student-guide); Author B → US2 (slides/skills/assessments); Author C → US3 (exercises/solutions); they run in parallel.
- Author A picks up US4 after US1; Author B picks up US5 after US2.
- Single author runs Polish in the last block.

---

## Notes

- Tests are **not** generated — verification is gate-based via `scripts/preflight.sh` (per spec; no test framework adopted).
- Every `[Story]` task lives in or under the path it owns, so cross-story file conflicts are nil.
- Commit after each task or logical group; the optional `after_tasks` hook can auto-commit.
- The single Constitution divergence (`slides/dist/` tracked) is intentional and recorded in plan.md Complexity Tracking — no task here changes the gitignore policy.

---

## Summary

- **Total tasks**: 82
- **Per user story**: Setup 4 · Foundational 18 · US1 5 · US2 21 · US3 13 · US4 5 · US5 8 · Polish 8
- **Parallel opportunities**: 14 in Phase 2; 10 in Phase 4 (slide beats); 10 in Phase 5 (exercise audits); 5 in Phase 4 (assessments); 4 in Phase 8 (polish).
- **Independent test criteria**:
  - US1: SC-001 stopwatch + `audit.cross-links` green.
  - US2: 6 audit gates green + 33-artefact build.
  - US3: 3 audit gates green + dress-rehearsal runtime ≤ 5 min/solution.
  - US4: synthetic-break injection round-trip.
  - US5: `audit.archive-isolation` green + 1-link rule satisfied.
- **Suggested MVP scope**: Phase 1 + Phase 2 + Phase 3 (US1) — delivers a navigable, audited bootcamp using the existing feature-004 May-2026 content. US2/US3/US4/US5 then layer on incrementally.
- **Format validation**: every task starts with `- [ ]`, has `T0NN` ID, includes file paths, includes `[P]`/`[Story]` labels per scope rules.
