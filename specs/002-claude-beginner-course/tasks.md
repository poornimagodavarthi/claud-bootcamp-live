---
description: "Task list for feature 002-claude-beginner-course"
---

# Tasks: Claude Code Beginner Course (Claude Code 101)

**Input**: Design documents from `/specs/002-claude-beginner-course/`

**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓ (6 files), quickstart.md ✓

**Tests**: Spec does NOT explicitly request unit/integration tests. The structural validator (`scripts/validate.sh`) and the capstone smoke checker (`scripts/check-beginner-capstone.sh`) ARE the test surface for this feature and are authored as foundational infrastructure (Phase 2) rather than as separate test tasks.

**Organization**: Tasks are grouped by user story. The two P1 stories (US1, US2) deliver the MVP and the full self-paced course respectively; the two P2 stories (US3, US4) deliver the workshop and intermediate cross-link paths.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the empty sibling directory skeleton and placeholder files so the rest of the feature can be authored into stable paths.

- [X] T001 Create top-level sibling directory skeleton: `slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, `exercises/beginner/module-00-setup/starter/` (with a `.keep` file). No content yet.
- [X] T002 [P] Create empty placeholder files at repo root, each containing only a single H1 line that names the file (never a forbidden token like `TBD`/`TODO`/`FIXME`, so the validator stays green even if run mid-transition): `GLOSSARY.md` (`# Glossary`), `beginner-student-guide.md` (`# Beginner Student Guide`), `beginner-instructor-guide.md` (`# Beginner Instructor Guide`), `beginner-certificate-template.md` (`# Beginner Certificate Template`). Phases 2/3 overwrite these in full.
- [X] T003 [P] Create eight exercise directories: `exercises/beginner/part-01/` through `exercises/beginner/part-08/`, each containing empty `starter/` and `solution/` subfolders with `.keep` sentinels.
- [X] T004 [P] Create `slides/beginner/README.md` with a placeholder table header listing the 8 part numbers and minute budgets from FR-030 (rows will be filled as decks are authored).

**Checkpoint**: Empty sibling tree exists; no validator failures yet (validator extensions not loaded). Ready to wire up foundational tooling.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build and ship the validator + builder + grader so every subsequent authoring task can be verified the moment it lands. These three pieces of tooling MUST be in place before any module content is authored, because the 10-section deck contract, 7-section exercise contract, and glossary-identity rule are too easy to drift without machine enforcement.

**CRITICAL**: No user story work begins until this phase is complete.

- [X] T005 Extend `slides/deploy-pptx.sh` per [contracts/validator-extensions.md](contracts/validator-extensions.md) §R2: change deck discovery to recursive (`find slides -type f -name 'part-*.md'`), keep flat ordering for intermediate decks first, append `slides/beginner/part-*.md` in lexical order. Verify by running `slides/deploy-pptx.sh --list-decks` (or equivalent dry-run) shows all 10 intermediate + 0 beginner decks correctly.
- [X] T006 Author `scripts/check-beginner-capstone.sh` per [contracts/capstone-grader.md](contracts/capstone-grader.md): bash 3.2-compatible smoke checker that runs `add "hello"` → `list` → `delete 1` → `list` against a learner's `notes.py` in an isolated temp dir, prints `PASS <8-hex-token>` on success and `FAIL: <step>: …` on any deviation. Make it executable (`chmod +x`). Verify with `bash -n scripts/check-beginner-capstone.sh` (syntax check) and a usage-error dry run.
- [X] T007 Extend `scripts/validate.sh` per [contracts/validator-extensions.md](contracts/validator-extensions.md) §§V1–V13: add `BEG_DECK_SLUGS` + `BEG_DECK_MINS=(20 25 30 25 30 25 25 30)` parallel arrays, gate all new checks behind `[[ -d slides/beginner ]]`, reuse existing HTML-comment stripper and STRICT/LOOSE forbidden-tokens regex on beginner globs, implement V1–V13 incrementally (V13 enforces FR-012: each beginner deck's `## Show me` slide body MUST contain at least one fenced code block ```` ``` ```` or one Markdown image `![alt](path)`). After each V*, run `scripts/validate.sh` and confirm it still exits 0 against the (still mostly empty) beginner tree (V11 should emit the optional-skills `ok:`; others should emit no failures because there are no beginner decks yet).
- [X] T008 Author `GLOSSARY.md` skeleton at repo root: H1 `# Glossary`, intro line, empty H2 letter-group headings `## A`, `## C`, `## E`, `## P`, `## S`, `## T` (others added as needed). This file becomes the single source of truth in Phase 3/4 — leaving it empty for now is intentional so V8 (orphan check) initially passes trivially.
- [X] T009 [P] Author `beginner-certificate-template.md` per [contracts/validator-extensions.md](contracts/validator-extensions.md) §V12: ≤ 30 lines, includes all 5 placeholders (`{{STUDENT_NAME}}`, `{{COMPLETION_DATE}}`, `{{INSTRUCTOR_NAME}}`, `{{WORKSHOP_TITLE}}`, `{{VERIFICATION_TOKEN}}`), mirrors the intermediate course's certificate visual style. Verify V12 passes.
- [X] T010 Run `scripts/validate.sh` end-to-end. Expected: all intermediate checks pass (unchanged), beginner checks emit `ok:` for the optional-skills branch (V11), and no failures. Fix any regression introduced by T005/T007 before exiting this phase. **Note**: V10 cross-reference checks correctly fail at end of Phase 2 because the referenced files (`README.md` beginner section, `beginner-student-guide.md` body, `beginner-instructor-guide.md` body) are still placeholders; those V10 ok:s land at T048, T053, T056. All other beginner checks pass.

**Checkpoint**: Tooling complete. Validator gates the 10/7-section contracts; builder picks up beginner decks; grader is ready to verify any `notes.py`. User stories can now be authored in parallel.

---

## Phase 3: User Story 1 - Absolute beginner runs Claude Code for the first time (Priority: P1) 🎯 MVP

**Goal**: A learner with no prior AI-tool experience can clone the repo, follow `module-00-setup` end-to-end, complete Module 01, and produce `first-prompt.txt` without external help.

**Independent Test**: A non-developer (or browser-only ChatGPT user) walks through Module 00 + Module 01 cold and produces the expected `first-prompt.txt` in ≤ 30 minutes. Verified by stopwatching one such learner.

### Implementation for User Story 1

- [X] T011 [US1] Author `exercises/beginner/module-00-setup/README.md` per [contracts/exercise-7-section.md](contracts/exercise-7-section.md): walks learner through installing Node.js (link only), running `npm i -g @anthropic-ai/claude-code`, running `claude --version`, capturing the output into `first-prompt.txt`. 7 sections in order; "Before you start" lists OS + Node check; "If something went wrong" has ≥ 3 rows (PATH missing, npm permission, Node too old).
- [X] T012 [US1] Add the Module 01 glossary entries to `GLOSSARY.md` under `## C`: `Claude Code`, `CLI`, and any other terms the M1 deck will introduce. Each line in canonical format `- **Term**: One-line definition.` per [contracts/glossary-identity.md](contracts/glossary-identity.md). Sort alphabetically within each H2 group.
- [X] T013 [US1] Author `slides/beginner/part-01-meet-claude-code.md` per [contracts/deck-10-section.md](contracts/deck-10-section.md): 20-min duration marker, ≤ 8 content slides, all 10 H2 sections in order. The "Show me" slide MUST contain a real terminal transcript copied from an actual `claude --version` + first-prompt run (FR-031). The Glossary card MUST byte-identically quote the M1 entries from `GLOSSARY.md`.
- [X] T014 [US1] Author `exercises/beginner/part-01/README.md` + `starter/` (containing a `.keep` and any scaffolding) + `solution/` (containing the expected `first-prompt.txt` reference content) per [contracts/exercise-7-section.md](contracts/exercise-7-section.md). H1 MUST match the M1 deck's H1.
- [X] T015 [US1] Append the M1 row to `slides/beginner/README.md`'s deck table: part number, slug, minute budget, one-line description, link to the deck file.
- [X] T016 [US1] Create `assessments/beginner/quiz.md` with H1 + intro and add Q1 + Q2 for Module 01, each preceded by `<!-- module: 01 -->`, each with 4 options A–D. Create `assessments/beginner/answer-key.md` with H1 + intro and add the matching Q1/Q2 entries (letter + `module-01 slide-K` source + 1-sentence rationale).
- [X] T017 [US1] Run `scripts/validate.sh`. Expected new `ok:` lines: deck V1/V2/V3 for `part-01`, exercise V4/V5 for `part-01`, glossary V8 for the M1 terms, quiz V9 partial (4/16 questions tagged module 01–08 — V9 will report fail-as-incomplete here; that's expected until Phase 4 lands). Fix any unexpected failures. Build the M1 deck: `cd slides && npx --yes @marp-team/marp-cli@latest --allow-local-files --pptx -o dist/pptx/beginner/part-01-meet-claude-code.pptx beginner/part-01-meet-claude-code.md` and eyeball for slide breaks.

**Checkpoint**: User Story 1 is shippable in isolation. A new learner can clone, follow `module-00-setup/README.md`, then `exercises/beginner/part-01/README.md`, and produce `first-prompt.txt`. The quiz/certificate paths are not yet usable (US2 territory) but the first-lesson experience is end-to-end.

---

## Phase 4: User Story 2 - Self-paced learner finishes the whole course in a weekend (Priority: P1)

**Goal**: A motivated beginner completes Modules 02–08, passes the 16-question quiz with ≥ 12/16, and produces the Module 08 capstone artifact verified by the grader — all without an instructor — earning a renderable certificate.

**Independent Test**: One self-paced learner goes from `README.md` to a signed certificate in ≤ 5 hours of focused work (SC-001). Verified by timing one learner.

### Implementation for User Story 2 — Modules 02 through 07 (per-module work is parallelizable across modules; shared-file work is sequential)

> Each module M ∈ {02, 03, 04, 05, 06, 07} requires: deck, exercise (README + starter + solution), glossary additions, and 2 quiz items + answer-key entries. Deck/exercise authoring across modules is `[P]`. Glossary and quiz/answer-key edits touch shared files and MUST be serialised.

- [X] T018 [US2] Add Module 02 ("Your first conversation") glossary entries to `GLOSSARY.md` (e.g. `Prompt`, `Diff`, `Accept`, `Reject`, `Undo`).
- [X] T019 [P] [US2] Author `slides/beginner/part-02-first-conversation.md` (25 min, ≤ 10 content slides) per [contracts/deck-10-section.md](contracts/deck-10-section.md).
- [X] T020 [P] [US2] Author `exercises/beginner/part-02/{README.md,starter/,solution/}` per [contracts/exercise-7-section.md](contracts/exercise-7-section.md).
- [X] T021 [US2] Append M2 row to `slides/beginner/README.md` deck table; add Q3+Q4 to `assessments/beginner/quiz.md` (tagged `<!-- module: 02 -->`) and matching entries to `answer-key.md`.

- [X] T022 [US2] Add Module 03 ("Asking for what you want") glossary entries to `GLOSSARY.md` (e.g. `Role prompt`, `Goal prompt`, `Constraint`).
- [X] T023 [P] [US2] Author `slides/beginner/part-03-asking-for-what-you-want.md` (30 min, ≤ 12 content slides). Include ≤ 5 example prompts on "Show me" / "Try it yourself".
- [X] T024 [P] [US2] Author `exercises/beginner/part-03/{README.md,starter/,solution/}`.
- [X] T025 [US2] Append M3 row to `slides/beginner/README.md`; add Q5+Q6 to quiz + answer-key.

- [X] T026 [US2] Add Module 04 ("Reading code together") glossary entries to `GLOSSARY.md`.
- [X] T027 [P] [US2] Author `slides/beginner/part-04-reading-code-together.md` (25 min, ≤ 10 content slides).
- [X] T028 [P] [US2] Author `exercises/beginner/part-04/{README.md,starter/,solution/}`. `starter/` MUST include a small (≤ 30-line) sample source file the learner asks Claude Code to explain.
- [X] T029 [US2] Append M4 row to `slides/beginner/README.md`; add Q7+Q8 to quiz + answer-key.

- [X] T030 [US2] Add Module 05 ("Editing one file safely") glossary entries to `GLOSSARY.md` (e.g. `Reversible edit`, `Hunk`).
- [X] T031 [P] [US2] Author `slides/beginner/part-05-editing-one-file-safely.md` (30 min, ≤ 12 content slides). Include the accept/reject mental model.
- [X] T032 [P] [US2] Author `exercises/beginner/part-05/{README.md,starter/,solution/}`. Exercise MUST include a one-line `git restore` recovery step (Edge Case "bad diff breaks working copy").
- [X] T033 [US2] Append M5 row to `slides/beginner/README.md`; add Q9+Q10 to quiz + answer-key.

- [X] T034 [US2] Add Module 06 ("CLAUDE.md cheat sheet") glossary entries to `GLOSSARY.md` (e.g. `CLAUDE.md`, `Project context`).
- [X] T035 [P] [US2] Author `slides/beginner/part-06-claude-md-cheat-sheet.md` (25 min, ≤ 10 content slides). MUST embed a real working ≤ 20-line `CLAUDE.md` example per FR-032.
- [X] T036 [P] [US2] Author `exercises/beginner/part-06/{README.md,starter/,solution/}`. `starter/` MUST contain the working ≤ 20-line `CLAUDE.md` from T035 so the learner observes a behaviour change in their next prompt.
- [X] T037 [US2] Append M6 row to `slides/beginner/README.md`; add Q11+Q12 to quiz + answer-key.

- [X] T038 [US2] Add Module 07 ("Safer & smarter") glossary entries to `GLOSSARY.md` (e.g. `Secret`, `PII`, `Permission`).
- [X] T039 [P] [US2] Author `slides/beginner/part-07-safer-and-smarter.md` (25 min, ≤ 10 content slides). MUST cover the "no secrets / no PII in prompts" rule (Edge Case).
- [X] T040 [P] [US2] Author `exercises/beginner/part-07/{README.md,starter/,solution/}`. Exercise MUST NOT ask the learner to paste anything sensitive.
- [X] T041 [US2] Append M7 row to `slides/beginner/README.md`; add Q13+Q14 to quiz + answer-key.

### Implementation for User Story 2 — Module 08 capstone

- [X] T042 [US2] Add Module 08 glossary entries to `GLOSSARY.md` (e.g. `Capstone`, `Subcommand`, `Persistence`).
- [X] T043 [US2] Author `exercises/beginner/part-08/solution/notes.py` per [contracts/capstone-cli.md](contracts/capstone-cli.md): single-file Python 3.11+, ≤ 100 LOC, stdlib only, three subcommands `add/list/delete` with `notes.json` persistence. Verify with `scripts/check-beginner-capstone.sh exercises/beginner/part-08/solution/notes.py` returning `PASS <token>`.
- [X] T044 [US2] Author `exercises/beginner/part-08/starter/notes.py`: minimal stub (1–5 lines: a `# TODO` and the empty `if __name__ == "__main__":` block) so the learner does NOT start from a blank file (FR-022). Verify the grader correctly FAILs against the stub.
- [X] T045 [US2] Author `exercises/beginner/part-08/README.md` per [contracts/exercise-7-section.md](contracts/exercise-7-section.md). "What you'll build" names `notes.py`; "How to know it worked" shows the exact `scripts/check-beginner-capstone.sh` invocation and the expected `PASS <token>` line.
- [X] T046 [US2] Author `slides/beginner/part-08-putting-it-together.md` (30 min, ≤ 12 content slides). "Show me" MUST show a real captured Claude Code session producing one of the subcommands. "What's next" points to `001-bootcamp-course-materials` (per FR-006).
- [X] T047 [US2] Append M8 row to `slides/beginner/README.md`; add Q15+Q16 to quiz + answer-key.

### Implementation for User Story 2 — Self-paced wrapper

- [X] T048 [US2] Author `beginner-student-guide.md` per FR-052 (≤ 200 lines). MUST link to: install path (Module 00), 8-module reading order with minute budgets, `assessments/beginner/quiz.md`, `beginner-certificate-template.md`, and `scripts/check-beginner-capstone.sh` (with the one-line certificate-render `sed` command from quickstart.md Workflow E).
- [X] T049 [US2] Verify the certificate rendering path end-to-end: run the `sed`-substitution one-liner from `beginner-student-guide.md` against `beginner-certificate-template.md` with a real token from T043's grader run; confirm the output is valid Markdown with no leftover `{{…}}` placeholders.

### Validation for User Story 2

- [X] T050 [US2] Run `scripts/validate.sh`. Expected: ALL checks pass. Specifically: V1–V3 for all 8 beginner decks; V4–V5 for all 8 beginner exercises (and module-00-setup exempted from V5's solution check); V6 forbidden-tokens clean across all beginner files; V7 duration sum = 210; V8 zero glossary drift, zero orphans, all unique; V9 exactly 16 questions, 2 per module, all answer-key entries match; V10 cross-references intact; V11 optional-skills ok; V12 certificate placeholders complete; V13 every beginner deck's `## Show me` slide contains at least one fenced code block or image. Fix any failure before exiting this phase.
- [X] T051 [US2] Build all 8 beginner decks to PPTX via `slides/deploy-pptx.sh` (or the per-deck `npx` loop). Spot-check at least Module 01, Module 03, Module 08 PPTX outputs for slide breaks, density, and image rendering.
- [X] T052 [US2] End-to-end MVP smoke: stopwatch a maintainer cold-reading `beginner-student-guide.md` → installing → completing Modules 00–08 → taking the quiz → grading the capstone → rendering the certificate. Target ≤ 5 hours per SC-001; the maintainer can skip Module 0 install if already installed.

**Checkpoint**: User Story 2 complete. The self-paced course is shippable end-to-end with a verifiable certificate. The MVP is now complete (US1 + US2 are both P1).

---

## Phase 5: User Story 3 - Workshop facilitator runs the same content as a half-day live session (Priority: P2)

**Goal**: An instructor delivers the same 8 modules in a 180-minute live workshop using `beginner-instructor-guide.md` as the sole runbook.

**Independent Test**: An instructor runs a 180-minute dry-run hitting per-module minute budgets within ±10% (SC-004). Verified by one live or paper dry-run.

- [X] T053 [US3] Author `beginner-instructor-guide.md` per FR-053 (≤ 250 lines). MUST contain: a 180-minute schedule (8 modules × 20–30 min + one 15-min break, totaling ≤ 180 min including buffer); per-module facilitation prompts; a common-blockers table (≥ 8 rows); the grading workflow (`scripts/check-beginner-capstone.sh` invocation + "did the quiz score ≥ 12/16?"); a link back to `beginner-student-guide.md`.
- [X] T054 [US3] Paper-dry-run the workshop: have a second maintainer read `beginner-instructor-guide.md` and the 8 decks back-to-back, ticking off the minute budget per module. Adjust per-module pacing notes if any module overruns by > 10%.
- [X] T055 [US3] Run `scripts/validate.sh` and confirm V10 now passes the `beginner-instructor-guide.md → beginner-student-guide.md` cross-reference assertion.

**Checkpoint**: User Story 3 complete. The workshop path is shippable in addition to self-paced.

---

## Phase 6: User Story 4 - Existing intermediate-bootcamp learner uses this as remedial pre-work (Priority: P2)

**Goal**: A learner who hits the intermediate course's Module 1 floor too soon can pivot to this beginner course, finish it, and rejoin at Module 2 with every Claude Code term defined.

**Independent Test**: Every Claude Code concept used on `slides/part-01-setup-mindset.md`'s "Concepts" slide appears in this course's `GLOSSARY.md`. Verified by cross-reading: a `grep` of the intermediate-course Module 1 deck against `GLOSSARY.md` finds every named term.

- [X] T056 [US4] Extend the top-level `README.md` per FR-054: add a "Start here" section pointing at `beginner-student-guide.md` for new learners and `student-guide.md` for the intermediate bootcamp; include one Mermaid `flowchart LR` diagram showing `Beginner course → Intermediate bootcamp → Certificate`; include an ASCII fallback in a `<details>` block (per research.md §R7). Preserve all existing intermediate-course README content unchanged.
- [X] T057 [US4] Cross-read audit: read `slides/part-01-setup-mindset.md` (intermediate Module 1) end-to-end and confirm every Claude Code concept it names (CLAUDE.md, prompts, accept/reject diffs, terminal use, etc.) appears in this course's `GLOSSARY.md`. For any missing term, add it to `GLOSSARY.md` AND reference it on the most relevant beginner deck's Glossary card (re-trigger V8 — drift must remain zero).
- [X] T058 [US4] Add a "What's next" subsection to the M08 deck (`slides/beginner/part-08-putting-it-together.md`) explicitly linking to `001-bootcamp-course-materials` (`student-guide.md` and `slides/README.md`), so any graduate has a one-click next step (FR-006).
- [X] T059 [US4] Run `scripts/validate.sh`. Expected new `ok:` for the README cross-references (V10). Confirm V8 still passes after T057's glossary additions.

**Checkpoint**: User Story 4 complete. The two courses are bidirectionally discoverable in one direction (beginner → intermediate; intermediate-course README untouched per spec Assumption).

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, optional skill, and release readiness.

- [X] T060 [P] Run the full validator one more time and capture the output: `scripts/validate.sh | tee specs/002-claude-beginner-course/validator-output.txt`. Expected: `Result: N ok, 0 fail` with N ≥ 80 (intermediate ~35 + beginner ~45). Commit the captured output for release-record purposes.
- [X] T061 [P] Build all decks to PPTX one final time: `cd slides && ./deploy-pptx.sh`. Expected: 10 intermediate + 8 beginner PPTX files in `slides/dist/pptx/` (or its `beginner/` subfolder), each 1.5–2.5 MB. Spot-check 3 random decks for visual integrity.
- [X] T062 [P] Re-run the capstone grader against the reference solution and confirm a stable token: `scripts/check-beginner-capstone.sh exercises/beginner/part-08/solution/notes.py`. Record the token in the M08 deck's "Show me" slide (or in `beginner-student-guide.md`) as an "expected token" example for instructors.
- [X] T063 Quickstart walk-through: execute every workflow in [quickstart.md](quickstart.md) Workflows A through E end-to-end against the now-complete course. Fix any documentation drift (e.g. a path that changed during authoring).
- [X] T064 Optional skill (per FR-060 / Clarifications Q5): if any module produced an obviously reusable pattern during authoring (e.g. an "ask for a diff" prompt template), author it as `skills/beginner/<slug>/SKILL.md` following the existing 6-section SKILL contract enforced by V11. If no candidate emerged, leave `skills/beginner/` absent — V11 will emit the optional `ok:` line.
- [X] T065 Release-readiness check: tick off the constitution's release-readiness slice for the beginner course in [plan.md](plan.md) § Constitution Check: (a) 8 beginner decks build; (b) 8 beginner exercises have all 7 sections; (c) optional skills check passes; (d) `assessments/beginner/answer-key.md` references current deliverable names; (e) `GLOSSARY.md` is consistent across all decks. Document the pass in the PR description.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Setup. **BLOCKS all user stories.** The validator, builder, and grader MUST be in place before any module content is written.
- **User Story 1 (Phase 3)**: Depends on Foundational. Independently deliverable (MVP for the "first-lesson works" promise).
- **User Story 2 (Phase 4)**: Depends on Foundational. Can begin in parallel with US1 in principle; in practice Phase 4 touches the same shared files (`GLOSSARY.md`, `quiz.md`, `answer-key.md`, `slides/beginner/README.md`) that Phase 3 also touches, so coordinate sequentially per file.
- **User Story 3 (Phase 5)**: Depends on User Story 2 (needs the 8 decks to schedule against).
- **User Story 4 (Phase 6)**: Depends on User Story 2 (needs `GLOSSARY.md` substantially populated to audit against the intermediate course).
- **Polish (Phase 7)**: Depends on all user stories being complete.

### Within Each User Story

- Glossary entries for a module MUST be added BEFORE that module's deck is authored (so V8 drift check is satisfied on the first validator run after authoring).
- Deck and exercise for a module are independent — they can be authored in parallel as long as their H1 titles agree.
- Quiz entries for a module SHOULD be added AFTER that module's deck and exercise, so the question can cite a real slide/step number in the answer key.

### Parallel Opportunities

- All Setup tasks marked `[P]` (T002, T003, T004) can run concurrently after T001.
- Inside Phase 4, deck-authoring tasks across different modules are marked `[P]`: {T019, T020}, {T023, T024}, {T027, T028}, {T031, T032}, {T035, T036}, {T039, T040} — each pair can be done concurrently with the others, subject to capacity.
- Polish tasks T060, T061, T062 are independent and `[P]`.
- T009 (certificate template) is `[P]` with T008 (GLOSSARY.md skeleton) since they touch different files.

---

## Parallel Example: Phase 4 — Modules 02 through 07 in parallel

If you have multiple authors available, the following six deck+exercise pairs can be worked concurrently after T018 (and its analogs T022, T026, T030, T034, T038) have appended the relevant glossary entries:

```text
Author A: T019 + T020   (Module 02)
Author B: T023 + T024   (Module 03)
Author C: T027 + T028   (Module 04)
Author D: T031 + T032   (Module 05)
Author E: T035 + T036   (Module 06)
Author F: T039 + T040   (Module 07)
```

The serialised follow-ups (T021, T025, T029, T033, T037, T041 — quiz + deck-table edits) MUST be queued through one author at a time because they all touch the same three shared files.

---

## Implementation Strategy

**MVP scope** = Phase 1 + Phase 2 + Phase 3 only. After T017 the repository has:
- A working extended validator
- A working capstone grader
- The Module 00 setup walkthrough
- Module 01 deck + exercise + 2 quiz items
- A populated certificate template (rendered against a placeholder run)

A learner can clone, run Module 00, complete Module 01, and produce `first-prompt.txt`. The full certificate path is NOT yet available (US2 owns that), but the foundational "Claude Code is alive on my machine" promise is shippable.

**Incremental delivery**:
1. Ship MVP (Phases 1+2+3) → publish as a `v0.1` tag if external visibility is desired.
2. Complete US2 (Phase 4) → publish `v1.0` (full self-paced course + certificate).
3. Complete US3 (Phase 5) → publish `v1.1` (workshop path added).
4. Complete US4 (Phase 6) → publish `v1.2` (intermediate bridge added).
5. Polish (Phase 7) → patch release.

Each version above passes `scripts/validate.sh` cleanly; partial completion of a phase MUST NOT be merged.
