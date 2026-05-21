---
description: "Task list for Claude Code Bootcamp — Course Materials Repository"
---

# Tasks: Claude Code Bootcamp — Course Materials Repository

**Input**: Design documents in `specs/001-bootcamp-course-materials/`
(spec.md, plan.md, research.md, data-model.md, contracts/, quickstart.md)

**Tests**: This is a content repository; "tests" are structural validation
runs of `scripts/validate.sh` plus reference-solution self-tests for
code-producing modules. Test tasks are included where they enforce a spec
requirement.

**Organization**: Tasks are grouped per the user's requested 20-section
breakdown (Repository foundation → Final quality review). User-story tags
([US1], [US2], [US3], [US4]) trace each task back to spec.md user stories
for accountability and parallel-team planning. Within each group, tasks
are listed in execution order; `[P]` marks tasks that touch independent
files and can run in parallel with siblings in the same group.

## Format

`- [ ] T### [P?] [Story?] Description with file path`

Each task is followed by an indented **Acceptance** bullet describing
the deterministic pass condition.

---

## Phase 1: Repository foundation

**Purpose**: Scaffold the repository skeleton, licenses, gitignore, and
agent context. Blocking for every later phase.

- [X] T001 Create top-level directory tree: `slides/`, `exercises/part-01/` through `exercises/part-10/`, `skills/`, `assessments/`, `scripts/`, `.github/`
  - **Acceptance**: `find . -type d -maxdepth 2` lists all 4 top-level content directories and 10 `exercises/part-NN/` subdirectories; no extras. Existing `slides/` and `.github/` retained.
- [X] T002 [P] Create `.gitignore` excluding `slides/dist/`, `.DS_Store`, `node_modules/`, `__pycache__/`, `.venv/`, `*.pyc`, `dist/`
  - **Acceptance**: `git check-ignore slides/dist/foo.pptx` returns the path; no committed artifact under `slides/dist/`.
- [X] T003 [P] Create top-level `LICENSE` containing the full Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license text (FR-005a)
  - **Acceptance**: First line matches "Creative Commons Attribution-NonCommercial-ShareAlike 4.0"; full canonical text present (no truncation).
- [X] T004 [P] Create `skills/LICENSE` containing the full MIT License text with copyright "© 2026 Luca Berton" (FR-005a)
  - **Acceptance**: File contains canonical MIT permission grant; the copyright line names Luca Berton and year 2026.
- [X] T005 [P] Create `skills/README.md` index listing all 10 skills with one-line descriptions and noting MIT licensing and project-agnostic usage
  - **Acceptance**: File lists every skill directory in the FR-016 set; explicitly states "Licensed MIT — safe for commercial reuse"; no bootcamp-specific paths.

**Checkpoint**: Repository skeleton exists; all later groups can write into known paths.

---

## Phase 2: README

**Purpose**: Author the public-facing landing document that anchors
cross-artifact consistency (constitution Principle IX).

- [X] T006 [US1, US2] Create `README.md` covering all FR-005 elements: title, **Packt Certification** branding (verbatim) + "LLM Engineering by Packt" parent line, instructor (Luca Berton), inaugural delivery date (30 May 2026, 09:00 AM EST, live virtual), 5h duration (4h instruction + 1h breaks/Q&A), audience, prerequisites, learning outcomes, the **per-module schedule table with the canonical minute budget (M1=20, M2=24, M3=22, M4=30, M5=28, M6=22, M7=30, M8=24, M9=22, M10=18 = 240)** and deliverables, the 10 projects, repository layout, build instructions, assessment policy (40/40/20, 70% pass), dual-license section (FR-005, FR-005a, FR-010)
  - **Acceptance**: README contains H2 sections "Schedule", "Projects", "Repository layout", "Build", "Assessment", "License"; Schedule section is a Markdown table with one row per module showing minutes that sum to 240; license section names CC BY-NC-SA 4.0 for course materials and MIT for `skills/`; module 5 deliverable named "Code Review Rubric"; project list matches FR-011 order; the strings "Packt Certification" and "LLM Engineering by Packt" appear verbatim; date "30 May 2026" + "09:00 AM EST" present.

---

## Phase 3: Slide infrastructure

**Purpose**: Establish Marp build conventions and the per-deck contract
file index before authoring deck content. Unblocks all 10 deck tasks.

- [X] T007 [US1] Create `slides/README.md` documenting deck naming (`part-NN-<slug>.md`), required Marp frontmatter, the 14-section contract reference, and render commands (`./deploy-pptx.sh`, `--pdf`, `--html`, `--all`, `--clean`)
  - **Acceptance**: File enumerates the 10 deck filenames matching FR-001; references `specs/001-bootcamp-course-materials/contracts/slide-deck.contract.md`; lists every flag supported by `deploy-pptx.sh`.
- [X] T008 [US1] Rename `slides/part-09-automation.md` → `slides/part-09-skills-workflows.md` and `slides/part-10-production.md` → `slides/part-10-production-readiness.md`; update any internal links
  - **Acceptance**: `git mv` recorded; `grep -r "part-09-automation\|part-10-production\.md" .` returns no matches outside `specs/`.

---

## Phase 4: Instructor guide

**Purpose**: Deliver everything an instructor needs for solo onboarding,
live facilitation, and grading (FR-024, US1).

- [X] T009 [US1, US4] Create `instructor-guide.md` with H2 sections: Pre-flight checklist (env, accounts, AV), **Per-module timing & facilitation (10 subsections — one per module, each headed with the canonical minute budget from FR-010: M1=20, M2=24, M3=22, M4=30, M5=28, M6=22, M7=30, M8=24, M9=22, M10=18)**, "If running short" cuts per module, Common student blockers, **Pre-work verification** (how to confirm a student's `module-00-prework/` smoke-test output before grading), Grading workflow (zip retrieval from Packt LMS, local rubric scoring, reference-solution validation), Certificate issuance procedure (FR-024, FR-023a, FR-025a)
  - **Acceptance**: All 10 modules have a per-module facilitation subsection with the exact minute budget in its heading; minute budgets sum to 240; grading section explicitly references `assessments/rubric.md`, `assessments/answer-key.md`, the `module-00-prework/` folder, and reference solutions under `exercises/part-NN/solution/`; pre-flight names Marp/Chromium/Claude Code/Git.

---

## Phase 5: Student guide

**Purpose**: Deliver the student onboarding, pre-work, and submission
contract (FR-025, FR-025a, FR-023a, US2).

- [X] T010 [US2] Create `student-guide.md` with H2 sections: Prerequisites, Environment setup (Python 3.11+, Node.js 20+ for modules 2/4/5, WSL2 note for Windows), How to follow the modules, Submission workflow (zip layout `module-00-prework/` + `module-01/`…`module-10/` + `assessments/`, upload to Packt LMS), Assessment & certificate path (FR-025, FR-023a, FR-027a)
  - **Acceptance**: File documents WSL2 as the only Windows path (FR-027a); zip layout subsection lists 12 top-level folders (`module-00-prework/`, `module-01/`…`module-10/`, `assessments/`); references `assessments/` files by exact name.
- [X] T011 [US2] Add "Mandatory pre-work (~30 min)" H2 section to `student-guide.md` covering environment setup, Claude Code authentication, repository clone, and a "hello-Claude" smoke test; the section MUST end with a copy-paste block the student saves as `module-00-prework/hello-claude.txt` inside their submission zip (FR-025a, FR-023a)
  - **Acceptance**: Section states pre-work is an entry condition for the live session; smoke test prompt is a single copy-paste block; checklist includes a place to paste Claude's reply; explicit instruction to save the captured output to `module-00-prework/hello-claude.txt`; instructor-guide cross-link explains the verification step.

---

## Phase 6: Module 1 materials — Welcome, Setup & AI-First Mindset

**Deliverable**: AI Coding Workspace. Conceptual module — no `solution/`.

- [X] T012 [P] [US1] Author/expand `slides/part-01-setup-mindset.md` to satisfy the 14-section slide-deck contract for the "AI-First Mindset" module (FR-006, FR-007, FR-008, FR-009)
  - **Acceptance**: File contains all 14 H2 sections in contract order; Marp frontmatter has `marp: true`, `theme`, `paginate`, `size`, `title`, `description`; `<!-- duration: 20 min -->` marker present; ≥2 ready-to-paste Claude Code prompts in "Suggested Claude Code prompts"; Definition of done is a pass/fail checklist; live session covers mindset + 5-min verification only (FR-025a).
- [X] T013 [P] [US2] Create `exercises/part-01/README.md` with all 9 exercise sections targeting the AI Coding Workspace deliverable (FR-012, FR-014)
  - **Acceptance**: All 9 H2 sections present in contract order; "Manual validation steps" lists deterministic checks (file exists / command output match); Claude Code prompt block is copy-paste-ready; no `solution/` directory required.

---

## Phase 7: Module 2 materials — Prompting Like a Tech Lead

**Deliverable**: CLI Task Manager. Code-producing — Python primary + Node secondary.

- [X] T014 [P] [US1] Author `slides/part-02-prompting.md` to satisfy the 14-section slide-deck contract; topic = prompting structure & big-prompt pattern; deliverable = CLI Task Manager (FR-006, FR-007)
  - **Acceptance**: 14 sections present; ≥2 prompts; "Mini project" + "Step-by-step lab" describe building a CLI task manager; duration marker matches schedule.
- [X] T015 [P] [US2] Create `exercises/part-02/README.md` with all 9 sections; deliverable = CLI task manager; document Python primary + Node.js secondary tracks (FR-013, FR-015a)
  - **Acceptance**: 9 H2 sections; explicit "Python (primary)" and "Node.js (secondary)" subsections under "Starter instructions"; `solution/` mentioned with "Do not open before completing the lab" notice; manual validation lists CLI commands with expected outputs.
- [X] T016 [P] [US2] Implement Python reference solution at `exercises/part-02/solution/python/` (argparse stdlib CLI: add/list/done/delete tasks, JSON file persistence, `python -m task_manager` runnable, smoke-test commands)
  - **Acceptance**: `cd exercises/part-02/solution/python && python -m task_manager add "test" && python -m task_manager list` shows the task; only stdlib used (no external deps in `requirements.txt`).
- [X] T017 [P] [US2] Implement Node.js reference solution at `exercises/part-02/solution/node/` (TypeScript + commander + tsx, package.json scripts, equivalent CLI surface to Python track)
  - **Acceptance**: `cd exercises/part-02/solution/node && npm install && npx tsx src/index.ts add "test" && npx tsx src/index.ts list` succeeds; CLI command names match Python track; README in `solution/node/` lists the install/run steps.

---

## Phase 8: Module 3 materials — Project Context with CLAUDE.md

**Deliverable**: Project Brain File. Conceptual module — no `solution/`.

- [X] T018 [P] [US1] Author `slides/part-03-claude-md.md` to satisfy the 14-section contract; topic = CLAUDE.md authoring; deliverable = Project Brain File (FR-006)
  - **Acceptance**: 14 sections; ≥2 prompts that produce a CLAUDE.md; live demo flow walks through anatomy of a CLAUDE.md.
- [X] T019 [P] [US2] Create `exercises/part-03/README.md` with all 9 sections; deliverable = a CLAUDE.md committed to the student's project (FR-012)
  - **Acceptance**: 9 sections; manual validation = file exists at repo root + Claude Code uses it on next prompt; cross-references `skills/claude-md-template/SKILL.md`.

---

## Phase 9: Module 4 materials — Build Faster with Best-of-N

**Deliverable**: Notes App API. Code-producing — Python primary + Node secondary.

- [X] T020 [P] [US1] Author `slides/part-04-best-of-n.md` to satisfy the 14-section contract; topic = Best-of-N pattern; deliverable = Notes App API (FR-006)
  - **Acceptance**: 14 sections; live demo flow shows generating N candidates and selecting; ≥2 prompts.
- [X] T021 [P] [US2] Create `exercises/part-04/README.md` with all 9 sections; deliverable = Notes App REST API; document Python (FastAPI) + Node.js (Hono) tracks (FR-013, FR-015a)
  - **Acceptance**: 9 sections; manual validation lists `curl` commands against `/notes` with expected JSON payloads; both tracks documented; `solution/` notice present.
- [X] T022 [P] [US2] Implement Python reference solution at `exercises/part-04/solution/python/` (FastAPI + Pydantic v2 + SQLite via stdlib `sqlite3`, full CRUD on `/notes`, `uvicorn` run command, `requirements.txt`)
  - **Acceptance**: `pip install -r requirements.txt && uvicorn app:app` starts; `curl -X POST localhost:8000/notes -d '{"text":"a"}'` and `curl localhost:8000/notes` return matching IDs; pinned versions in `requirements.txt`.
- [X] T023 [P] [US2] Implement Node.js reference solution at `exercises/part-04/solution/node/` (Hono + Zod + better-sqlite3, equivalent CRUD)
  - **Acceptance**: `npm install && npm run dev` starts; same curl flow returns JSON parity with Python track; `package.json` lists pinned versions.

---

## Phase 10: Module 5 materials — Testing, Debugging & Self-Review

**Deliverable**: Tests + Bug Fixes + **Code Review Rubric**. Code-producing — Python + Node.

- [X] T024 [P] [US1] Author `slides/part-05-testing-debugging.md` to satisfy the 14-section contract; topic = AI-assisted test generation, debugging, self-review; deliverable explicitly named "Tests + Bug Fixes + Code Review Rubric" (FR-006, FR-011)
  - **Acceptance**: 14 sections; deliverable name uses "Code Review Rubric" verbatim; ≥2 prompts (one for test gen, one for code review); references `exercises/part-05/code-review-rubric.md`, NOT `assessments/rubric.md`.
- [X] T025 [P] [US2] Create `exercises/part-05/README.md` with all 9 sections; deliverable = pytest test suite + 2 bug fixes + Code Review Rubric (FR-011, FR-012)
  - **Acceptance**: 9 sections; deliverable list explicitly mentions `code-review-rubric.md` filename; both tracks (Python pytest, Node vitest) documented; `solution/` notice present.
- [X] T026 [P] [US2] Create `exercises/part-05/code-review-rubric.md` (the **student-built** Code Review Rubric template — distinct from `assessments/rubric.md`) (FR-011)
  - **Acceptance**: File header names it "Code Review Rubric (student artifact — module 5)"; file is a template the student fills in; it is NOT the instructor grading rubric; cross-references zero paths under `assessments/`.
- [X] T027 [P] [US2] Implement Python reference solution at `exercises/part-05/solution/python/` (pytest + httpx test suite for the module 4 Notes API solution, plus 2 deliberate bug-fix commits demonstrated in commit history or `BUGS.md`)
  - **Acceptance**: `pytest -q` passes; ≥10 test cases covering happy path + edge cases + error paths; `BUGS.md` documents the 2 fixes traced to commits.
- [X] T028 [P] [US2] Implement Node.js reference solution at `exercises/part-05/solution/node/` (vitest test suite for module 4 Node solution; matching `BUGS.md`)
  - **Acceptance**: `npm test` passes; ≥10 test cases; `BUGS.md` mirrors Python track structure.

---

## Phase 11: Module 6 materials — Git Workflows for Safe AI Dev

**Deliverable**: Feature Branch Workflow. Conceptual module — no `solution/`.

- [X] T029 [P] [US1] Author `slides/part-06-git-workflows.md` to satisfy the 14-section contract; topic = Git workflow with AI-generated commits/PRs (FR-006)
  - **Acceptance**: 14 sections; live demo flow shows feature branch → AI-generated commit message → PR description; ≥2 prompts (commit msg, PR body).
- [X] T030 [P] [US2] Create `exercises/part-06/README.md` with all 9 sections; deliverable = a documented feature-branch workflow run on a sample repo (FR-012)
  - **Acceptance**: 9 sections; manual validation = `git log --oneline` shows expected commit pattern + PR link or `BRANCHING.md` artifact present; cross-references `skills/git-workflow/SKILL.md`.

---

## Phase 12: Module 7 materials — Multimodal: Screenshot to UI

**Deliverable**: Dashboard UI. Code-producing — Python only (FR-013).

- [X] T031 [P] [US1] Author `slides/part-07-multimodal.md` to satisfy the 14-section contract; topic = multimodal input (screenshots/wireframes → code) (FR-006)
  - **Acceptance**: 14 sections; live demo flow uses the canonical wireframe; ≥2 prompts; deliverable = Dashboard UI from wireframe.
- [X] T032 [P] [US2] Author wireframe **sources** and render PNGs for module 7. Commit the canonical wireframe as Mermaid source `exercises/part-07/wireframe.mmd` and render to `exercises/part-07/wireframe.png` via `npx -y @mermaid-js/mermaid-cli -i wireframe.mmd -o wireframe.png`. Commit the hand-sketch variant as Excalidraw-exported SVG `exercises/part-07/wireframe-sketch.svg` and a converted PNG at `exercises/part-07/wireframe-sketch.png` (e.g., via `npx -y @resvg/resvg-js wireframe-sketch.svg wireframe-sketch.png` or equivalent). Document both render commands in `exercises/part-07/README.md` so reviewers can reproduce them. (FR-015b)
  - **Acceptance**: Both source files (`wireframe.mmd`, `wireframe-sketch.svg`) and both PNGs (`wireframe.png`, `wireframe-sketch.png`) are committed; `file wireframe.png` reports valid PNG; the canonical render is computer-generated and clean; the sketch render is hand-drawn style; both depict the same dashboard layout so the reference solution matches both; render commands documented in the exercise README and reproducible from a clean clone with only Node.js installed.
- [X] T033 [US2] Create `exercises/part-07/README.md` with all 9 sections; deliverable = Dashboard UI matching `wireframe.png`; references both wireframe assets (FR-012, FR-015b) — *depends on T032 (asset paths)*
  - **Acceptance**: 9 sections; manual validation steps reference `wireframe.png` and the rendered output side-by-side; explicitly Python-only (no Node track); `solution/` notice present.
- [X] T034 [P] [US2] Implement Python reference solution at `exercises/part-07/solution/` (single-page dashboard rendering the canonical wireframe — minimal Flask + HTML/CSS, or Streamlit, chosen per `research.md` R3) (FR-015b)
  - **Acceptance**: `python app.py` (or `streamlit run app.py`) starts; rendered output visually matches `wireframe.png` layout (same panels, same positions); rubric-scorable per the contract.

---

## Phase 13: Module 8 materials — Refactoring & Documentation at Scale

**Deliverable**: Refactor + Handoff Docs. Code-producing — Python only.

- [X] T035 [P] [US1] Author `slides/part-08-refactor-docs.md` to satisfy the 14-section contract; topic = AI-driven refactor + documentation generation (FR-006)
  - **Acceptance**: 14 sections; live demo flow shows refactor under constraints + generating handoff docs; ≥2 prompts.
- [X] T036 [P] [US2] Create `exercises/part-08/README.md` with all 9 sections; deliverable = refactored module + handoff documentation set (FR-012)
  - **Acceptance**: 9 sections; manual validation = pytest still passes after refactor + `HANDOFF.md` and `ARCHITECTURE.md` present; Python only.
- [X] T037 [P] [US2] Implement Python reference solution at `exercises/part-08/solution/` (a "before" module + the refactored "after" + generated `HANDOFF.md` and `ARCHITECTURE.md`)
  - **Acceptance**: `pytest` passes against the "after" code; `HANDOFF.md` includes setup, run, test, deploy sections; `ARCHITECTURE.md` includes a module map.

---

## Phase 14: Module 9 materials — Commands, Hooks & Reusable Workflows

**Deliverable**: Personal Claude Skills / Command Library. Conceptual — uses `skills/`.

- [X] T038 [P] [US1] Author `slides/part-09-skills-workflows.md` to satisfy the 14-section contract; topic = SKILL.md packaging, slash commands, hooks; deliverable = personal skills library (FR-006)
  - **Acceptance**: 14 sections; live demo flow shows authoring a SKILL.md and invoking it; cross-references `skills/` directory; ≥2 prompts.
- [X] T039 [P] [US2] Create `exercises/part-09/README.md` with all 9 sections; deliverable = student authors at least one new SKILL.md following the bootcamp's skill contract (FR-012, FR-016, FR-017)
  - **Acceptance**: 9 sections; manual validation = student's new skill loads in Claude Code (frontmatter parses) and produces output on test prompt; cross-references `skill.contract.md`.

---

## Phase 15: Module 10 materials — Production Readiness

**Deliverable**: Production Readiness Report. Conceptual — no `solution/`.

- [X] T040 [P] [US1] Author `slides/part-10-production-readiness.md` to satisfy the 14-section contract; topic = production readiness review framework (FR-006)
  - **Acceptance**: 14 sections; ≥2 prompts; deliverable = a production-readiness report; cross-references `skills/production-readiness-review/SKILL.md` and `skills/security-checklist/SKILL.md`.
- [X] T041 [P] [US2] Create `exercises/part-10/README.md` with all 9 sections; deliverable = production-readiness report on the student's choice of one prior module's project (FR-012)
  - **Acceptance**: 9 sections; manual validation = report contains all rubric headings (security, observability, deployment, runbooks, rollback); template provided in starter instructions.

---

## Phase 16: Claude Skills library

**Purpose**: Author all 10 Claude Code-native `SKILL.md` files
(FR-016, FR-017, FR-018, US3). Each skill is project-agnostic and
follows `contracts/skill.contract.md`.

- [X] T042 [P] [US3] Create `skills/claude-md-template/SKILL.md` (frontmatter `name: claude-md-template`, one-line `description`; 6 body sections)
  - **Acceptance**: Frontmatter parses; all 6 H2 sections (Purpose, When to use, Body, Inputs, Outputs, Worked example) present in order; no path/repo assumptions; worked example produces a CLAUDE.md.
- [X] T043 [P] [US3] Create `skills/code-review/SKILL.md` (matches contract; aligned with module 5 teaching)
  - **Acceptance**: 6 sections; "When to use" lists ≥3 trigger scenarios; worked example covers a small diff review.
- [X] T044 [P] [US3] Create `skills/test-generation/SKILL.md` (aligned with module 5)
  - **Acceptance**: 6 sections; worked example generates pytest cases for a sample function.
- [X] T045 [P] [US3] Create `skills/best-of-n/SKILL.md` (aligned with module 4)
  - **Acceptance**: 6 sections; "Body" specifies N, evaluation criteria, selection step; worked example produces N candidates + chosen winner.
- [X] T046 [P] [US3] Create `skills/refactor/SKILL.md` (aligned with module 8)
  - **Acceptance**: 6 sections; constraints input clearly listed; worked example shows before/after.
- [X] T047 [P] [US3] Create `skills/release-notes/SKILL.md`
  - **Acceptance**: 6 sections; worked example consumes a `git log` and produces categorized release notes.
- [X] T048 [P] [US3] Create `skills/security-checklist/SKILL.md` (aligned with module 10)
  - **Acceptance**: 6 sections; checklist body covers OWASP top categories; worked example reports findings on a sample snippet.
- [X] T049 [P] [US3] Create `skills/git-workflow/SKILL.md` (aligned with module 6)
  - **Acceptance**: 6 sections; body covers branch / commit msg / PR description templates; worked example shows full feature flow.
- [X] T050 [P] [US3] Create `skills/documentation-generation/SKILL.md` (aligned with module 8)
  - **Acceptance**: 6 sections; worked example produces README + ARCHITECTURE for a sample module.
- [X] T051 [P] [US3] Create `skills/production-readiness-review/SKILL.md` (aligned with module 10)
  - **Acceptance**: 6 sections; body covers security / observability / deployment / runbooks / rollback dimensions; worked example reports on a sample app.

---

## Phase 17: Assessment materials

**Purpose**: Author the 5 assessment artifacts implementing the
40/40/20 weighting and 70% pass rule (FR-019–FR-022, US2).

- [X] T052 [P] [US2] Create `assessments/knowledge-quiz.md` covering the 10 sample topics (prompt structure, CLAUDE.md, AI code review, Git for AI workflows, Best-of-N, test generation, unsafe-output detection, refactor with constraints, multimodal inputs, production readiness); plain Markdown only (FR-019)
  - **Acceptance**: ≥20 scored items distributed across the 10 topic areas; each item has a stable ID; no machine-gradable export format used; total point value matches the 40% weight stated in `rubric.md`.
- [X] T053 [P] [US2] Create `assessments/practical-task.md` defining the graded mini-build aligned with the curriculum (FR-020)
  - **Acceptance**: Task brief includes scope, time budget, deliverables list, scoring dimensions; references the rubric's practical-component criteria.
- [X] T054 [P] [US2] Create `assessments/code-review-reflection.md` defining the written reflection task (FR-021)
  - **Acceptance**: Prompt + word count target + scoring dimensions stated; references the rubric's reflection criteria.
- [X] T055 [P] [US2] Create `assessments/rubric.md` with the 40/40/20 weighting, 70% pass threshold, per-component criteria, and grading workflow notes (FR-022)
  - **Acceptance**: Component weights sum to 100%; pass threshold stated as 70%; explicitly distinct from `exercises/part-05/code-review-rubric.md` (a note in the header clarifies this); per-component criteria tables present.
- [X] T056 [US2] Create `assessments/answer-key.md` with answers/scoring guidance for every quiz item authored in T052 (FR-022) — *depends on T052*
  - **Acceptance**: Every quiz item ID from T052 has a corresponding answer entry; partial-credit guidance documented where applicable.

---

## Phase 18: Certificate template

**Purpose**: Issuable Packt-endorsed Certificate of Completion
(FR-023, US2).

- [X] T057 [US2] Create `certificate-template.md` with placeholders for student name, date, instructor signature (Luca Berton), workshop title, and Packt Publishing endorsement language (FR-023)
  - **Acceptance**: File contains `{{STUDENT_NAME}}`, `{{COMPLETION_DATE}}`, `{{INSTRUCTOR_NAME}}` (default Luca Berton), `{{WORKSHOP_TITLE}}` placeholders; "Endorsed by Packt Publishing" line present; instructor-guide cross-link included.

---

## Phase 19: Build script

**Purpose**: Self-bootstrapping Marp build (FR-002, FR-003, FR-004,
SC-008). The repo already contains `slides/deploy-pptx.sh` from prior
work; this phase brings it into spec compliance.

- [X] T058 [US1, US4] Update `slides/deploy-pptx.sh` to: detect global `marp`, fall back to `npx --yes @marp-team/marp-cli@latest`; output to `slides/dist/`; support flags `--pdf`, `--html`, `--all`, `--clean`; document `CHROME_PATH` override in script header (FR-002, FR-003)
  - **Acceptance**: `slides/deploy-pptx.sh --clean` removes `slides/dist/`; `slides/deploy-pptx.sh` produces 10 PPTX files in `slides/dist/`; `--all` produces PPTX+PDF+HTML for each deck; script header lists every flag and the `CHROME_PATH` env var.
- [X] T059 [US1] Run a clean build smoke test: from a fresh clone, `cd slides && ./deploy-pptx.sh` succeeds end-to-end with only Node.js installed (SC-008)
  - **Acceptance**: Build completes in <3 min after first-run install; exit code 0; `ls slides/dist/*.pptx | wc -l` = 10.

---

## Phase 20: Final quality review

**Purpose**: Cross-artifact validation, structural enforcement,
quickstart smoke test, and release sign-off (constitution Principle IX,
SC-001, SC-002, SC-003, SC-007, US4).

- [X] T060 [US4] Create `scripts/validate.sh` enforcing: every `slides/part-NN-*.md` has the 14 required H2 sections; every `slides/part-NN-*.md` has a `<!-- duration: NN min -->` marker matching the canonical FR-010 budget (M1=20, M2=24, M3=22, M4=30, M5=28, M6=22, M7=30, M8=24, M9=22, M10=18); every `exercises/part-NN/README.md` has the 9 required H2 sections; every `skills/*/SKILL.md` has YAML frontmatter (`name`, `description`) plus the 6 body H2 sections; the 10-project list is identical across `README.md`, slides, exercises, and `assessments/rubric.md`; module instruction times sum to 240; **forbidden-tokens regex (FR-027b)** scans `README.md`, `instructor-guide.md`, `student-guide.md`, `certificate-template.md`, `slides/part-*.md`, `exercises/part-*/README.md`, `assessments/*.md`, and `skills/*/SKILL.md` (excluding HTML comments and the `specs/`/`.specify/` directories) and fails on any case-insensitive match of: `TODO`, `TBD`, `FIXME`, `XXX`, `coming soon`, `placeholder`, `lorem ipsum`, `unleash`, `revolutioniz`, `revolutionary`, `game[- ]chang`, `cutting[- ]edge`, `world[- ]class`, `next[- ]gen`, `rockstar`, `ninja`, `transform your`, `master(?:ing)? the art` (constitution II, IX; FR-026, FR-027, FR-027b, FR-028)
  - **Acceptance**: `bash scripts/validate.sh` exits 0 on a clean repo; injecting any contract violation (delete a section, rename a project, set a wrong duration marker, plant the word `unleash` in any delivery file) makes it exit non-zero with a clear error pointing at the file + missing section / wrong minute / forbidden token + line number; per-deck duration breakdown is printed.
- [X] T061 [US4] Run `scripts/validate.sh` against the populated repository and resolve every reported error (SC-002, SC-003, SC-007) — *depends on T060 and all module/skill/assessment authoring tasks*
  - **Acceptance**: `bash scripts/validate.sh` completes in <10s and exits 0; output lists all 10 decks, 10 exercises, 10 skills as ✓ pass; total instruction-minutes line is in [235, 245].
- [X] T062 [US1] Execute `specs/001-bootcamp-course-materials/quickstart.md` end-to-end on a clean clone, timing each step (SC-001) — *depends on T058, T059, T009, T060*
  - **Acceptance**: Total wall-clock time ≤ 30 minutes; each table row's actual time recorded; any step that overruns is fixed before sign-off.
- [X] T063 [P] [US2] Reference-solution self-test sweep: for each of `exercises/part-{02,04,05,07,08}/solution/...`, run that solution's documented validation commands (FR-015a) — *depends on T016, T017, T022, T023, T027, T028, T034, T037*
  - **Acceptance**: Every solution's validation commands exit 0; for module 5, both tracks' test suites are green; module 7 reference UI renders the canonical wireframe.
- [X] T064 [P] [US3] Skill portability spot-check: copy `skills/code-review/`, `skills/test-generation/`, and `skills/best-of-n/` into a throwaway unrelated repository and invoke each via Claude Code (SC-010) — *depends on T043, T044, T045*
  - **Acceptance**: Each of the 3 skills produces useful output without edits to the SKILL.md file; no path or filename inside the skill references the bootcamp repo.
- [X] T065 [US4] Cross-artifact terminology pass: confirm "Code Review Rubric" (module 5 student deliverable) is used in every cross-reference and is never confused with `assessments/rubric.md` (FR-011, FR-028) — *depends on T024, T025, T026, T055, T006*
  - **Acceptance**: `grep -rn "rubric" --include="*.md" .` shows two distinct artifact types — `exercises/part-05/code-review-rubric.md` (student) and `assessments/rubric.md` (instructor) — with zero ambiguous references; README's project list uses "Code Review Rubric" verbatim.

---

## Dependencies & Execution Order

### Group dependencies

- **Phase 1 (foundation)**: starts immediately, blocks every later phase.
- **Phase 2 (README)**: depends on Phase 1 (paths exist).
- **Phase 3 (slide infra)**: depends on Phase 1; blocks Phases 6–15 deck tasks.
- **Phases 4–5 (guides)**: depend on Phase 1; can run in parallel with module phases.
- **Phases 6–15 (modules 1–10)**: depend on Phase 3 (slides README + rename) and Phase 1 (exercise dirs); can run in parallel across modules; within each module the deck task and exercise task are independent (`[P]`) but module 7's exercise README depends on its wireframe assets (T033 ← T032).
- **Phase 16 (skills)**: depends on Phase 1 (`skills/` exists, `skills/LICENSE` present); all 10 skill tasks parallelizable.
- **Phase 17 (assessments)**: depends on Phase 1 + Phase 11 (module 5 deliverable name finalized) + Phase 2 (rubric must reference README's project list); T056 depends on T052.
- **Phase 18 (certificate)**: depends on Phase 1.
- **Phase 19 (build script)**: T058 can run any time after Phase 3; T059 depends on Phase 6–15 deck tasks (the decks must exist).
- **Phase 20 (final review)**: T060 can be authored early; T061 depends on T060 + all module/skill/assessment authoring; T062 depends on T058, T059, T009, T060; T063 depends on every reference-solution task; T064 depends on the 3 named skills; T065 depends on the cross-referencing tasks listed.

### Per-task ordering inside modules

- Deck task (`T012`, `T014`, `T018`, `T020`, `T024`, `T029`, `T031`, `T035`, `T038`, `T040`) and exercise README task can be authored in parallel.
- Reference-solution tasks (Python and Node) are `[P]` siblings — independent files.
- Module 7: wireframe assets (T032) **must** land before exercise README (T033) since the README references the asset filenames; the solution (T034) can be authored in parallel with T033 once T032 lands.

### Parallel opportunities

- Phase 1 tasks T002–T005 are all `[P]`.
- All 10 deck tasks are `[P]` across phases 6–15 (different files).
- All 10 exercise README tasks are `[P]` across phases 6–15 (different files).
- All 8 reference-solution tasks (T016, T017, T022, T023, T027, T028, T034, T037) are `[P]` (different directories).
- All 10 SKILL.md tasks (T042–T051) are `[P]`.
- All 4 assessment authoring tasks T052–T055 are `[P]`; T056 sequential after T052.
- T063 and T064 in Phase 20 are `[P]` siblings.

---

## Parallel Execution Examples

### Module 4 (Best-of-N) — full module in parallel

```bash
# After Phase 3 completes, four developers can work on module 4 concurrently:
Task: "Author slides/part-04-best-of-n.md (T020)"
Task: "Create exercises/part-04/README.md (T021)"
Task: "Implement exercises/part-04/solution/python/ (T022)"
Task: "Implement exercises/part-04/solution/node/ (T023)"
```

### Skills library — 10-way parallel

```bash
# After Phase 1 completes, all 10 skills authored simultaneously:
Task: "Create skills/claude-md-template/SKILL.md (T042)"
Task: "Create skills/code-review/SKILL.md (T043)"
Task: "Create skills/test-generation/SKILL.md (T044)"
Task: "Create skills/best-of-n/SKILL.md (T045)"
Task: "Create skills/refactor/SKILL.md (T046)"
Task: "Create skills/release-notes/SKILL.md (T047)"
Task: "Create skills/security-checklist/SKILL.md (T048)"
Task: "Create skills/git-workflow/SKILL.md (T049)"
Task: "Create skills/documentation-generation/SKILL.md (T050)"
Task: "Create skills/production-readiness-review/SKILL.md (T051)"
```

### Reference-solution test sweep (T063)

```bash
# After every solution lands:
(cd exercises/part-02/solution/python && python -m task_manager add t && python -m task_manager list)
(cd exercises/part-02/solution/node && npm install && npx tsx src/index.ts add t && npx tsx src/index.ts list)
(cd exercises/part-04/solution/python && pip install -r requirements.txt && uvicorn app:app & sleep 2 && curl -fsS localhost:8000/notes)
(cd exercises/part-04/solution/node && npm install && npm run dev & sleep 2 && curl -fsS localhost:3000/notes)
(cd exercises/part-05/solution/python && pip install -r requirements.txt && pytest -q)
(cd exercises/part-05/solution/node && npm install && npm test)
(cd exercises/part-07/solution && python app.py & sleep 2 && curl -fsS localhost:8000)
(cd exercises/part-08/solution/after && pytest -q)
```

---

## Implementation Strategy

### MVP definition

**MVP = User Story 1 (instructor delivers) + the slide build pipeline**:
Phases 1, 2, 3, 4, 6–15 (deck tasks only — `T012`, `T014`, `T018`, `T020`, `T024`, `T029`, `T031`, `T035`, `T038`, `T040`), 19, and the structural validator portion of Phase 20 (`T060`, `T061`).

This produces a teachable workshop with all 10 decks, an instructor
guide, a working build, and validated structure — but no exercises,
no skills, no assessments. It satisfies SC-001, SC-002 (slides only),
SC-003, SC-008.

### Incremental delivery sequence

1. **Phase 1 → 2 → 3** in order (foundation, README, slide infra).
2. **Phases 6–15 deck tasks** (10 decks, all `[P]`) + **Phase 4** (instructor guide) + **Phase 19** (build) → run T059, T060, T061 → **MVP complete; instructor can teach a slides-only dry run.**
3. **Phases 6–15 exercise tasks** + **Phase 5** (student guide) → students can self-pace through labs.
4. **Reference-solution tasks** (T016, T017, T022, T023, T027, T028, T034, T037) — modules become independently verifiable; T063 passes.
5. **Phase 16** (skills) → US3 satisfied; T064 passes.
6. **Phase 17** (assessments) + **Phase 18** (certificate) → US2 fully satisfied; assessment grading workflow live.
7. **Phase 20 final tasks** (T062 quickstart, T065 terminology pass) → release sign-off.

### Parallel team strategy

- **Solo author (Luca)**: follow the incremental sequence above. ~70% of total effort sits in Phases 6–15 (decks + exercises + solutions); batch by module.
- **2-person team**: one author owns slides + guides + build; the other owns exercises + solutions + skills + assessments.
- **3-person team**: split slides / exercises+solutions / skills+assessments+certificate. Final review (Phase 20) is a single-owner integration step regardless of team size.

---

## Notes

- Every code-producing module's `solution/` directory **must** include a
  top-level `exercises/part-NN/README.md` notice "Do not open
  `solution/` before completing the lab" (FR-015a). This is a content
  requirement of the exercise README task, not a separate task.
- Module 9's "Personal Claude Skills / Command Library" deliverable
  reuses the `skills/` directory authored in Phase 16 — Phase 14's
  exercise (T039) has the student author **one new** skill following
  the same contract; Phase 16 tasks ship the bootcamp's 10 canonical
  skills (FR-016).
- "Code Review Rubric" (`exercises/part-05/code-review-rubric.md`,
  T026) is a **student-built artifact**, not the instructor grading
  rubric (`assessments/rubric.md`, T055). T065 explicitly verifies
  zero confusion across the repo (FR-011, FR-028).
- Task IDs T001–T065 cover all 28 functional requirements
  (FR-001–FR-028 plus FR-005a, FR-015a, FR-015b, FR-023a, FR-025a,
  FR-027a). FR coverage map is implicit in the [Story] tags and
  parenthetical FR citations on each task.
- Avoid: rewriting `slides/part-09-automation.md` or
  `slides/part-10-production.md` in place — T008 renames them first;
  authoring tasks (T038, T040) target the new names only.
- Commit after each completed task or each completed module (whichever
  is larger) per the constitution's authoring workflow.
