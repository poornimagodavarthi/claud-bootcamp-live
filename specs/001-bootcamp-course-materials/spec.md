# Feature Specification: Claude Code Bootcamp — Course Materials Repository

**Feature Branch**: `001-bootcamp-course-materials`

**Created**: 2026-05-21

**Status**: Draft

**Input**: User description: "Create the complete course-materials repository for the Packt Publishing endorsed workshop: Claude Code Bootcamp — Build 10 Real-World Projects with Claude Code in One Day. A premium 5-hour live online bootcamp (4h instruction + 1h breaks/Q&A) with 10 modules, 10 hands-on projects, 10 downloadable Claude Skills, instructor and student guides, slide decks (Marp), exercises, assessments (40% quiz / 40% practical / 20% reflection, 70% pass), and a Packt-endorsed certificate template."

## Clarifications

### Session 2026-05-21

- Q: Primary language/runtime for the code-producing project labs (modules 2, 4, 5, 7, 8)? → A: Python is the single primary track for all code labs; Node.js is a secondary track only for modules 2 (CLI Task Manager), 4 (Notes App API), and 5 (Tests + Bug Fixes + Rubric).
- Q: Should exercise directories ship instructor-grade reference solutions? → A: Yes — ship a reference solution under `exercises/part-NN/solution/` for every code-producing module (2, 4, 5, 7, 8) only, hidden from the student-facing path with a clear "Do not open before completing the lab" notice; conceptual modules (1, 3, 6, 9, 10) do not require a `solution/` directory.
- Q: Cross-platform shell support policy? → A: macOS/Linux are the primary supported platforms; Windows is supported via WSL2 only, documented as a one-page setup note in `student-guide.md`. Native PowerShell and native Windows shells are not supported.
- Q: Module 7 wireframe asset — ship a canonical input or have students bring their own? → A: Ship one canonical wireframe (PNG/SVG) at `exercises/part-07/wireframe.png` plus an alternate hand-sketch variant in the same directory; the reference solution UI matches the canonical wireframe so validation and the rubric are deterministic.
- Q: How are the assessments delivered and graded? → A: Markdown-only, instructor-administered. The quiz, practical task, and reflection live as plain Markdown files; students answer in a copy or in chat; the instructor grades against `assessments/answer-key.md` and `assessments/rubric.md`. No structured machine-gradable format and no LMS export are mandated for v1.
- Q: How do students submit deliverables to the instructor for grading? → A: Students package their deliverables into a single zip and upload to the Packt LMS / Packt-provided shared drive; the instructor downloads, grades locally against the rubric, and records the score back in the LMS. No GitHub-based submission flow is required for v1.
- Q: Module 1 timebox — setup vs mindset within 20 minutes? → A: Mandatory self-paced pre-work (~30 min, completed before the live session) covers environment setup, Claude Code authentication, repository clone, and a "hello-Claude" smoke test. Module 1's live 20 minutes is then reserved for AI-first mindset content plus a brief 5-minute verification check; live setup troubleshooting is explicitly out of scope for the live session.
- Q: File format for the 10 downloadable skills? → A: Claude Code-native format. Each skill ships as `skills/<skill-name>/SKILL.md` with YAML frontmatter declaring `name` and `description`, plus the 6 required attributes (purpose, when-to-use, body, inputs, outputs, worked example) in the Markdown body. Skills are auto-discoverable when the `skills/` directory is dropped into a Claude Code-enabled project.
- Q: Repository licensing for a public, Packt-endorsed product? → A: Dual license. Course materials (slides, exercises, guides, assessments, certificate template) are released under **CC BY-NC-SA 4.0**; the `skills/` directory is released under **MIT** so graduates can reuse skills in commercial projects. The repository ships a top-level `LICENSE` (CC BY-NC-SA 4.0) and a `skills/LICENSE` (MIT), and `README.md` documents the split.
- Q: Naming collision — module 5 "Rubric" deliverable vs `assessments/rubric.md`? → A: Rename module 5's student-built deliverable to **"Code Review Rubric"**, located at `exercises/part-05/code-review-rubric.md`. The instructor-grading rubric remains at `assessments/rubric.md`. All cross-references in slides, README, and exercise materials MUST use "Code Review Rubric" for the module 5 artifact.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instructor delivers the live 5-hour bootcamp end-to-end (Priority: P1)

An instructor (Luca Berton or a licensed Packt instructor) opens the repository the morning of the workshop, builds the slide decks once, and teaches all 10 modules from a single source of truth without authoring any missing content. Each module's slides walk them through promise → concepts → live demo → lab → checkpoint, with instructor notes, common mistakes, and timing cues so the 5-hour schedule lands within tolerance.

**Why this priority**: Without this story, the workshop cannot be taught at all. Every other story is meaningless if the instructor cannot deliver the live session.

**Independent Test**: A qualified instructor (not the author) clones the repository on a clean machine, runs the slide build, opens module 1 and teaches it (or simulates teaching it) using only repository content, then continues sequentially through module 10. Pass = no module is missing required sections, no instructor needs to invent content live, and the 4-hour instruction budget is respected.

**Acceptance Scenarios**:

1. **Given** a clean clone of the repository, **When** the instructor runs the slide build script, **Then** all 10 module decks compile to PPTX (and optionally PDF/HTML) without errors and land in `slides/dist/`.
2. **Given** the instructor opens any module deck, **When** they review its slides, **Then** they find all 14 required sections (Title, Promise, Why this matters, Concepts, Live demo flow, Mini project, Step-by-step lab, Suggested Claude Code prompts, Deliverable checklist, Definition of done, Review checkpoint, Common mistakes, Instructor notes, Transition to next module).
3. **Given** the instructor consults `instructor-guide.md`, **When** they prepare for delivery, **Then** they find timing breakdowns, setup checks, AV requirements, troubleshooting, and per-module facilitation tips covering all 10 modules.
4. **Given** the published 5-hour schedule, **When** the sum of module times plus breaks plus Q&A is computed from the materials, **Then** it equals 5 hours (4h instruction + 1h breaks/Q&A) within ±5 minutes.

---

### User Story 2 - Student completes all 10 projects and earns the certificate (Priority: P1)

A beginner-to-intermediate developer who attends the live session (or self-paces afterward) follows the student guide, completes all 10 hands-on projects using the supplied exercise instructions and Claude Code prompts, takes the assessment, scores ≥ 70%, and receives a Packt-endorsed Certificate of Completion. They leave with a working portfolio and a reusable Claude Skills library.

**Why this priority**: The student outcome is the product. The bootcamp's value proposition (premium, hands-on, portfolio-producing) collapses if students cannot complete projects independently.

**Independent Test**: A volunteer developer with prerequisites (basic programming, Git, Claude Code access) works through `student-guide.md` and `exercises/part-01/` through `exercises/part-10/` without instructor help, then takes `assessments/knowledge-quiz.md` and `assessments/practical-task.md`. Pass = student produces all 10 deliverables, scores ≥ 70% against `assessments/rubric.md`, and a certificate can be issued from `certificate-template.md`.

**Acceptance Scenarios**:

1. **Given** a student has met prerequisites, **When** they open `exercises/part-N/`, **Then** they find Goal, Scenario, Starter instructions, Claude Code prompt, Manual validation steps, Expected deliverable, Definition of done, Stretch challenge, and Troubleshooting — all 9 required sections.
2. **Given** a student completes module N, **When** they self-check against the module's Definition of Done, **Then** they can determine pass/fail without instructor input.
3. **Given** a student finishes all 10 modules, **When** they open `assessments/`, **Then** they find a knowledge quiz, a practical task, a code review reflection, a rubric, and an answer key sufficient to be graded for 70% pass.
4. **Given** a student passes the assessment, **When** the instructor opens `certificate-template.md`, **Then** they can issue a Packt-endorsed Certificate of Completion with student name, date, and instructor signature placeholders.

---

### User Story 3 - Learner reuses the downloadable Claude Skills library after the bootcamp (Priority: P2)

After the workshop, a graduate copies the `skills/` directory into their own projects and immediately uses the supplied Claude Skills (CLAUDE.md template, code review, test generation, Best-of-N workflow, refactor, release notes, security checklist, Git workflow, documentation, production readiness review) on real codebases without any further instruction.

**Why this priority**: This is the durable post-workshop value. It differentiates this premium bootcamp from a slide-only course but is not blocking for the live session itself.

**Independent Test**: A graduate copies `skills/` into an unrelated project. They invoke at least 3 skills (e.g., `/review`, `/gen-tests`, `/release-notes`) on real code and obtain useful output without editing the skill files. Pass = each of the 10 skill files is self-contained, has a clear invocation pattern, and produces actionable output.

**Acceptance Scenarios**:

1. **Given** the `skills/` directory, **When** a learner inspects it, **Then** they find all 10 required skill artifacts (CLAUDE.md template, code review prompt, test generation prompt, Best-of-N workflow, refactor command, release notes command, security checklist, Git workflow checklist, documentation generation prompt, production readiness review prompt).
2. **Given** any skill file, **When** the learner reads it, **Then** they find purpose, when to use it, the prompt body, expected inputs/outputs, and at least one worked example.
3. **Given** a graduate's existing repository, **When** they place a skill file in their workspace and invoke it via Claude Code, **Then** the skill works without referencing bootcamp-specific paths or assumptions.

---

### User Story 4 - Maintainer keeps materials current and consistent across modules (Priority: P3)

The repository owner (Luca Berton) updates a module — for example, adjusting a Claude Code prompt or refreshing a screenshot — and the surrounding materials (slides, exercise, skill, assessment references) remain consistent because of repository conventions and review checkpoints.

**Why this priority**: Important for long-term sustainability of the workshop product but does not block the first delivery.

**Independent Test**: Make a controlled change to one module's deliverable definition, then verify (via README and cross-references) which other files must be updated. Pass = the dependency map is discoverable from the repository (README + module front-matter or instructor guide).

**Acceptance Scenarios**:

1. **Given** an updated module deck, **When** the maintainer rebuilds slides, **Then** the build script regenerates only outputs cleanly without manual fix-up.
2. **Given** a change in module N's deliverable, **When** the maintainer reviews `assessments/rubric.md` and `exercises/part-N/`, **Then** they can identify whether assessment criteria need updating.

---

### Edge Cases

- A student arrives without Claude Code access or with the wrong account tier: the prerequisites and `instructor-guide.md` "pre-flight" must explicitly cover this and provide a fallback (read-only mode or pair-programming with a peer).
- A learner using Windows: the workshop supports Windows only via WSL2. `student-guide.md` MUST include a concise WSL2 setup note; native PowerShell and native Windows shells are out of scope.
- The `marp` CLI is missing or Chromium is not installed: `slides/deploy-pptx.sh` must fall back to `npx --yes @marp-team/marp-cli@latest` and document the `CHROME_PATH` workaround.
- A module overruns its time budget: instructor notes must list "if running short" cuts (skip stretch challenge, skip optional sub-topic) so the schedule still lands.
- Claude Code output is unsafe, incomplete, or hallucinated during a live demo: every module must include a "Common mistakes" or review-rubric step that teaches learners to catch this rather than copy-paste.
- The repository is forked privately by a corporate cohort: licensing and Packt endorsement language must be unambiguous so internal use vs republishing is clear.
- A student fails the assessment (< 70%): the answer key and rubric must support a re-take path without the instructor reauthoring the quiz.

## Requirements *(mandatory)*

### Functional Requirements

#### Repository structure & buildability

- **FR-001**: Repository MUST contain, at minimum: `README.md`, `.gitignore`, `instructor-guide.md`, `student-guide.md`, `certificate-template.md`, a `slides/` tree (with `README.md`, `deploy-pptx.sh`, and 10 module decks named `part-01-setup-mindset.md` through `part-10-production-readiness.md`), an `exercises/` tree with subdirectories `part-01/` through `part-10/`, a `skills/` directory, and an `assessments/` directory containing `knowledge-quiz.md`, `practical-task.md`, `code-review-reflection.md`, `rubric.md`, and `answer-key.md`.
- **FR-002**: All slide decks MUST be authored in Marp-flavored Markdown and MUST build to PPTX via `slides/deploy-pptx.sh` without errors on a machine with Node.js available; PDF and HTML outputs MUST be available via flags (`--pdf`, `--html`, `--all`).
- **FR-003**: `slides/deploy-pptx.sh` MUST auto-detect a global `marp` binary and fall back to `npx --yes @marp-team/marp-cli@latest`, output to `slides/dist/`, and support a `--clean` flag.
- **FR-004**: Build artifacts (`slides/dist/`) MUST be excluded from version control via `.gitignore`.
- **FR-005**: `README.md` MUST clearly state the workshop title, Packt Publishing endorsement, instructor (Luca Berton), 5-hour duration (4h instruction + 1h breaks/Q&A), audience, prerequisites, learning outcomes, the 10-module schedule with times and deliverables, the 10 projects, repository layout, build instructions, and assessment/certification policy (40/40/20 weighting, 70% pass).
- **FR-005a**: The repository MUST publish a dual-license scheme: a top-level `LICENSE` file releasing course materials (slides, exercises, guides, assessments, certificate template) under **CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0), and a `skills/LICENSE` file releasing the `skills/` directory under the **MIT License** so graduates can reuse skills in commercial projects. `README.md` MUST document the dual-license split in a dedicated License section, replacing the current "All rights reserved" placeholder.

#### Module content (slides)

- **FR-006**: Each of the 10 module decks MUST contain all 14 required sections in this order: Title, Promise, Why this matters, Concepts, Live demo flow, Mini project, Step-by-step lab, Suggested Claude Code prompts, Deliverable checklist, Definition of done, Review checkpoint, Common mistakes, Instructor notes, Transition to next module.
- **FR-007**: Each module's Promise MUST be expressed as concrete, testable learner capabilities (verbs like "build", "configure", "review"), not motivational statements.
- **FR-008**: Each module's "Suggested Claude Code prompts" section MUST contain at least 2 ready-to-paste prompts that produce the module's deliverable when used as written.
- **FR-009**: Each module's "Definition of done" MUST be expressed as a pass/fail checklist that the student can self-verify without instructor judgment.
- **FR-010**: Module timings MUST sum to 4 hours (240 minutes) of instruction; the published 5-hour schedule MUST account for the remaining 60 minutes as breaks and Q&A/exam briefing. The canonical per-module instruction-minute budget is fixed as: M1=20, M2=24, M3=22, M4=30, M5=28, M6=22, M7=30, M8=24, M9=22, M10=18 (total = 240). Each slide deck's `<!-- duration: NN min -->` marker MUST match this table; `scripts/validate.sh` MUST verify both the per-deck markers and the sum. Any change to the per-module budget MUST be balanced against the others in the same PR (per constitution Authoring & Delivery Workflow → Schedule integrity).
- **FR-011**: The 10 modules MUST cover, in order: (1) Welcome, Setup & AI-First Mindset → AI Coding Workspace; (2) Prompting Like a Tech Lead → CLI Task Manager; (3) Project Context with CLAUDE.md → Project Brain File; (4) Build Faster with Best-of-N → Notes App API; (5) Testing, Debugging & Self-Review → Tests + Bug Fixes + **Code Review Rubric**; (6) Git Workflows for Safe AI Dev → Feature Branch Workflow; (7) Multimodal: Screenshot to UI → Dashboard UI; (8) Refactoring & Documentation at Scale → Refactor + Handoff Docs; (9) Commands, Hooks & Reusable Workflows → Personal Claude Skills / Command Library; (10) Production Readiness → Production Readiness Report. The module 5 "Code Review Rubric" deliverable is the student-built artifact (located at `exercises/part-05/code-review-rubric.md`) and is distinct from the instructor-grading rubric at `assessments/rubric.md`; all cross-references in slides, README, exercises, and skills MUST use the term "Code Review Rubric" for the module 5 artifact.

#### Exercises

- **FR-012**: Each `exercises/part-NN/` directory MUST contain a `README.md` with all 9 required sections: Goal, Scenario, Starter instructions, Claude Code prompt to use, Manual validation steps, Expected deliverable, Definition of done, Stretch challenge, Troubleshooting.
- **FR-013**: Each exercise's Claude Code prompt MUST be a complete, copy-paste-ready big prompt aligned with the module's teaching (not a stub). For code-producing labs, the prompt and starter materials MUST target **Python** as the primary track. Modules 2 (CLI Task Manager), 4 (Notes App API), and 5 (Tests + Bug Fixes + Rubric) MUST additionally provide a **Node.js (TypeScript)** secondary track with parallel prompt, validation, and reference-solution coverage; modules 7 (Dashboard UI) and 8 (Refactor + Handoff Docs) ship Python-only.
- **FR-014**: Each exercise's Manual validation steps MUST be deterministic (specific commands or observable behaviors) so a student can pass/fail themselves.
- **FR-015**: Where applicable, exercises MUST include any starter files (skeleton code, sample data, wireframe images) needed to begin without external downloads.
- **FR-015a**: Code-producing modules (2, 4, 5, 7, 8) MUST ship an instructor-grade reference solution under `exercises/part-NN/solution/` that the module's Manual validation steps verify against. The directory MUST be preceded by a top-level `exercises/part-NN/README.md` notice instructing students not to open `solution/` before completing the lab. For modules with both Python and Node.js tracks (2, 4, 5), the reference solution MUST cover both tracks (e.g., `solution/python/` and `solution/node/`). Conceptual modules (1, 3, 6, 9, 10) are exempt from the `solution/` requirement.
- **FR-015b**: `exercises/part-07/` MUST ship a canonical wireframe asset (`wireframe.png` or `.svg`) plus a hand-sketch variant (`wireframe-sketch.png` or `.svg`) committed to the repository. The reference solution under `exercises/part-07/solution/` MUST implement the canonical wireframe so that Manual validation steps and the assessment rubric are deterministic. No external downloads are required for module 7.

#### Skills library

- **FR-016**: The `skills/` directory MUST contain 10 self-contained, downloadable skill artifacts covering: CLAUDE.md template, code review prompt, test generation prompt, Best-of-N prompting workflow, refactor command, release notes command, security checklist, Git workflow checklist, documentation generation prompt, and production readiness review prompt. Each skill MUST be packaged in the **Claude Code-native skill format** as `skills/<skill-name>/SKILL.md`, with YAML frontmatter declaring at minimum `name` and `description` so the skill is auto-discoverable when the `skills/` directory is dropped into a Claude Code-enabled project.
- **FR-017**: Each skill file MUST include the 6 required attributes in its Markdown body: purpose, when to use it, the prompt/checklist body, expected inputs, expected outputs, and at least one worked example. The frontmatter `description` field MUST be a one-line summary suitable for Claude Code's skill picker.
- **FR-018**: Skills MUST be project-agnostic — no path or assumption tied to the bootcamp repository — so graduates can drop them into other codebases unchanged.

#### Assessment & certification

- **FR-019**: `assessments/knowledge-quiz.md` MUST contain enough scored items to constitute the 40% knowledge component, drawn from the listed sample topics (prompt structure, CLAUDE.md, AI code review, Git for AI workflows, Best-of-N, test generation, unsafe-output detection, refactor with constraints, multimodal inputs, production readiness). The quiz MUST be authored as plain Markdown intended for instructor-administered delivery; no structured machine-gradable format (YAML/JSON/QTI/etc.) and no LMS export are required for v1.
- **FR-020**: `assessments/practical-task.md` MUST define a graded mini-build aligned with the workshop curriculum, sufficient to constitute the 40% practical component.
- **FR-021**: `assessments/code-review-reflection.md` MUST define a written reflection task sufficient to constitute the 20% component.
- **FR-022**: `assessments/rubric.md` MUST publish the scoring scheme (40/40/20 weighting, 70% pass threshold) with per-component criteria, and `assessments/answer-key.md` MUST allow an instructor to grade the quiz consistently.
- **FR-023**: `certificate-template.md` MUST be issuable as a Packt Publishing endorsed Certificate of Completion with placeholders for student name, date, instructor signature (Luca Berton), and workshop title.
- **FR-023a**: The student submission workflow MUST be: each student packages their pre-work artifact plus 10 deliverables (code, docs, quiz answers, reflection, screenshots for visual modules) into a single zip archive and uploads it to the Packt LMS or a Packt-provided shared drive; the instructor downloads, grades locally against `assessments/rubric.md`, and records the score in the LMS. `student-guide.md` MUST document the zip layout (`module-00-prework/` containing the captured `hello-Claude` smoke-test output, then `module-01/` … `module-10/`, then `assessments/`), and `instructor-guide.md` MUST document the local grading workflow including how to run reference-solution validation against a submitted zip and how to verify pre-work completion before grading.

#### Guides

- **FR-024**: `instructor-guide.md` MUST cover: pre-flight checklist (env, accounts, AV), per-module timing and facilitation tips, "if running short" cuts per module, common student blockers, how to grade, and how to issue the certificate.
- **FR-025**: `student-guide.md` MUST cover: prerequisites, environment setup, how to follow the modules, how to submit deliverables, how to take the assessment, and how to claim the certificate.
- **FR-025a**: `student-guide.md` MUST include a **mandatory pre-work** section (estimated ≄30 minutes, self-paced, to be completed before the live session) covering: environment setup (Python 3.11+, Node.js for module 2/4/5 secondary track, WSL2 for Windows users), Claude Code authentication, repository clone, and a "hello-Claude" smoke test that the student runs and copies the output of into the pre-work checklist. Pre-work completion MUST be a stated entry condition for the live session; module 1's live 20 minutes covers AI-first mindset plus a 5-minute verification only and MUST NOT include first-time install steps.

#### Tone & quality

- **FR-026**: All content MUST avoid vague motivational filler and prioritize practical, instructor-ready, student-ready teaching assets.
- **FR-027**: All authored files MUST be complete (no placeholder-only stubs); any "TODO" must be tracked in a maintainer-facing location, not visible in delivery materials.
- **FR-027b**: `scripts/validate.sh` MUST enforce FR-026 and FR-027 by failing on any case-insensitive match of a forbidden-token regex within delivery materials (`README.md`, `instructor-guide.md`, `student-guide.md`, `certificate-template.md`, `slides/part-*.md`, `exercises/part-*/README.md`, `assessments/*.md`, `skills/*/SKILL.md`). The forbidden tokens are at minimum: `TODO`, `TBD`, `FIXME`, `XXX`, `coming soon`, `placeholder`, `lorem ipsum`, `unleash`, `revolutioniz`, `revolutionary`, `game[- ]chang`, `cutting[- ]edge`, `world[- ]class`, `next[- ]gen`, `rockstar`, `ninja`, `transform your`, `master(?:ing)? the art`. Matches inside HTML comments (`<!-- ... -->`) and inside the `specs/` and `.specify/` directories MUST be exempt so maintainer notes remain unaffected.
- **FR-027a**: Supported student platforms are macOS, Linux, and Windows-via-WSL2 only. All shell commands in slides, exercises, and the slide build script MUST execute under bash on these platforms; native PowerShell parity and native Windows shell support are explicitly out of scope.
- **FR-028**: Terminology, project names, module titles, and the 10-project list MUST be consistent across `README.md`, slides, exercises, skills, assessments, and guides.

### Key Entities

- **Module**: One of 10 teaching units. Attributes: number, title, time budget (minutes), promise, topics, project, deliverable, definition of done. Relates to one slide deck, one exercise directory, and (typically) one or more skills.
- **Project (Deliverable)**: A learner-produced artifact tied to a module (e.g., CLI Task Manager, Notes App API, Production Readiness Report). Attributes: name, module, expected outputs, validation steps.
- **Exercise**: The lab instructions for a module's project. Attributes: goal, scenario, starter instructions, Claude prompt, validation, deliverable, DoD, stretch, troubleshooting.
- **Slide Deck**: Marp Markdown source for a module. Attributes: 14 required sections, build outputs (PPTX/PDF/HTML).
- **Skill**: A reusable Claude Code prompt/command/checklist file. Attributes: purpose, when-to-use, body, inputs, outputs, example.
- **Assessment Item**: A scored quiz question, a practical task, or a written reflection. Attributes: type, weight, criteria.
- **Rubric**: Scoring scheme mapping assessment items to the 40/40/20 weighting and 70% pass threshold.
- **Certificate**: Issued artifact for passing learners. Attributes: learner name, workshop title, date, instructor, Packt endorsement.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new instructor can clone the repository, run the slide build, and start teaching module 1 in under 30 minutes from a clean machine.
- **SC-002**: 100% of the 10 module decks contain all 14 required sections; 100% of the 10 exercise directories contain all 9 required sections; 100% of the 10 skills contain all 6 required attributes (purpose, when-to-use, body, inputs, outputs, example).
- **SC-003**: The sum of module instruction times equals 240 minutes (±5 minutes), and the total schedule (instruction + breaks + Q&A) equals 300 minutes.
- **SC-004**: A student with the listed prerequisites can complete every module's deliverable using only repository content (no external instructor help) at least 80% of the time in pilot delivery.
- **SC-005**: At least 70% of pilot students score ≥ 70% on the combined assessment and qualify for the certificate.
- **SC-006**: Graduates report using at least 3 of the 10 downloadable skills in real projects within 30 days of the workshop (post-workshop survey). *Out of scope for v1: this is a post-pilot outcome metric, not a buildable artifact. The post-workshop survey instrument is not authored in v1 and is tracked separately for the first delivery's retrospective.*
- **SC-007**: Cross-reference consistency check: project names, module titles, and the 10-project list match across `README.md`, all slides, all exercises, all skills, and `assessments/rubric.md` with zero mismatches.
- **SC-008**: Slide build (`slides/deploy-pptx.sh`) succeeds end-to-end on a fresh machine with only Node.js installed (Marp self-installs via `npx`), producing PPTX for all 10 decks.
- **SC-009**: Instructor can grade a complete student submission (quiz + practical + reflection) in under 30 minutes using only `assessments/rubric.md` and `assessments/answer-key.md`.
- **SC-010**: A graduate can drop any of the 10 skill files into an unrelated repository and obtain useful Claude Code output without modifying the skill file.

## Assumptions

- The current `slides/` content (`part-01` through `part-10` Marp files and `deploy-pptx.sh`) is a starting point that will be expanded to meet the 14-section slide requirement; module 9 will be renamed/aligned to `part-09-skills-workflows.md` and module 10 to `part-10-production-readiness.md` to match the requested file names.
- Packt Publishing endorsement is confirmed: the workshop is delivered under the official Packt Certification programme as part of "LLM Engineering by Packt". Inaugural delivery is 30 May 2026 at 09:00 AM EST, live virtual. The canonical brand string "Packt Certification" MUST appear verbatim in `README.md` and `certificate-template.md`. Logo assets are supplied by Packt as a binary drop into a future `assets/` directory; their absence is not blocking for the v1 spec/plan/tasks.
- The bootcamp is delivered live online (not in-person), so AV/setup guidance focuses on screen sharing, video conferencing, and remote-pair workflows.
- Students bring their own working Claude Code access; the workshop does not provision accounts.
- "Beginner-to-intermediate" means students can read code in at least one language and use Git basics; the workshop does not teach programming fundamentals.
- Node.js is the assumed host runtime for the slide build (used by Marp). Code-producing project labs use **Python (3.11+) as the primary track**; modules 2, 4, and 5 additionally provide a **Node.js (TypeScript) secondary track**; modules 7 and 8 are Python-only.
- Workshop delivery runs in English; localization is out of scope for v1.
- The certificate is issued by the instructor (Luca Berton) under Packt's endorsement; an automated certificate-issuance system is out of scope.
- Module 9's "Personal Claude Skills / Command Library" deliverable is satisfied by the same `skills/` directory used as the post-workshop downloadable library.

## Dependencies

- **Marp CLI** (`@marp-team/marp-cli`) for slide builds; auto-installed via `npx` if not global.
- **Chromium** (downloaded by Marp on first run, or pointed to via `CHROME_PATH`) for PPTX/PDF export.
- **Claude Code** access for instructor and students (external, not provisioned by this repository).
- **Git** for source control and the module 6 workflow lab.
- **Packt Publishing** endorsement and certificate language (external approval, assumed granted).

## Out of Scope (v1)

- Automated grading or LMS integration.
- Machine-gradable quiz exports (YAML/JSON, Moodle XML, GIFT, QTI) and Packt LMS import packaging.
- Localization beyond English.
- Recorded/video versions of the workshop.
- Cloud-hosted lab environments (students use local machines).
- Custom Claude Code account provisioning.
- An `assets/` image library beyond what the wireframe lab in module 7 strictly requires.
