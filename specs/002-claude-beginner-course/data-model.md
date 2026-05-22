# Data Model — Claude Code Beginner Course

**Feature**: `002-claude-beginner-course`  
**Phase**: 1 (Design & Contracts)  
**Date**: 21 May 2026

This is a course-materials feature, not an application. There is no database, no API, no runtime state. The "data model" below is the set of authoring entities the validator and grader treat as first-class, along with their fields, relationships, and validation rules. Each entity maps to one or more files on disk under predictable paths.

---

## Entities

### 1. Module

A self-contained 20–30-minute lesson.

| Field | Type | Source | Notes |
|---|---|---|---|
| `number` | int (01–08) | derived from filename `part-NN-*.md` | 00 = setup prework; 01–08 = numbered modules |
| `slug` | string (kebab-case) | derived from filename | e.g. `meet-claude-code`, `first-conversation` |
| `title` | string | deck H1 + exercise H1 (must match) | enforced by validator |
| `duration_min` | int | `<!-- duration: NN min -->` marker in deck | one of {20, 25, 30}; canonical per FR-030 |
| `deck` | one `Deck` | `slides/beginner/part-NN-<slug>.md` | one-to-one |
| `exercise` | one `Exercise` | `exercises/beginner/part-NN/` | one-to-one |
| `quiz_items` | list of 2 `QuizQuestion` | `assessments/beginner/quiz.md` filtered by `<!-- module: NN -->` | exactly 2 per module |
| `glossary_terms` | list of `GlossaryEntry` | extracted from deck Glossary card slide | each MUST appear byte-identical in `GLOSSARY.md` |

**Validation rules**:
- `number` MUST be unique across `slides/beginner/`.
- `duration_min` MUST match the canonical budget for its `number` (FR-030).
- `deck.duration_marker` MUST equal `duration_min`.
- The 8 numbered modules' durations MUST sum to 210 minutes; the 200–240 envelope (SC-008) tolerates author additions but the validator's hard upper bound stays at 240.

**State transitions**: none (static authoring entity).

---

### 2. Deck

A single Marp slide file.

| Field | Type | Source | Notes |
|---|---|---|---|
| `path` | string | `slides/beginner/part-NN-<slug>.md` | one per Module |
| `frontmatter` | YAML block | top of file | MUST include `marp: true`, `theme: default`, `paginate: true`, `size: 16:9`, `title`, `description` |
| `duration_marker` | string | `<!-- duration: NN min -->` immediately after frontmatter | one per deck |
| `sections` | ordered list of 10 H2 headings | extracted via grep | MUST be exactly the 10 headings of FR-011 in order (see `contracts/deck-10-section.md`) |
| `content_slide_count` | int | count of `---` slide breaks between title and Glossary card | MUST be ≤ 12 (FR-013) |
| `prompts_shown` | list of fenced code blocks tagged as prompts | scanned at validator time | each MUST be copy-pasteable (no `...` truncation) — FR-014 |
| `glossary_card` | one slide | the H2 = `Glossary card` slide | MUST contain `**term**: definition` pairs, one per line |

**Validation rules**: see `contracts/deck-10-section.md`.

---

### 3. Exercise

A folder under `exercises/beginner/part-NN/`.

| Field | Type | Source | Notes |
|---|---|---|---|
| `path` | string | `exercises/beginner/part-NN/` | one per Module |
| `readme` | file | `exercises/beginner/part-NN/README.md` | required |
| `sections` | ordered list of 7 H2 headings | extracted from README | MUST be exactly the 7 headings of FR-021 in order (see `contracts/exercise-7-section.md`) |
| `starter_dir` | folder | `starter/` | MUST exist and contain ≥ 1 file (FR-022) |
| `solution_dir` | folder | `solution/` | MUST exist and contain ≥ 1 non-empty file (FR-023). EXCEPTION: Module 00 setup has no `solution/` |
| `prompt_to_paste` | fenced code block | section #4 of README | MUST be verbatim copy-pasteable (FR-014) |
| `expected_artifact` | string | derived from "How to know it worked" section | a single named file, screenshot, or transcript (FR-025) |
| `freeplan_friendly` | bool | inferred from README; defaults true | FR-024 |

**Validation rules**: see `contracts/exercise-7-section.md`.

---

### 4. GlossaryEntry

A single term with a one-line plain-language definition.

| Field | Type | Source | Notes |
|---|---|---|---|
| `term` | string | bolded text in `**term**: definition` line | unique across `GLOSSARY.md` |
| `definition` | string | text after `: ` on the same line | exactly one line, no embedded newlines |
| `source_module` | int | module that introduces the term | derived from deck Glossary card slide |

**Validation rules**:
- Every term that appears in any beginner deck's Glossary card MUST appear in `GLOSSARY.md` with a byte-identical definition (SC-006).
- Conversely, every entry in `GLOSSARY.md` MUST appear in at least one beginner deck's Glossary card (orphan-glossary check).
- Term names MUST be unique across `GLOSSARY.md`.

**State transitions**: none.

---

### 5. QuizQuestion

One of 16 multiple-choice items.

| Field | Type | Source | Notes |
|---|---|---|---|
| `number` | int 1–16 | numbered list in `assessments/beginner/quiz.md` | unique |
| `module_tag` | int 1–8 | `<!-- module: NN -->` HTML comment immediately above the question | exactly 2 questions per module value |
| `prompt` | string | the question text | derivable from slides or exercise of the tagged module (FR-041) |
| `options` | list of exactly 4 | sub-bullets `A.`/`B.`/`C.`/`D.` | one is correct |
| `correct_letter` | char in {A,B,C,D} | from `answer-key.md` | exactly one per question |
| `rationale` | string | one sentence in `answer-key.md` | required |
| `source` | string | `module-NN slide-K` or `module-NN exercise-step-K` | required, in `answer-key.md` |

**Validation rules**:
- Exactly 16 questions in `quiz.md`.
- Exactly 2 questions tagged per module (1..8).
- Each question has exactly 4 options.
- Every question has a matching entry in `answer-key.md` (by number).
- Answer-key letter MUST be one of A/B/C/D.

---

### 6. Certificate

A renderable template.

| Field | Type | Source | Notes |
|---|---|---|---|
| `path` | string | `beginner-certificate-template.md` | exactly one |
| `template_vars` | list of placeholders | scanned via grep `\{\{[A-Z_]+\}\}` | MUST include `{{STUDENT_NAME}}`, `{{COMPLETION_DATE}}`, `{{INSTRUCTOR_NAME}}`, `{{WORKSHOP_TITLE}}`, `{{VERIFICATION_TOKEN}}` |
| `render_command` | string | documented in `beginner-student-guide.md` | a single `sed` or `pandoc` line |

**Validation rules**:
- All 5 template vars MUST be present.
- `{{VERIFICATION_TOKEN}}` MUST be documented as "paste the token from `scripts/check-beginner-capstone.sh`" in `beginner-student-guide.md`.

---

### 7. CapstoneSubmission (runtime, not a stored artifact)

The learner's `notes.py` file as graded by `scripts/check-beginner-capstone.sh`.

| Field | Type | Source | Notes |
|---|---|---|---|
| `path` | string (CLI arg) | `$1` to grader | required |
| `loc` | int | `wc -l` of the file | SHOULD be ≤ 100 (not strictly enforced by grader; lint advisory only) |
| `subcommands` | implicit | observed by grader running `add`/`list`/`delete` | MUST behave per `contracts/capstone-cli.md` |
| `persistence` | file | `notes.json` in cwd, created by `add` | grader runs in `mktemp -d`; learner-side notes are in their cwd |
| `verification_token` | 8-char hex | computed by grader from successful run | output as `PASS <token>` on stdout |

**State transitions** (per grader run):
```text
no-notes-json → add "hello" → notes.json with 1 entry → list (contains "hello") → delete 1 → notes.json with 0 entries → list (does NOT contain "hello") → PASS
```
Any deviation → `FAIL: <one-line reason>`, exit 1.

---

### 8. LearnerPersona (informational; not enforced)

| Field | Value |
|---|---|
| Prior AI tool experience | None assumed |
| Platform | macOS, Linux, or Windows + WSL2 |
| Claude plan | Free |
| Reading level | US high-school senior |
| Goal | Self-paced certificate in ≤ 5 hours (SC-001) |

Used by reviewers to keep tone consistent. Not validated by scripts.

---

## Relationships

```text
Module 1..1 ── Deck
Module 1..1 ── Exercise
Module 1..2 ── QuizQuestion
Module 0..N ── GlossaryEntry     (the entries this module introduces)

Deck.glossary_card.terms  ⇿  GlossaryEntry.term     (character-identical)
Exercise.prompt_to_paste  ⇿  Deck.prompts_shown     (recommended overlap; not enforced)

QuizQuestion.number       ⇿  AnswerKey.number       (one-to-one)
Certificate.template_vars ⊇  {STUDENT_NAME, COMPLETION_DATE, INSTRUCTOR_NAME, WORKSHOP_TITLE, VERIFICATION_TOKEN}
CapstoneSubmission        →  Certificate.{{VERIFICATION_TOKEN}}     (one token per successful run)
```

---

## File layout summary

| Entity | Path |
|---|---|
| Module 00 setup | `exercises/beginner/module-00-setup/` |
| Module 01..08 Deck | `slides/beginner/part-NN-<slug>.md` |
| Module 01..08 Exercise | `exercises/beginner/part-NN/{README.md,starter/,solution/}` |
| Glossary | `GLOSSARY.md` |
| Quiz | `assessments/beginner/quiz.md` |
| Answer key | `assessments/beginner/answer-key.md` |
| Student guide | `beginner-student-guide.md` |
| Instructor guide | `beginner-instructor-guide.md` |
| Certificate | `beginner-certificate-template.md` |
| Capstone grader | `scripts/check-beginner-capstone.sh` |
| Validator (extended) | `scripts/validate.sh` |
| Build script (extended) | `slides/deploy-pptx.sh` |

All entity field validations are mechanically checked by the extended `scripts/validate.sh`. The capstone CLI contract is mechanically checked by `scripts/check-beginner-capstone.sh`. Anything not on this list is reviewer-enforced at PR time.
