# Phase 1 Data Model: Claude Code Bootcamp — Course Materials Repository

**Branch**: `001-bootcamp-course-materials`
**Date**: 2026-05-21

This is a content repository, not an application; "data model" here
formalizes the **content entities** the repository produces and the
relationships and validation rules among them. These entities are the
target of `scripts/validate.sh` and of human review.

---

## Entity inventory

### 1. Module

A teaching unit. There are exactly **10** modules, numbered 1–10.

| Attribute | Type | Constraints |
|---|---|---|
| `number` | int | 1–10, unique |
| `title` | string | matches the FR-011 canonical name for that number |
| `time_minutes` | int | one of {20, 25, 30, 35} (matches spec schedule) |
| `promise` | string | testable learner capability (verb-led; no motivational language — Principle VII) |
| `topics` | string[] | min 2 items |
| `project_name` | string | references a `Project` entity (FR-011 canonical names) |
| `category` | enum | `code-producing` (modules 2, 4, 5, 7, 8) or `conceptual` (modules 1, 3, 6, 9, 10) |
| `tracks` | string[] | `code-producing` modules only: subset of `{python, node}`. Modules 2, 4, 5 = `[python, node]`; modules 7, 8 = `[python]`. |

**Validation rules**:

- `sum(time_minutes for all modules) == 240 ± 5` (constitution Schedule
  integrity).
- `(number, title)` pairs match the FR-011 canonical list exactly.

**Relationships**:

- 1 Module ↔ 1 Slide Deck (`slides/part-NN-<slug>.md`)
- 1 Module ↔ 1 Exercise (`exercises/part-NN/`)
- 1 Module ↔ 1 Project (deliverable)
- 1 Module → 0..N Skills referenced (e.g., module 9 enumerates the
  whole skills library)

### 2. Project (Deliverable)

A learner-produced artifact tied to a Module.

| Attribute | Type | Constraints |
|---|---|---|
| `name` | string | from FR-011 canonical list (e.g., "CLI Task Manager") |
| `module_number` | int | 1–10, unique |
| `expected_outputs` | string[] | filenames or observable artifacts |
| `validation_steps` | string[] | deterministic steps a student can self-run (Principle VI) |

**Special cases**:

- Module 5 deliverable is **"Tests + Bug Fixes + Code Review Rubric"**
  (renamed in spec round 2 to eliminate naming collision with
  `assessments/rubric.md`). The Code Review Rubric component lives at
  `exercises/part-05/code-review-rubric.md`.
- Module 9 deliverable IS the `skills/` directory itself (Assumption
  in spec).

### 3. Exercise

The lab instructions for a Module. Exactly one per module.

| Attribute | Type | Constraints |
|---|---|---|
| `path` | string | `exercises/part-NN/README.md` |
| `goal` | string | one paragraph |
| `scenario` | string | concrete, story-driven |
| `starter_instructions` | string[] | numbered steps |
| `claude_prompt` | string | complete, copy-paste-ready big prompt (FR-013) |
| `manual_validation_steps` | string[] | deterministic |
| `expected_deliverable` | string | matches Project's `expected_outputs` |
| `definition_of_done` | string[] | pass/fail checklist (Principle VI) |
| `stretch_challenge` | string | optional extension |
| `troubleshooting` | (issue, fix)[] | min 3 entries |
| `solution_dir` | path \| null | required for code-producing modules; `null` for conceptual |

**Validation rules**:

- Exactly **9** required H2 sections present (constitution Principle II).
- For modules 2, 4, 5: `solution_dir` contains both `python/` and
  `node/`.
- For modules 7, 8: `solution_dir` contains exactly `python/` content
  (no `node/`).
- For modules 1, 3, 6, 9, 10: `solution_dir == null` (no `solution/`
  directory required).
- For module 7: `exercises/part-07/wireframe.png` AND
  `exercises/part-07/wireframe-sketch.png` (or `.svg`) exist (FR-015b).

### 4. Slide Deck

A Marp Markdown file under `slides/`. Exactly one per module.

| Attribute | Type | Constraints |
|---|---|---|
| `path` | string | `slides/part-NN-<slug>.md` (slugs fixed per file plan) |
| `frontmatter` | yaml | `marp: true`, `theme: default`, `paginate: true`, `size: 16:9`, `title`, `description` |
| `sections` | string[] | exactly 14 in fixed order (see contract) |
| `duration_minutes` | int | recorded as an HTML comment `<!-- duration: NN min -->` near the top, must equal Module.time_minutes |

**Validation rules**:

- 14 required section headings present (constitution Principle II).
- Module numbering and duration match the Module entity.

### 5. Skill

A reusable Claude Code-native artifact under `skills/<kebab-name>/`.

| Attribute | Type | Constraints |
|---|---|---|
| `name` (frontmatter) | string | kebab-case, matches directory name |
| `description` (frontmatter) | string | ≤ 120 chars, action-oriented |
| `purpose` (body) | string | section H2 |
| `when_to_use` (body) | string | section H2 |
| `prompt_body` (body) | string | section H2; the actual reusable prompt |
| `expected_inputs` (body) | string | section H2 |
| `expected_outputs` (body) | string | section H2 |
| `worked_example` (body) | string | section H2; ≥ 1 reproducible example |

**Required skill set (10 entries)**:

| # | `name` | Purpose |
|---|---|---|
| 1 | `claude-md-template` | Generate a high-quality CLAUDE.md for a project |
| 2 | `code-review` | Review a diff against a rubric, surface unsafe output |
| 3 | `test-generation` | Generate tests for a target file/function |
| 4 | `best-of-n` | Run a Best-of-N solution-comparison workflow |
| 5 | `refactor` | Refactor with constraints, preserving behavior |
| 6 | `release-notes` | Produce release notes from a commit range or PR |
| 7 | `security-checklist` | Run a security review on a project or diff |
| 8 | `git-workflow` | Branch/commit/diff/PR-style review on AI-generated code |
| 9 | `documentation-generation` | Generate onboarding/handoff docs |
| 10 | `production-readiness-review` | Run the production-readiness review |

**Validation rules**:

- 10 directories exist with the names above.
- Each contains `SKILL.md` with valid frontmatter and the 6 body
  sections.
- No skill references bootcamp-specific paths (FR-018; project-agnostic).

### 6. Assessment Item

An item inside an assessment file.

| Attribute | Type | Constraints |
|---|---|---|
| `kind` | enum | `quiz_question` (in `knowledge-quiz.md`), `practical_step` (in `practical-task.md`), `reflection_prompt` (in `code-review-reflection.md`) |
| `weight_pct` | int | per-item weight; the totals per file map to the 40/40/20 grand totals |
| `criteria` | string[] | for quiz: 1 correct answer + N distractors; for practical: numbered steps; for reflection: prompt + scoring criteria |

**Quantity constraints**:

- `knowledge-quiz.md`: ≥ 20 quiz items, totalling 40% of the grade.
- `practical-task.md`: ≥ 1 graded mini-build, totalling 40% of the
  grade. May contain multiple sub-tasks summing to 40.
- `code-review-reflection.md`: ≥ 1 reflection prompt, totalling 20%.

### 7. Rubric

The instructor-grading rubric, exactly one entity at
`assessments/rubric.md`.

| Attribute | Type | Constraints |
|---|---|---|
| `components` | object | exactly 3 keys: `knowledge_quiz` (weight 40), `practical_task` (weight 40), `code_review_reflection` (weight 20) |
| `pass_threshold_pct` | int | `70` |
| `per_component_criteria` | string[][] | each component has explicit scoring criteria |

**Note**: The student-built artifact in module 5 is the **"Code Review
Rubric"** (`exercises/part-05/code-review-rubric.md`) and is
**distinct** from this entity. Cross-references in slides/exercises
use the term "Code Review Rubric" to disambiguate (FR-011).

### 8. Certificate

A template at `certificate-template.md`.

| Attribute | Type | Constraints |
|---|---|---|
| `placeholders` | string[] | at minimum: `{{student_name}}`, `{{date}}`, `{{instructor_name}}`, `{{workshop_title}}` |
| `endorsement_text` | string | states "Endorsed by Packt Publishing" |
| `instructor_name_default` | string | `Luca Berton` (placeholder still allowed) |
| `pass_requirement_text` | string | states 70% threshold |

---

## Relationships diagram

```text
Module (10) ──┬─ 1 Slide Deck
              ├─ 1 Exercise ──── 0..1 solution/ ──┬─ python/ (modules 2,4,5,7,8 partial)
              │                                    └─ node/   (modules 2,4,5)
              ├─ 1 Project (deliverable)
              └─ 0..N references → Skill

Skill (10, independent of any Module structurally)

Assessment Item (N) ──── 1 of 3 files ──── 1 Rubric ──── 1 Certificate
                                                          (issued on ≥ 70%)
```

---

## State transitions

The repository itself does not have runtime state. The **Workshop
delivery flow** has these states (used in `instructor-guide.md`):

```
[Pre-workshop]
   ├─ student completes pre-work (FR-025a)
   └─ instructor verifies materials (release-readiness checklist)
            │
            ▼
[Live workshop in session]
   ├─ Module 1 → … → Module 10 (linear; no skipping)
            │
            ▼
[Post-workshop assessment]
   ├─ student submits zip to Packt LMS (FR-023a)
   ├─ instructor grades against Rubric
   └─ on score ≥ 70 → Certificate issued
```

---

## Validation rules reference

| Rule | Source | Enforcement |
|---|---|---|
| 14 slide sections | Principle II, FR-006 | `scripts/validate.sh` |
| 9 exercise sections | Principle II, FR-012 | `scripts/validate.sh` |
| 6 skill body sections + 2 frontmatter fields | Principle II, FR-016, FR-017 | `scripts/validate.sh` |
| Module times sum to 240 ± 5 | Schedule integrity | `scripts/validate.sh` |
| Solution dirs for code-producing modules | FR-015a | `scripts/validate.sh` |
| Module 7 wireframe assets | FR-015b | `scripts/validate.sh` |
| Cross-artifact name consistency | Principle IX, FR-028, SC-007 | `scripts/validate.sh` |
| Dual-license files present | FR-005a | `scripts/validate.sh` |
| `slides/dist/` gitignored | FR-004 | `scripts/validate.sh` |
| Tone / no filler | Principle VII | Human review at PR time |
| Prompt quality | FR-008, FR-013 | Human review |
| Instructor-notes sufficiency | Quality Standards | Human review |
