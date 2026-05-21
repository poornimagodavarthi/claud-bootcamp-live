# Implementation Plan: Claude Code Beginner Course (Claude Code 101)

**Branch**: `002-claude-beginner-course` | **Date**: 21 May 2026 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-claude-beginner-course/spec.md`

## Summary

Author a beginner-friendly companion course to the intermediate bootcamp under `001-bootcamp-course-materials`. The deliverable is 8 modules (01–08) plus Module 00 prework, each shipping a Marp deck (10-section simplified contract), a runnable exercise (7-section simplified contract), 2 quiz items, glossary entries, and — for Module 08 only — a `notes.py` capstone with an automated smoke check. Beginner artifacts interleave as siblings next to the intermediate course (`slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, plus top-level `beginner-*.md` and `GLOSSARY.md`), sharing one `slides/deploy-pptx.sh` build pipeline and one `scripts/validate.sh` validator. Technical approach: extend the existing Bash validator to enforce the new 10/7-section contracts and Glossary character-identity check on `slides/beginner/**` and `exercises/beginner/**`; extend `deploy-pptx.sh` to discover decks via `slides/**/part-*.md`; ship a tiny POSIX-bash capstone grader `scripts/check-beginner-capstone.sh`; author the content under the new sibling tree. No new runtime dependencies.

## Technical Context

**Language/Version**: Markdown (Marp-flavored) for slides; Bash 3.2+ for scripts (macOS compatibility); Python 3.11+ for the Module 08 capstone artifact only (a single ≤ 100 LOC `notes.py`).

**Primary Dependencies**: Marp CLI (`@marp-team/marp-cli`, invoked via `npx --yes` to bypass any broken global install); Chromium (for PPTX/PDF export — invoked by Marp); standard POSIX utilities (`bash`, `sed`, `awk`, `grep`, `perl`, `find`, `shasum`). No new runtime dependencies beyond what the intermediate course already requires.

**Storage**: Plain files on disk. The Module 08 capstone persists notes to `notes.json` in the learner's working directory (no database). Build artifacts land in `slides/dist/` (already gitignored).

**Testing**: `scripts/validate.sh` is the structural test harness (extended for this feature). `scripts/check-beginner-capstone.sh` is the capstone smoke test (new in this feature). There is no separate unit-test framework — content correctness is enforced by the validator's regex and section checks; capstone correctness is enforced by the smoke checker exercising the three CLI subcommands against expected stdout.

**Target Platform**: macOS, Linux, or Windows-with-WSL2 (same as the intermediate course). Bash must run on macOS 3.2 (no associative arrays, no `mapfile`). Marp PPTX export requires a Chromium binary available to Puppeteer (`CHROME_PATH` env var documented in `slides/deploy-pptx.sh`).

**Project Type**: Course materials (single repository, no application code). The feature ships authoring assets (Markdown), build scripts (Bash), and one tiny reference Python program (the capstone solution).

**Performance Goals**: `scripts/validate.sh` MUST exit in ≤ 10 seconds on a clean checkout (it is run on every PR). `slides/deploy-pptx.sh` MUST build all 10 intermediate decks + all 8 beginner decks in ≤ 5 minutes on a developer laptop with a warm Marp/Chromium cache.

**Constraints**: Bash 3.2 compatibility (no associative arrays — use parallel arrays indexed by integer). No third-party Python packages for the capstone (stdlib only). Beginner deck minute-budgets sum to 210 minutes for modules 01–08 (within the 200–240 window of FR-002); this is independent of the intermediate course's 240-minute schedule integrity rule. Reading level: US high-school senior or below. The forbidden-tokens regex MUST apply identically to both courses' authoring files.

**Scale/Scope**: 1 Module 00 prework + 8 modules × {1 deck + 1 exercise (with `starter/` and `solution/`) + 2 quiz items + glossary entries} + 1 top-level student guide + 1 top-level instructor guide + 1 certificate template + 1 GLOSSARY.md + 1 quiz file + 1 answer key + 1 new bash script + extensions to 2 existing scripts. Total estimated authoring footprint: ~50 new files, ~3,000 lines of Markdown, ~200 lines of Bash, ≤ 100 lines of Python.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against `.specify/memory/constitution.md` v1.0.0:

| Principle | Status | Evidence |
|---|---|---|
| I. Practical, Project-Based Learning (NON-NEGOTIABLE) | PASS | Every module ships an exercise with a single concrete artifact (FR-020, FR-025); Module 08 ships a capstone `notes.py` (FR-033). |
| II. Standardized Module Anatomy | **DEVIATION — JUSTIFIED** | Beginner course intentionally uses a **simplified 10-section deck contract** (FR-011) and **simplified 7-section exercise contract** (FR-021), NOT the intermediate course's 14/9-section contracts. See Complexity Tracking below. |
| III. Marp-Flavored Markdown | PASS | FR-010 mandates Marp frontmatter and `slides/beginner/part-NN-<slug>.md` layout; FR-050 reuses `slides/deploy-pptx.sh`. |
| IV. Beginner-to-Intermediate Accessibility | PASS | This entire feature exists to drop the assumption floor below "Claude Code basics"; FR-004 explicitly caps reading level at US high-school senior and forbids unprefaced jargon. |
| V. Build, Review, Teach in Under 30 Minutes | PASS | No new build dependency (FR-050); install path is `npm i -g @anthropic-ai/claude-code` (Clarifications Q2). Onboarding is a single `beginner-student-guide.md` (FR-052). |
| VI. Concrete, Verifiable Deliverables | PASS | FR-025 forbids "understanding it" as deliverable; FR-044/FR-045 define pass/fail via `scripts/check-beginner-capstone.sh` and a numeric quiz threshold. |
| VII. No Motivational Filler | PASS | FR-055 inherits the same forbidden-tokens regex enforced by `scripts/validate.sh`. |
| VIII. Assessment and Certification Are First-Class | PASS | FR-040..FR-046 mandate quiz, answer key, certificate template, and verification-token grader. |
| IX. Cross-Artifact Consistency | PASS | FR-015 + SC-006 require character-identical glossary entries; FR-051 extends the existing validator; FR-054 updates the top-level README. |
| X. Minimal External Dependencies | PASS | No new runtime dependencies (FR-050 reuses Marp CLI; capstone is stdlib Python; grader is POSIX bash). |

**Authoring & Delivery Workflow gates**:

- *Schedule integrity (240 ± 5 min)*: Applies to the intermediate course (10 modules × ~24 min). The beginner course is a **separate, sibling course** with its own 210-minute envelope (FR-002, SC-008). The 240-minute rule is therefore not violated; the beginner schedule integrity rule is "200 ≤ sum ≤ 240" and the validator enforces it.
- *Release readiness (10/10/10 + assessments)*: The beginner course adds its own parallel release-readiness slice: 8 beginner decks build, 8 beginner exercises have 7 required sections, 0 required skills (per Clarifications Q5; skills are opportunistic), assessments reference current deliverable names, terminology is consistent via `GLOSSARY.md`.

**Gate result**: PASS with one justified deviation (Principle II — recorded in Complexity Tracking).

## Project Structure

### Documentation (this feature)

```text
specs/002-claude-beginner-course/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command output)
├── quickstart.md        # Phase 1 output (/speckit.plan command output)
├── contracts/           # Phase 1 output (/speckit.plan command output)
│   ├── deck-10-section.md
│   ├── exercise-7-section.md
│   ├── glossary-identity.md
│   ├── capstone-cli.md
│   ├── capstone-grader.md
│   └── validator-extensions.md
├── checklists/
│   └── requirements.md  # Already authored (16/16 passing)
├── spec.md              # Feature spec
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
```

### Source Code (repository root)

The beginner course interleaves as a sibling layout next to the intermediate course (locked by Clarifications 2026-05-21 Q1). New paths created by this feature are marked **NEW**; paths extended in place are marked **EXTEND**.

```text
Training-Claude-Code-Extended/
├── README.md                                # EXTEND (FR-054 — side-by-side positioning + Mermaid path diagram)
├── GLOSSARY.md                              # NEW   (FR-015 — single source of truth for beginner glossary entries)
├── beginner-student-guide.md                # NEW   (FR-052 — ≤ 200 lines)
├── beginner-instructor-guide.md             # NEW   (FR-053 — ≤ 250 lines)
├── beginner-certificate-template.md         # NEW   (FR-043, FR-046 — shares template vars with intermediate certificate; adds {{VERIFICATION_TOKEN}})
│
├── slides/
│   ├── deploy-pptx.sh                       # EXTEND (FR-050 — discover decks via slides/**/part-*.md)
│   ├── part-NN-*.md                         # (intermediate course — unchanged)
│   └── beginner/                            # NEW
│       ├── README.md                        # NEW (table of 8 beginner decks)
│       ├── part-01-meet-claude-code.md      # NEW (20 min, ≤ 8 content slides)
│       ├── part-02-first-conversation.md    # NEW (25 min, ≤ 10 content slides)
│       ├── part-03-asking-for-what-you-want.md  # NEW (30 min, ≤ 12 content slides)
│       ├── part-04-reading-code-together.md # NEW (25 min, ≤ 10 content slides)
│       ├── part-05-editing-one-file-safely.md   # NEW (30 min, ≤ 12 content slides)
│       ├── part-06-claude-md-cheat-sheet.md # NEW (25 min, ≤ 10 content slides)
│       ├── part-07-safer-and-smarter.md     # NEW (25 min, ≤ 10 content slides)
│       └── part-08-putting-it-together.md   # NEW (30 min, ≤ 12 content slides; capstone deck)
│
├── exercises/
│   ├── part-NN/                             # (intermediate course — unchanged)
│   └── beginner/                            # NEW
│       ├── module-00-setup/
│       │   ├── README.md                    # NEW (install Claude Code CLI; produce first-prompt.txt)
│       │   └── starter/.keep
│       ├── part-01/
│       │   ├── README.md                    # NEW (7-section contract)
│       │   ├── starter/                     # NEW (scaffolding — never step-1 file creation)
│       │   └── solution/                    # NEW (working reference)
│       ├── part-02/ ... part-07/            # NEW (same shape as part-01)
│       └── part-08/
│           ├── README.md                    # NEW (capstone exercise; ≤ 15 min budget)
│           ├── starter/notes.py             # NEW (minimal stub)
│           └── solution/notes.py            # NEW (working ≤ 100 LOC reference)
│
├── assessments/
│   ├── *.md                                 # (intermediate course — unchanged)
│   └── beginner/                            # NEW
│       ├── quiz.md                          # NEW (FR-040 — 16 MCQs, 2 per module)
│       └── answer-key.md                    # NEW (FR-042 — letter + source slide + rationale)
│
├── skills/
│   ├── <intermediate-skills>/               # (intermediate course — unchanged)
│   └── beginner/                            # OPTIONAL (created only if Q5/FR-060 produces a skill)
│
└── scripts/
    ├── validate.sh                          # EXTEND (FR-051 — beginner 10/7-section, glossary identity, beginner duration sum 200–240)
    └── check-beginner-capstone.sh           # NEW   (FR-045 — bash 3.2-compatible smoke check; PASS + verification token)
```

**Structure Decision**: Single-repository sibling layout (locked by Clarifications Q1). The beginner course shares the intermediate course's two pieces of build infrastructure (`slides/deploy-pptx.sh` and `scripts/validate.sh`) and adds exactly one new script (`scripts/check-beginner-capstone.sh`). All beginner-specific content lives under predictable `beginner/` subfolders or top-level `beginner-*.md` siblings — no nesting inside `001-bootcamp-course-materials`, no rename of intermediate paths. This keeps both courses independently buildable and avoids any change to feature 001's release surface.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Constitution Principle II (Standardized Module Anatomy) — beginner course uses a **10-section deck contract + 7-section exercise contract** instead of the constitution's 14-section deck + 9-section exercise structure. | The beginner course's whole positioning (FR-004, FR-011, FR-021, User Story 1) is "easier and more explanatory than the intermediate course." Asking absolute beginners to navigate 14 deck sections per module — including instructor-only sections like `Instructor notes` and intermediate-only artifacts like `Step-by-step Lab` and `Definition of Done` — defeats the course's reason to exist. The simpler contract is itself the user-visible promise (e.g. "Try it yourself" inside the slide, "Lesson reflection" instead of a graded checkpoint). | Reusing the intermediate course's 14/9-section contracts was the default option and was rejected because (a) it forces beginner authors to fabricate per-module instructor notes and stretch challenges that have no audience in self-paced beginner delivery, and (b) it makes the validator unable to flag "this beginner deck is too dense" — the 10-section contract caps content slides at 12 (FR-013) so density is enforceable. Splitting the difference (e.g. 12/8 sections) was rejected because it offers no clear pedagogical anchor. The 10/7 split mirrors the Anthropic Academy "Claude 101" reference shape that the spec is patterned after. Validator extensions (FR-051) make the beginner contract a first-class, machine-checkable rule, so the deviation does not weaken Principle II for the intermediate course — both contracts are now formally enforced. |
