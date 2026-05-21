# Feature Specification: Claude Code Beginner Course (Claude Code 101)

**Feature Branch**: `002-claude-beginner-course`

**Created**: 21 May 2026

**Status**: Draft

**Input**: User description: "I want a course beginner-friendly that leverages Anthropic Claude Code. Slides must be more easy and explanatory. Exercises too." Reference inspiration: the Anthropic Academy "Claude 101" curriculum (pasted by the user) — its pedagogical shape (very short lessons, plain-language explanations, lesson reflections, "Try it out when..." callouts, learning objectives per lesson) is the target tone and density. Scope shift: where Claude 101 is about `claude.ai`, this course is about **Claude Code** as a beginner-friendly companion to the existing intermediate bootcamp under `specs/001-bootcamp-course-materials`.

---

## Clarifications

### Session 2026-05-21

- Q: Folder layout for beginner artifacts (sibling vs nested vs renamed)? → A: Sibling layout — beginner artifacts interleave next to the intermediate course (`slides/beginner/`, `exercises/beginner/`, `assessments/beginner/` + top-level `beginner-*.md` siblings + `GLOSSARY.md`), sharing one `slides/deploy-pptx.sh` and one `scripts/validate.sh` with the intermediate course.
- Q: Claude Code distribution channel and minimum version? → A: CLI only, latest — `@anthropic-ai/claude-code` installed via `npm i -g`; Module 0 tells learners "use the latest version" and does not pin a minimum.
- Q: Module 08 capstone exact scope? → A: Three commands + JSON persistence — `python notes.py add <text>`, `python notes.py list`, `python notes.py delete <id>`; reads/writes `notes.json` in the current working directory; single-file `notes.py`, ≤ 100 LOC, Python 3.11+, no third-party dependencies. Grader verifies by running the three commands in sequence.
- Q: Self-paced grading authority for the capstone? → A: Automated smoke check — ship `scripts/check-beginner-capstone.sh <path-to-notes.py>` that runs `add` → `list` → `delete` → `list` against the learner's file, asserts the expected output, and prints `PASS` plus a short verification token. The certificate template gains a `{{VERIFICATION_TOKEN}}` field the learner pastes in. Quiz remains self-graded against `answer-key.md`.
- Q: Skills (`SKILL.md`) policy for the beginner course? → A: Allow opportunistically — no `SKILL.md` is required, but if a module naturally produces one it MAY be added under `skills/beginner/<slug>/SKILL.md`. No minimum, no maximum. If any are added they inherit MIT licensing per FR-060 and MUST conform to the same 6-section structure the intermediate-course validator already enforces. No author is obligated to introduce skills purely to fill a quota.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Absolute beginner runs Claude Code for the first time and ships one small change (Priority: P1)

A learner who has never used Claude Code (or any AI coding assistant) opens the course README, follows the install steps, runs Claude Code in a sample repo, asks it to do one tiny thing (e.g. "add a hello-world function to `app.py`"), reviews the diff, accepts it, and runs the resulting code. They finish the first lesson in ~15 minutes feeling that the tool works on their machine and that they understand what just happened.

**Why this priority**: This is the absolute floor of competence. Without it nothing else in the course matters. The existing intermediate bootcamp (`001-bootcamp-course-materials`) explicitly assumes Claude Code is already installed and the learner already knows how to chat with it; this course must remove that assumption.

**Independent Test**: A non-developer (or a developer who has only used ChatGPT in a browser) can clone the repo, follow `module-00-setup/README.md` end-to-end, complete the Module 1 exercise, and produce the expected `hello.txt` artifact without asking for help. Verified by walking one such learner through it from cold.

**Acceptance Scenarios**:

1. **Given** a fresh laptop with no AI tooling installed, **When** the learner follows `module-00-setup/README.md` step by step, **Then** they end with a working `claude` command in their terminal and a successful "first prompt" round-trip captured in `module-00-setup/first-prompt.txt`.
2. **Given** the learner has completed Module 0, **When** they follow the Module 1 exercise, **Then** they produce the deliverable file the exercise asks for and the slide deck's "Definition of done" checklist passes on first read.
3. **Given** any single lesson, **When** the learner reads the slide deck top-to-bottom, **Then** they can state the lesson's promise, the one concept introduced, and the one thing they will produce — without needing the instructor.

---

### User Story 2 — Self-paced learner finishes the whole course in a weekend (Priority: P1)

A motivated beginner completes all 8 modules over two evenings (≈4–5 hours total seat time, including exercises) entirely on their own, without a live instructor. They earn a certificate of completion by passing a short knowledge quiz and producing the small capstone artifact.

**Why this priority**: The course must work *without* a live workshop facilitator. The existing intermediate bootcamp is designed for instructor-led delivery; this beginner course must be self-serve first, instructor-friendly second.

**Independent Test**: One self-paced learner, working alone, can go from `README.md` to a signed certificate in ≤ 5 hours of focused work, including the quiz and capstone. Verified by timing one learner.

**Acceptance Scenarios**:

1. **Given** the learner has finished Module 8, **When** they take the knowledge quiz, **Then** they can pass it on a single attempt if they completed every exercise (i.e. answers are present in the slides or exercises, never in outside material).
2. **Given** the learner has passed the quiz and completed the capstone, **When** they fill in the certificate template, **Then** the certificate is ready to share (PDF or PNG) with no further instructor sign-off required.

---

### User Story 3 — Workshop facilitator runs the same content as a half-day live session (Priority: P2)

An instructor reuses the same decks and exercises to deliver a 3-hour beginner workshop (group setting, projector, mixed-skill audience). They follow an instructor guide that maps each module to a wall-clock minute budget and gives them facilitation prompts at every checkpoint.

**Why this priority**: Reusing the same artifacts for both self-paced and live delivery is a force multiplier and matches the pedagogy of the existing intermediate bootcamp. P2 because the self-paced path (User Story 2) must work even if the instructor guide is never written.

**Independent Test**: An instructor can run a 180-minute live session using only `beginner-instructor-guide.md` and the decks, hitting the per-module minute budget within ±10%. Verified by one dry-run.

**Acceptance Scenarios**:

1. **Given** the instructor guide, **When** the facilitator follows the suggested minute budget per module, **Then** the total live session fits in 180 minutes including a 15-minute break.
2. **Given** any module deck, **When** the facilitator reaches the "Show me" slide, **Then** the live demo runs end-to-end in ≤ 5 minutes on a clean machine.

---

### User Story 4 — Existing intermediate-bootcamp learner uses this as remedial pre-work (Priority: P2)

A learner enrolled in the intermediate bootcamp (`001-bootcamp-course-materials`) realises they are missing fundamentals after Module 1 of the intermediate course. They can pivot to this beginner course, finish it in a few hours, and rejoin the intermediate course at Module 2 without confusion.

**Why this priority**: This is the integration story between the two courses. P2 because it depends on User Stories 1 and 2 already working.

**Independent Test**: A learner who finishes this beginner course's Module 8 can read `student-guide.md` (the intermediate course's student guide) and recognise every Claude Code term and tool referenced there. Verified by cross-reading: every Claude Code concept the intermediate course assumes is taught at least once in this beginner course.

**Acceptance Scenarios**:

1. **Given** the beginner course is complete, **When** the learner opens the intermediate course's Module 1 deck (`slides/part-01-setup-mindset.md`), **Then** they understand every concept on the "Concepts" slide (CLAUDE.md, prompts, accept/reject diffs, terminal use) without further definitions.
2. **Given** the cross-reference table in this course's README, **When** the learner clicks any "see also" link into the intermediate course, **Then** the link resolves and the target section makes sense as a next step.

---

### Edge Cases

- **Learner is on Windows without WSL2** — Course assumes macOS, Linux, or Windows-with-WSL2 (same as the intermediate bootcamp). Module 0 must say so on the first page and link to the WSL2 install path; the validator must catch any module that quietly assumes only macOS.
- **Learner has no Claude account / no API key** — Module 0 must walk through account creation, plan selection (Free is acceptable for ≥ 7 of the 8 modules), and explicitly call out which module needs a paid plan (if any).
- **Claude Code is rate-limited mid-exercise** — Each exercise must state explicitly whether it is "Free-plan friendly" and, if not, the equivalent dry-run path so the learner can still complete the lesson.
- **Learner accepts a bad diff and breaks their working copy** — Every exercise must run inside its own folder (`exercises/beginner/part-NN/`) and the exercise instructions must include a one-line `git restore` (or equivalent) recovery step.
- **Learner copy-pastes a prompt that contains private information** — Module 7 (safety & responsible use) must teach the "no secrets, no PII in prompts" rule and the exercises must never ask the learner to paste anything sensitive.
- **Forbidden-token leakage from the intermediate course** — Some slide content may be tempting to copy from `001-bootcamp-course-materials`. The validator (the same forbidden-tokens regex used by the intermediate course) must also run against this course's authoring files.
- **Decks render inconsistently** — The slide build path must be the same Marp-CLI pipeline as the intermediate course (`slides/deploy-pptx.sh`) so a single command builds both courses.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Course shape & positioning

- **FR-001**: The course MUST be authored as a sibling to `001-bootcamp-course-materials`, NOT inside it. Beginner-specific authoring files live under `slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, plus top-level `beginner-student-guide.md`, `beginner-instructor-guide.md`, `beginner-certificate-template.md`, and `GLOSSARY.md`. This sibling layout is locked: the beginner course shares one `slides/deploy-pptx.sh` build pipeline and one `scripts/validate.sh` with the intermediate course (per Clarifications 2026-05-21 Q1).
- **FR-002**: The course MUST consist of exactly 8 numbered modules (01–08) plus a Module 00 prework. Each module MUST be deliverable in 20–30 minutes of seat time (including its exercise), summing to between 200 and 240 minutes total seat time across modules 01–08.
- **FR-003**: The course MUST be self-paced by default and instructor-led by option. Every module MUST work end-to-end without a live facilitator.
- **FR-004**: The course MUST target absolute beginners. The reading level MUST be at most equivalent to a US high-school senior; jargon MUST be defined inline on first use; no module may assume prior CLI, git, or Python knowledge beyond what an earlier module of this course taught.
- **FR-005**: The course MUST be specifically about **Claude Code** (the CLI / IDE / desktop tool), NOT about `claude.ai` web chat. Where `claude.ai` is mentioned it must be as a comparison point only. The supported distribution channel is the official CLI `@anthropic-ai/claude-code` installed via `npm i -g`; Module 0 instructs learners to install the latest version and does NOT pin a minimum version (per Clarifications 2026-05-21 Q2). Screenshots and transcripts MUST be taken from this CLI surface, not from the desktop GUI.
- **FR-006**: The course MUST cross-reference the intermediate course (`001-bootcamp-course-materials`) from its README and from the final module ("what's next") so a graduate has an obvious next step.

#### Slide decks — easier and more explanatory than the intermediate course

- **FR-010**: Each module MUST ship one Marp slide deck under `slides/beginner/part-NN-<slug>.md`. The deck MUST use the same Marp frontmatter shape as the intermediate course (`marp: true`, `theme: default`, `paginate: true`, `size: 16:9`, `title`, `description`) and MUST include a `<!-- duration: NN min -->` marker matching the canonical budget below.
- **FR-011**: Each deck MUST follow a **simplified 10-section structure** (NOT the intermediate course's 14-section structure):

  1. Title slide
  2. What you'll learn (3 bullets max, plain-language learning objectives)
  3. Why this matters (one short paragraph + one analogy)
  4. The one concept (a single named idea with a one-sentence definition)
  5. Show me (a screenshot, a tiny code block, or a short transcript of a real Claude Code session — not pseudocode)
  6. Try it yourself (a 3–5 step micro-exercise the learner does in the slide, not in a separate file)
  7. Common mistakes (≤ 3 items, each one sentence)
  8. Lesson reflection (1–2 prompts the learner answers in their head)
  9. What's next (one line pointing at the next module)
  10. Glossary card (every new term introduced in this module with a one-line definition)

- **FR-012**: Each deck MUST contain at least one **annotated screenshot** or a real, runnable code block — never decorative stock imagery. Diagrams MUST use Mermaid (rendered via the same wireframe pipeline as the intermediate course) or plain ASCII.
- **FR-013**: Each deck MUST contain at most 12 content slides (excluding title and glossary). Density target: a slide is too dense if it has more than 5 bullets or more than 8 lines of code.
- **FR-014**: Every prompt shown to the learner in a deck MUST be verbatim copy-pasteable into Claude Code. No truncated `...` and no editorial paraphrases.
- **FR-015**: Every term from the Glossary card slide MUST appear in the course-wide `GLOSSARY.md` (single source of truth across all 8 modules); definitions MUST be identical character-for-character.

#### Exercises — easier and more explanatory than the intermediate course

- **FR-020**: Each module MUST ship one exercise under `exercises/beginner/part-NN/README.md`. The exercise MUST be completable in ≤ 15 minutes by a learner who watched the deck once.
- **FR-021**: Each exercise README MUST follow a **simplified 7-section structure** (NOT the intermediate course's 9-section structure):

  1. What you'll build (1–2 sentences)
  2. Before you start (prerequisites + a "you should have completed module N-1" line)
  3. Step-by-step (numbered list, ≤ 10 steps, each step exactly one action)
  4. The prompt to paste (a fenced code block the learner copies into Claude Code verbatim)
  5. How to know it worked (a checkbox list + the exact terminal command to verify, with expected output)
  6. If something went wrong (a "symptom → cause → one-line fix" table, ≥ 3 rows)
  7. You did it! (one line congratulating the learner + a single optional stretch challenge of one sentence)

- **FR-022**: Every exercise MUST run in its own folder (`exercises/beginner/part-NN/`) and MUST NOT depend on any state from a previous exercise. Each exercise MUST ship a `starter/` subfolder containing whatever scaffolding the learner needs so step 1 is never "create the file."
- **FR-023**: Every exercise MUST ship a reference solution under `exercises/beginner/part-NN/solution/` that the learner can diff against. The solution MUST be working code (or working text artifact) — not pseudocode.
- **FR-024**: Every exercise MUST be runnable on Free-plan Claude Code (no paid features required). If a module's natural demo requires a paid feature, the exercise MUST use a Free-plan equivalent and the deck MUST explain the difference in one line.
- **FR-025**: Every exercise MUST end with a single concrete artifact the learner can point at (a file, a screenshot, or a captured terminal transcript). "Understanding it" is never an acceptable deliverable.

#### Module curriculum (the 8 modules)

- **FR-030**: The 8 modules MUST cover, in this fixed order:

  1. **Module 01 — Meet Claude Code** (what it is, how it differs from chat-in-a-browser, install verification) — 20 min, ≤ 8 content slides.
  2. **Module 02 — Your first conversation** (open it, ask one thing, accept a diff, reject a diff, undo) — 25 min, ≤ 10 content slides.
  3. **Module 03 — Asking for what you want** (plain-language prompt patterns: role, goal, constraints; ≤ 5 example prompts) — 30 min, ≤ 12 content slides.
  4. **Module 04 — Reading code together** (point Claude Code at a file, ask "explain this," ask follow-ups) — 25 min, ≤ 10 content slides.
  5. **Module 05 — Editing one file safely** (small, reversible edits; reading the diff; the accept/reject mental model) — 30 min, ≤ 12 content slides.
  6. **Module 06 — CLAUDE.md, the cheat sheet** (the single project-level context file; a ≤ 20-line example; how it changes Claude's behaviour) — 25 min, ≤ 10 content slides.
  7. **Module 07 — Safer & smarter** (no secrets in prompts, when to say no to a diff, when to start fresh, simple permission model) — 25 min, ≤ 10 content slides.
  8. **Module 08 — Putting it together** (a 15-minute capstone: build a tiny `notes.py` CLI with `add`/`list`/`delete` subcommands and JSON persistence, from scratch with Claude Code; this is the certificate-eligible artifact — see FR-033) — 30 min, ≤ 12 content slides.

  Canonical minute budget: 20 + 25 + 30 + 25 + 30 + 25 + 25 + 30 = **210 minutes** across modules 01–08 (within the 200–240 window of FR-002).

- **FR-031**: Module 01's "Show me" slide MUST be a real terminal transcript of installing and launching Claude Code on macOS, copy-pasted from an actual run, not faked.
- **FR-032**: Module 06's CLAUDE.md example MUST be a real working file ≤ 20 lines that can be dropped into `exercises/beginner/part-06/starter/` and produce a visible behaviour change in the next prompt.
- **FR-033**: Module 08's capstone MUST be a single-file Python program `notes.py`, ≤ 100 lines of code total, runnable with no installed dependencies beyond Python 3.11+ (already required by the intermediate course). It MUST expose exactly three subcommands invoked as `python notes.py add <text>`, `python notes.py list`, and `python notes.py delete <id>`, persisting state to `notes.json` in the current working directory (per Clarifications 2026-05-21 Q3). It MUST be the artifact the certificate is awarded against.

#### Assessment & certificate

- **FR-040**: The course MUST ship one knowledge quiz at `assessments/beginner/quiz.md` with exactly 16 multiple-choice questions (2 per module), each with 4 options and exactly one correct answer.
- **FR-041**: Every quiz answer MUST be derivable from material physically present in the slides or exercises of this course; no outside reading required.
- **FR-042**: The course MUST ship an answer key at `assessments/beginner/answer-key.md` with the correct letter, the source module/slide, and a one-sentence rationale per question.
- **FR-043**: The course MUST ship a certificate template at `beginner-certificate-template.md` (sibling to the intermediate `certificate-template.md`) with the same template variables (`{{STUDENT_NAME}}`, `{{COMPLETION_DATE}}`, `{{INSTRUCTOR_NAME}}`, `{{WORKSHOP_TITLE}}`) and the same render path (`sed` + `pandoc` or `marp`).
- **FR-044**: The pass threshold MUST be ≥ 12/16 on the quiz AND a working Module 08 capstone artifact. "Working" is defined as `scripts/check-beginner-capstone.sh <path-to-notes.py>` exiting 0 and printing `PASS` (per Clarifications 2026-05-21 Q4 and FR-045). Failure on either part means "retake the relevant module"; no partial credit.
- **FR-045**: The repository MUST ship `scripts/check-beginner-capstone.sh` that takes a path to the learner's `notes.py`, runs `add "hello"` → `list` → `delete 1` → `list` against it in an isolated temp directory, asserts the expected stdout at each step, and on success prints `PASS` followed by a short verification token (e.g. an 8-char hash of the captured output). On failure it MUST print a one-line reason and exit non-zero. The script MUST work on macOS bash 3.2 and Linux bash 4+, with no dependencies beyond Python 3.11+ and standard POSIX utilities.
- **FR-046**: The certificate template (`beginner-certificate-template.md`, per FR-043) MUST include a `{{VERIFICATION_TOKEN}}` placeholder, populated by the learner from the output of `scripts/check-beginner-capstone.sh`. The student guide MUST document this one-line render command alongside the existing `{{STUDENT_NAME}}` / `{{COMPLETION_DATE}}` substitution example.

#### Tooling, packaging, and consistency with the intermediate course

- **FR-050**: The slide build pipeline MUST be the same `slides/deploy-pptx.sh` already used by the intermediate course. The script MUST pick up the beginner decks automatically (by extending its glob to find `slides/**/part-*.md` or by adding a beginner-specific build target — implementation choice belongs to `/speckit.plan`).
- **FR-051**: The validator (`scripts/validate.sh`) MUST be extended to enforce the beginner course's contracts: the **10-section deck structure**, the **7-section exercise structure**, the per-deck duration markers, the forbidden-tokens regex (same list as the intermediate course), and the cross-references in the beginner README. Violations MUST fail the validator with a file:line message, same as today.
- **FR-052**: The student-facing entry point MUST be `beginner-student-guide.md` (sibling to the intermediate `student-guide.md`). It MUST contain the install path, the 8-module reading order, the assessment path, and the certificate path. Total length: ≤ 200 lines.
- **FR-053**: The instructor-facing entry point MUST be `beginner-instructor-guide.md` (sibling to the intermediate `instructor-guide.md`). It MUST contain a 180-minute live schedule, per-module facilitation prompts, a common-blockers table, and the grading workflow (which is: "did the capstone artifact run? did the quiz score ≥ 12/16?"). Total length: ≤ 250 lines.
- **FR-054**: The top-level `README.md` MUST be updated to clearly position the two courses side by side: this beginner course as the "start here" path, the intermediate bootcamp as the "next step." A single ASCII or Mermaid diagram MUST show the recommended path through both courses.
- **FR-055**: All authoring files (slides, exercises, guides, certificate, quiz, answer key) MUST be free of the same forbidden tokens enforced for the intermediate course. The beginner course's content MAY use the words "easy" and "beginner" — those are NOT in the banned list and are the whole point of this course.

#### Licensing

- **FR-060**: The course MUST inherit the same dual-license model as the intermediate course: CC BY-NC-SA 4.0 at the repo root for prose/slides, MIT for any reusable skill files. Skills (`SKILL.md`) are NOT required in the beginner course; authors MAY add them opportunistically under `skills/beginner/<slug>/SKILL.md` when a module organically produces a reusable pattern, with no minimum and no maximum (per Clarifications 2026-05-21 Q5). Any skill that is added MUST conform to the same 6-section structure the intermediate-course validator already enforces; the validator MUST apply the same check to `skills/beginner/**` when present, and MUST NOT fail on its absence.

### Key Entities

- **Module**: A self-contained 20–30-minute lesson with one deck + one exercise + one verifiable artifact + 2 questions in the quiz.
- **Deck**: A Marp markdown file under `slides/beginner/part-NN-<slug>.md` matching the 10-section contract above.
- **Exercise**: A folder under `exercises/beginner/part-NN/` containing `README.md` (7-section contract), `starter/`, and `solution/`.
- **Glossary entry**: A single term + one-line plain-language definition. Authoritative copy lives in `GLOSSARY.md`; deck glossary cards quote it verbatim.
- **Quiz question**: One of 16 items in `assessments/beginner/quiz.md`. Each is bound to a module by tag so the validator can confirm full module coverage (2 per module).
- **Certificate**: A renderable template producing a shareable PDF/PNG per learner who passes the quiz and completes the capstone.
- **Learner persona**: An absolute beginner with no prior AI-coding-tool experience, on macOS/Linux/WSL2, with a Free-plan Claude account.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A self-paced absolute-beginner learner finishes Modules 00–08 and earns a certificate in ≤ 5 hours of focused work, measured wall-clock from opening the course README to producing the rendered certificate file.
- **SC-002**: ≥ 90% of self-paced learners who attempt the quiz pass on their first attempt (≥ 12/16), measured across a pilot cohort of at least 5 learners.
- **SC-003**: ≥ 90% of self-paced learners successfully produce the Module 08 capstone artifact (it runs without errors) on their first attempt, measured across the same pilot cohort.
- **SC-004**: A workshop facilitator delivers the live 180-minute version within ±10% of the per-module budgets in the instructor guide, measured on at least one live dry-run.
- **SC-005**: 100% of slides pass the 10-section structural validator; 100% of exercises pass the 7-section structural validator; 100% of authoring files pass the forbidden-tokens regex. Validator exits 0.
- **SC-006**: Every term that appears in a deck's Glossary card slide also appears in `GLOSSARY.md` with a byte-identical definition, measured by an automated diff in the validator.
- **SC-007**: Every prompt shown in a deck can be copy-pasted into Claude Code and produces an output that a human reviewer marks as "matching the lesson's intent" in ≥ 90% of trials, measured across at least 3 dry-runs per module.
- **SC-008**: Total seat time across modules 01–08 (excluding Module 00 setup) sums to between 200 and 240 minutes per the duration markers; this is enforced by the validator.

---

## Assumptions

- **Repository layout**: Beginner artifacts live in sibling folders, not nested inside `001-bootcamp-course-materials`. Specifically: `slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, plus top-level `beginner-student-guide.md`, `beginner-instructor-guide.md`, `beginner-certificate-template.md`, and `GLOSSARY.md`. **Locked** by Clarifications 2026-05-21 Q1.
- **Audience platform**: macOS, Linux, or Windows-with-WSL2 — same as the intermediate course. No native-Windows-without-WSL2 path.
- **Language/runtime baseline**: Python 3.11+ for the Module 08 capstone. Same Python baseline as the intermediate course, so no new toolchain to learn.
- **Free-plan friendliness**: All 8 modules' exercises can be completed on the Claude Code free tier. If any single feature shown requires a paid plan, the deck shows it as a screenshot and the exercise uses a free-plan equivalent.
- **Slide tooling**: Marp-CLI, reusing the existing `slides/deploy-pptx.sh`. No new build dependency.
- **No live video**: The course ships as Markdown, slides, exercises, quiz, and certificate. No recorded video content is in scope for this feature.
- **No translations**: English only for v1. Future localisations are out of scope.
- **No grading-service automation**: Quiz grading is manual (self-graded against `answer-key.md` for self-paced learners; instructor-graded in workshop mode). Capstone correctness IS automated locally via `scripts/check-beginner-capstone.sh` (per Clarifications 2026-05-21 Q4), but there is no hosted autograder service.
- **No new licensing**: Inherits the existing dual license (CC BY-NC-SA 4.0 root + MIT for any skill files).
- **Brand strings**: Reuses the same brand strings as the intermediate course where applicable ("Packt Certification", "LLM Engineering by Packt", "Luca Berton"). Workshop title differs — proposed default `"Claude Code 101 — Beginner Workshop"`, confirmable in `/speckit.plan`.
- **Cross-reference to intermediate course**: The intermediate course's existing files do NOT need to change to point back at this beginner course; the cross-link is one-way (beginner → intermediate "what's next") in v1. A bidirectional link can be added by editing the intermediate course's README in a follow-up feature.
