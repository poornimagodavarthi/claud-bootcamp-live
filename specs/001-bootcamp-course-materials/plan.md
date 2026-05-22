# Implementation Plan: Claude Code Bootcamp — Course Materials Repository

**Branch**: `001-bootcamp-course-materials` | **Date**: 2026-05-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-bootcamp-course-materials/spec.md`

## Summary

Author a complete, instructor-ready and student-ready course-materials
repository for the Packt Publishing endorsed *Claude Code Bootcamp — Build
10 Real-World Projects with Claude Code in One Day* (5 hours, 4h
instruction + 1h breaks/Q&A). Deliverables: GitHub-ready `README.md`,
`instructor-guide.md`, `student-guide.md`, `certificate-template.md`,
dual-license setup (CC BY-NC-SA 4.0 + MIT for `skills/`), 10 Marp slide
decks (each with the 14 mandatory sections), 10 hands-on exercises (each
with the 9 mandatory sections; reference solutions for code-producing
modules 2/4/5/7/8 with Python primary and Node.js secondary for 2/4/5),
10 Claude Code-native SKILL.md skill artifacts under `skills/`, five
assessment files (`knowledge-quiz.md`, `practical-task.md`,
`code-review-reflection.md`, `rubric.md`, `answer-key.md`), the slide
build script (`slides/deploy-pptx.sh`), and a final cross-artifact
validation checklist.

Technical approach: this is a **content repository**, not an application.
Implementation is text authoring (Markdown / Marp Markdown), one Bash
build script, and a structural validation script. No runtime backend, no
DB, no API. Toolchain is intentionally minimal (Marp CLI via npx,
optional Chromium for PPTX/PDF, Python 3.11+ and Node.js 20+ for the
project labs students complete). The plan organizes authoring into a
foundational pass (build/license/guides), a content pass (modules ×
slides + exercises), a skills pass, an assessment pass, and a final
validation pass aligned to the constitution's release-readiness rule.

## Technical Context

**Language/Version**: Markdown (CommonMark + Marp directives) for all
authored content; Bash 4+ for build and validation scripts. Project
labs that students *build during the bootcamp* use **Python 3.11+** as
the primary track and **Node.js 20+ (TypeScript 5+)** as a secondary
track for modules 2, 4, 5 (per spec FR-013).

**Primary Dependencies**:

- [`@marp-team/marp-cli`](https://github.com/marp-team/marp-cli) — slide
  build (PPTX default; PDF/HTML via flags). Auto-installed via `npx`.
- Chromium (downloaded by Marp on first run, or `CHROME_PATH` override)
  — required for PPTX/PDF export.
- Git — used by module 6 lab and by all submission/review workflows.
- Claude Code — external SaaS, used by instructor and students; not
  provisioned by this repo.

No application runtime, framework, or package manager is introduced for
the repository itself.

**Storage**: N/A. All artifacts are files on disk under version control.

**Testing**:

- **Structural validation**: a Bash script (`scripts/validate.sh`)
  enforces the constitution's structural rules: every slide deck has 14
  required sections; every exercise has 9 required sections; every
  skill has YAML frontmatter (`name`, `description`) and the 6 body
  attributes; the 10-project list is consistent across `README.md`,
  slides, exercises, and `assessments/rubric.md`; module instruction
  times sum to 240 minutes (±5).
- **Build validation**: `slides/deploy-pptx.sh` MUST succeed on a clean
  machine with only Node.js installed; PPTX outputs land in
  `slides/dist/`.
- **Reference-solution validation**: each code-producing module ships
  a `solution/` directory whose own tests/commands pass; module 5's
  reference solution explicitly demonstrates the test-suite pattern
  taught in that module.

**Target Platform**: macOS, Linux, and Windows-via-WSL2 (per spec
FR-027a). Authoring is platform-neutral Markdown; build script is
bash-only. Native PowerShell is out of scope.

**Project Type**: **Course-materials repository** (single-project
content library; no `src/` or `tests/` in the conventional sense).
Mapped to the plan template's "single project" option, with the
"source code" tree replaced by the content layout shown below.

**Performance Goals**:

- Slide build (`slides/deploy-pptx.sh`) completes for all 10 decks in
  under 3 minutes on a clean machine after Marp/Chromium first-run
  install.
- A new instructor goes from clone → first deck visible in under 30
  minutes (spec SC-001).
- Structural validation (`scripts/validate.sh`) completes in under 10
  seconds.

**Constraints**:

- 14 required sections per slide deck; 9 per exercise; 6 attributes per
  skill — all enforced by `scripts/validate.sh` (constitution Principle II).
- Module instruction times MUST sum to 240 minutes ±5 (constitution
  Authoring & Delivery Workflow → Schedule integrity).
- Dual license: top-level `LICENSE` (CC BY-NC-SA 4.0) + `skills/LICENSE`
  (MIT) (FR-005a).
- Marp Markdown only; no proprietary slide formats (constitution
  Principle III).
- No new external runtime dependencies beyond those listed above
  (constitution Principle X).

**Scale/Scope**:

- 10 modules × (1 slide deck + 1 exercise) = 20 module artifacts
- 5 code-producing modules × ≤ 2 reference-solution tracks = up to 8
  reference-solution directories (modules 2, 4, 5 ship Python + Node;
  modules 7, 8 ship Python only)
- 10 Claude Code skills (10 directories × `SKILL.md`)
- 5 assessment artifacts
- ~6 top-level Markdown files (README, two guides, certificate template,
  two LICENSE files)
- 1 Bash build script + 1 Bash validation script
- Estimated authored Markdown: 12,000–18,000 lines across the repo

## Constitution Check

*Gate: Must pass before Phase 0 research. Re-checked after Phase 1.*

The repository constitution is at `.specify/memory/constitution.md`
(version 1.0.0). Each principle is evaluated against this plan:

| # | Principle | Compliance | Notes |
|---|---|---|---|
| I | Practical, Project-Based Learning (NON-NEGOTIABLE) | ✅ Pass | Every module ships a concrete deliverable; reference solutions provided for code-producing modules; theory limited to what's needed for the lab. |
| II | Standardized Module Anatomy | ✅ Pass | `scripts/validate.sh` will enforce 14 slide sections + 9 exercise sections + 6 skill attributes. Contracts defined in Phase 1. |
| III | Marp-Flavored Markdown for All Slides | ✅ Pass | All decks authored as Marp Markdown under `slides/`; built via `slides/deploy-pptx.sh`; outputs in `slides/dist/` (gitignored). |
| IV | Beginner-to-Intermediate Accessibility | ✅ Pass | Python primary track (broad audience); Node.js secondary for 3 modules; pre-work absorbs setup risk; no programming-fundamentals teaching. |
| V | Build, Review, Teach in Under 30 Minutes | ✅ Pass | Self-bootstrapping `npx`-based build; instructor and student guides cover solo onboarding; SC-001 measurable. |
| VI | Concrete, Verifiable Deliverables | ✅ Pass | Every exercise's "Manual validation steps" deterministic; module 7 has canonical wireframe so output is rubric-scorable. |
| VII | No Motivational Filler | ✅ Pass | Plan, slides, exercises, skills follow promise/topic/lab/checkpoint structure. Authoring guidelines in instructor-guide enforce this. |
| VIII | Assessment and Certification Are First-Class | ✅ Pass | All 5 assessment artifacts in scope; 40/40/20 + 70% pass enforced; submission via Packt LMS zip; certificate template included. |
| IX | Cross-Artifact Consistency | ✅ Pass | `scripts/validate.sh` enforces consistent terminology + 10-project list across README, slides, exercises, skills, rubric. Module 5 deliverable renamed to "Code Review Rubric" to eliminate naming collision. |
| X | Minimal External Dependencies | ✅ Pass | Only Marp CLI, Chromium (Marp), Git, Claude Code. Python/Node introduced only for student-built project labs. No SaaS lock-in beyond Claude Code. |

**Result**: ✅ All gates pass. No constitutional violations require justification.
**Complexity Tracking**: Empty (no violations).

## Project Structure

### Documentation (this feature)

```text
specs/001-bootcamp-course-materials/
├── plan.md              # This file (/speckit.plan output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (structural contracts)
│   ├── slide-deck.contract.md
│   ├── exercise.contract.md
│   └── skill.contract.md
├── checklists/
│   └── requirements.md  # Existing (from /speckit.specify)
└── tasks.md             # Phase 2 output (NOT created here; from /speckit.tasks)
```

### Source Code (repository root)

This is a course-materials repository, not an application. The
"source" tree is the authored content tree:

```text
.
├── README.md                          # FR-001, FR-005, FR-005a
├── LICENSE                            # CC BY-NC-SA 4.0 (FR-005a)
├── .gitignore                         # excludes slides/dist/, .DS_Store
├── instructor-guide.md                # FR-024
├── student-guide.md                   # FR-025, FR-025a (pre-work)
├── certificate-template.md            # FR-023
├── .github/
│   └── copilot-instructions.md        # SPECKIT marker → plan.md
├── scripts/
│   └── validate.sh                    # Structural validation (constitution II, IX)
├── slides/
│   ├── README.md                      # deck index + render commands
│   ├── deploy-pptx.sh                 # FR-002, FR-003
│   ├── part-01-setup-mindset.md       # 14-section deck (FR-006)
│   ├── part-02-prompting.md
│   ├── part-03-claude-md.md
│   ├── part-04-best-of-n.md
│   ├── part-05-testing-debugging.md
│   ├── part-06-git-workflows.md
│   ├── part-07-multimodal.md
│   ├── part-08-refactor-docs.md
│   ├── part-09-skills-workflows.md    # renamed from part-09-automation.md
│   ├── part-10-production-readiness.md # renamed from part-10-production.md
│   └── dist/                          # gitignored build output (FR-004)
├── exercises/
│   ├── part-01/README.md              # 9-section exercise (FR-012)
│   ├── part-02/
│   │   ├── README.md
│   │   └── solution/                  # FR-015a
│   │       ├── python/
│   │       └── node/
│   ├── part-03/README.md
│   ├── part-04/
│   │   ├── README.md
│   │   └── solution/{python,node}/
│   ├── part-05/
│   │   ├── README.md
│   │   ├── code-review-rubric.md      # FR-011 (renamed deliverable)
│   │   └── solution/{python,node}/
│   ├── part-06/README.md
│   ├── part-07/
│   │   ├── README.md
│   │   ├── wireframe.png              # FR-015b
│   │   ├── wireframe-sketch.png       # FR-015b
│   │   └── solution/                  # Python only
│   ├── part-08/
│   │   ├── README.md
│   │   └── solution/                  # Python only
│   ├── part-09/README.md
│   └── part-10/README.md
├── skills/
│   ├── LICENSE                        # MIT (FR-005a)
│   ├── claude-md-template/SKILL.md    # FR-016, FR-017
│   ├── code-review/SKILL.md
│   ├── test-generation/SKILL.md
│   ├── best-of-n/SKILL.md
│   ├── refactor/SKILL.md
│   ├── release-notes/SKILL.md
│   ├── security-checklist/SKILL.md
│   ├── git-workflow/SKILL.md
│   ├── documentation-generation/SKILL.md
│   └── production-readiness-review/SKILL.md
└── assessments/
    ├── knowledge-quiz.md              # FR-019 (Markdown-only)
    ├── practical-task.md              # FR-020
    ├── code-review-reflection.md      # FR-021
    ├── rubric.md                      # FR-022 (instructor grading rubric)
    └── answer-key.md                  # FR-022
```

**Structure Decision**: Single content repository, no separate
`src/`/`tests/` split. The plan-template's "Option 1: Single project"
applies, with the source-code tree replaced by the content layout
shown above. The `scripts/` directory holds Bash automation
(validation, optional helpers) but is not "source code" in the
application sense. Build artifacts go to `slides/dist/` only and are
gitignored.

## Phase 0: Outline & Research

Phase 0 resolves any open NEEDS CLARIFICATION items and locks
authoring conventions before content production starts. The spec has
**zero** NEEDS CLARIFICATION markers (10 questions resolved across two
clarification rounds), so research focuses on **best-practice
decisions** that affect authoring throughput and final quality.

Research topics (consolidated in `research.md`):

1. **Marp authoring conventions** — pagination, theme, code-fence
   styling, image handling for Module 7 wireframe.
2. **Claude Code SKILL.md packaging** — frontmatter fields, naming
   convention, discovery rules (per the user's existing `/Users/.../assets/prompts/skills/` examples).
3. **Python project skeletons for labs** — module 2 CLI, module 4 API,
   module 5 testing target. Choose minimal, idiomatic stacks (no
   framework where stdlib suffices).
4. **Node.js (TypeScript) parallel skeletons** for modules 2, 4, 5 —
   minimum stack for parity with Python tracks.
5. **Cross-artifact validation strategy** — which checks belong in
   `scripts/validate.sh` vs which are review-time-only.
6. **Marp build performance & PPTX/Chromium fallbacks** — confirm
   `npx` self-bootstrap works on a fresh macOS/Linux/WSL2 machine.
7. **License templating** — exact CC BY-NC-SA 4.0 and MIT text sources
   and how the dual-license pointer is documented in `README.md`.
8. **Pre-work smoke-test design** — what minimal Claude Code prompt
   confirms a student is ready, capturable as a copy-paste output.

**Output**: [research.md](./research.md) with Decision / Rationale /
Alternatives entries for each topic.

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete.

### Data model

Domain entities (already enumerated in `spec.md` "Key Entities") are
formalized in [data-model.md](./data-model.md) with attribute
inventories, validation rules, and relationships. Entities: Module,
Project (Deliverable), Exercise, Slide Deck, Skill, Assessment Item,
Rubric, Certificate.

### Contracts

This repository's "interfaces" are the structural contracts that
governing tools (`scripts/validate.sh`) and human reviewers enforce.
They live under [contracts/](./contracts/):

- **`slide-deck.contract.md`** — the 14 required sections, ordering
  rules, frontmatter requirements, naming convention
  (`part-NN-<slug>.md`). Validators check section presence; reviewers
  check quality.
- **`exercise.contract.md`** — the 9 required sections, naming
  convention (`exercises/part-NN/README.md`), `solution/` requirement
  for code-producing modules (2/4/5/7/8), `solution/{python,node}/` for
  modules 2/4/5.
- **`skill.contract.md`** — Claude Code-native `SKILL.md` format with
  YAML frontmatter (`name`, `description`) and the 6 body attributes
  (purpose, when to use, body, inputs, outputs, worked example).

These contracts replace traditional API contracts for this content
repository.

### Quickstart

[quickstart.md](./quickstart.md) — the "30-minute path to teaching
module 1" walk-through targeting SC-001. Used both by new instructors
and as smoke-test verification after every release.

### Agent context update

`.github/copilot-instructions.md` is updated so the SPECKIT marker
points to this plan file. Done as the final Phase 1 step.

**Output**: `data-model.md`, `contracts/slide-deck.contract.md`,
`contracts/exercise.contract.md`, `contracts/skill.contract.md`,
`quickstart.md`, updated `copilot-instructions.md`.

## Complexity Tracking

> Filled only if Constitution Check has violations that must be justified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| _(none)_  | _(n/a)_    | _(n/a)_                              |

No constitutional violations. All 10 principles satisfied without
justification entries.
