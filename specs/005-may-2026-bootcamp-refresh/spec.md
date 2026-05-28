# Feature Specification: May 2026 Bootcamp Refresh

**Feature Branch**: `005-may-2026-bootcamp-refresh`

**Created**: 2026-05-28

**Status**: Draft

**Input**: User description: "Revisit all the repo. I want a robust bootcamp for my students. Nice slidedeck, nice exercises, solutions, and everything seems nice for students. Add a May 2026 upgrade pack covering: Claude Code surfaces (terminal/IDE/desktop/web), Skills-first workflows, bundled skills (/debug, /verify, /code-review), MCP connectors, hooks for guardrails, @claude in GitHub Actions, multi-agent / background workflows, overeager-agent safety + permission modes, modern production-readiness checklist, Unix-style composability. Headline upgrades: Skills, MCP, Hooks, GitHub Actions, Multi-agent."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — A new student can navigate from `README` to first deliverable in under 60 seconds (Priority: P1)

A developer who has never seen the repo before opens `README.md`, sees the 10-part agenda with durations, locates "Where do I start?" / pre-work, finds Part 1 of the slides, the matching Part 1 exercise, and the reference solution — all reachable by clicking links from the README. Inside 60 seconds they know what to do next.

**Why this priority**: If a student can't orient in the first minute, the rest of the bootcamp loses time. This is the foundation; nothing else matters if onboarding is broken.

**Independent Test**: Hand the repo to a fresh developer with a stopwatch. Verify they can reach `exercises/part-01/README.md` (the first hands-on task) and identify its deliverable within 60 seconds. Passes ⇔ they don't have to ask the instructor anything except "ready to start?"

**Acceptance Scenarios**:

1. **Given** a fresh clone, **When** the student opens `README.md`, **Then** they see the 10-part agenda with durations, a pre-work checklist, and a "Where do I start?" pointer to Part 1's slide + exercise.
2. **Given** the student clicks the Part 1 exercise link, **When** the exercise README loads, **Then** prerequisites, task summary, acceptance criteria, and the link to the reference solution are visible without scrolling past the first viewport.
3. **Given** the student finishes Part 1, **When** they look for "what's next", **Then** the exercise links to the next part and to the matching slide deck.

---

### User Story 2 — An instructor can deliver the full 4-hour bootcamp from this repo alone, with the May 2026 agentic story landed (Priority: P1)

An instructor (e.g., Luca Berton) opens the repo and runs the workshop end-to-end: slides display correctly, durations sum to 240 min, every part has a live demo, a mini project, a step-by-step lab, suggested prompts, a deliverable checklist, and a definition-of-done. The 5 headline May-2026 upgrades (Skills, MCP, Hooks, GitHub Actions, Multi-agent) are visible in the slide content and reinforced by at least one hands-on exercise.

**Why this priority**: The instructor experience is the second-most-critical journey. Without a clean delivery path, the workshop can't be repeated by the instructor or by anyone they hand the repo to.

**Independent Test**: Instructor dry-runs the full deck set with a wall clock and a checklist; verifies each module has all required slides, demos exist, and the 5 May-2026 themes each appear in ≥1 deck and ≥1 exercise. Passes ⇔ no module requires external content to deliver.

**Acceptance Scenarios**:

1. **Given** the deployed `slides/dist/pdf/*.pdf` set, **When** the instructor opens each of part-01 → part-10, **Then** each deck has Cover · Promise · Why this matters · Concepts (with SVG) · Live demo · Mini project · Step-by-step lab · Suggested prompts · Deliverable checklist · Definition of done · Transition.
2. **Given** the bootcamp agenda, **When** the instructor sums the per-deck `<!-- duration: NN min -->` markers, **Then** the total equals 240 ± 10 minutes across parts 01–10.
3. **Given** the May 2026 upgrade pack, **When** the instructor inventories slide content, **Then** Skills, MCP, Hooks, GitHub Actions, and Multi-agent each appear in ≥1 deck and each is exercised hands-on at least once in `exercises/`.
4. **Given** a fresh laptop with documented pre-work, **When** the instructor runs each module's live-demo prompt, **Then** Claude Code reaches the expected deliverable shape.

---

### User Story 3 — Every student deliverable has a working reference solution to compare against (Priority: P1)

For each of the 10 parts, the student can finish their attempt, then open `exercises/part-NN/solution/` and compare. The reference solution runs on a fresh laptop in under 5 minutes, demonstrates the rubric items, and explains the design choices.

**Why this priority**: Without reference solutions, students leave the bootcamp without a "north star". The solution closes the loop on every module's promise.

**Independent Test**: On a fresh laptop with pre-work installed, the instructor can `cd exercises/part-NN/solution && <run command>` for each part and produce the expected output within 5 minutes. Passes ⇔ all 10 solutions are executable and self-documenting.

**Acceptance Scenarios**:

1. **Given** part-NN exists, **When** a reviewer opens `exercises/part-NN/`, **Then** they find a `README.md` (the brief) AND a `solution/` directory (the reference).
2. **Given** the reference solution, **When** the reviewer follows its README, **Then** the deliverable is produced in under 5 minutes on a clean Python 3.11 / Node 20 / Git environment.
3. **Given** the assessment rubric (`assessments/rubric.md`), **When** the reference solution is scored against it, **Then** it passes every rubric item with no warnings.

---

### User Story 4 — The repo carries a pre-flight audit that catches breakage before delivery (Priority: P2)

Before each cohort, the instructor runs a single command (`scripts/preflight.sh` or `make preflight`) that verifies: all 10 deck artefacts build, all cross-links resolve, durations sum to 240 min, the wow-beginner theme is applied, no slide overflows, no `[NEEDS CLARIFICATION]` markers remain in published content, and every exercise has a solution. Non-zero exit code blocks delivery.

**Why this priority**: Critical for repeatability but not user-visible. Skipped on first run; required by run #2.

**Independent Test**: Intentionally break one rule (delete a solution dir, or insert `![w:9999]…`). The audit MUST exit non-zero and name the broken file. Passes ⇔ all known-good states return RC=0 and all known-bad states return RC≠0.

**Acceptance Scenarios**:

1. **Given** a clean checkout, **When** the instructor runs the audit, **Then** RC=0 and a one-page green report prints.
2. **Given** any FR-001..FR-020 violation, **When** the audit runs, **Then** RC≠0 with a precise pointer to the offending file/line.

---

### User Story 5 — Off-agenda content is clearly archived, not in the student's path (Priority: P2)

The repo currently carries beginner-tier slides, exercises, and a beginner course spec that are NOT part of the published 10-part agenda. A student arriving at the repo MUST NOT confuse them with the bootcamp itself. Either they live under `archive/` (or a similarly-labelled folder) OR the README/student-guide explicitly labels them as "pre-bootcamp warm-up content (optional)" and the primary navigation never references them as bootcamp modules.

**Why this priority**: Student-experience hygiene. Important for a clean delivery but the bootcamp can run with a labelled note.

**Independent Test**: A new student reads only the README and the student-guide. They can articulate what content is the bootcamp (10 parts) vs what is optional/warm-up (beginner). Passes ⇔ they don't open the beginner decks expecting them to be on today's agenda.

**Acceptance Scenarios**:

1. **Given** the bootcamp README, **When** the student looks for the agenda, **Then** the 10 parts are listed and beginner content (if retained) is labelled as optional under a separate heading.
2. **Given** the slide build, **When** the audit runs, **Then** `slides/dist/` contains exactly the 10 agenda artefacts in each format (or beginner artefacts are namespaced under `dist/archive/` and excluded from the headline count).

---

### Edge Cases

- **Student arrives without pre-work** → `README.md` MUST include a 60-second pre-flight (commands to verify Claude Code, Python 3.11+, Node 20+, Git) with one-line fixes.
- **Network-restricted venue** (no MCP, no GitHub.com) → MCP and GitHub-Actions exercises MUST have an offline fallback (a recorded demo or a local-mock exercise) so the module can still ship its deliverable.
- **Deprecated `.claude/commands/` references** in retained content → MUST be migrated to Skills (`skills/<name>/SKILL.md`) with a one-line "legacy alias" note where appropriate.
- **One module overflows its time budget** during live delivery → instructor-guide MUST mark a "cut line" per module (the slide that can be skipped without losing the deliverable).
- **Reference solution rots** when Claude Code or a dependency upgrades → audit MUST detect missing binaries / dangling shebangs on a fresh laptop and fail loudly; weekly re-run is a follow-up, not in scope.
- **A demo prompt produces a different shape today than at recording time** → polish-log per deck MUST be updated with a dated note; the rubric MUST be tolerant of shape changes that don't affect correctness.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: README MUST be the canonical entry point and MUST contain: the 10-part agenda with durations, the pre-work checklist, a repo map, build commands, an assessment overview, and an explicit "Where do I start?" pointer that reaches Part 1's slide + exercise.
- **FR-002**: Each of the 10 agenda parts (01–10) MUST have a slide deck (`slides/part-NN-*.md`), an exercise (`exercises/part-NN/README.md`), and a reference solution (`exercises/part-NN/solution/`). Cross-links between the three MUST resolve.
- **FR-003**: Each slide deck MUST cover the canonical layout: Cover · Promise · Why this matters · Concepts (with one inline SVG sized to fit the 16:9 frame) · Live demo flow · Mini project · Step-by-step lab · Suggested Claude Code prompts · Deliverable checklist · Definition of done · Common mistakes · Instructor notes · Transition. Per-deck duration is declared via `<!-- duration: NN min -->`.
- **FR-004**: The bootcamp MUST land the May 2026 upgrade pack:
  - (a) **Claude Code surfaces**: terminal, IDE (VS Code / JetBrains), desktop app, web — covered in Part 1.
  - (b) **Skills-first workflows**: `SKILL.md` authorship, frontmatter, supporting files, automatic invocation, skill vs `CLAUDE.md`, skill permissions — Part 9.
  - (c) **Bundled skills**: `/debug`, `/verify`, `/code-review`, `/loop`, `/batch` — Part 5 (debugging) and Part 8 (refactor/docs).
  - (d) **MCP connectors**: what MCP is, connectors for Jira / Slack / Drive / GitHub / internal tools, safe boundaries, prompting changes — Part 9.
  - (e) **Hooks**: `post-edit` formatter, `pre-commit` lint+tests, `pre-bash` deny dangerous, audit logging — Part 9.
  - (f) **GitHub Actions**: `@claude` mentions, PR review, issue-to-PR, scheduled maintenance, self-hosted runners (reference the official `anthropics/claude-code-action`) — Part 6.
  - (g) **Multi-agent / background workflows**: lead vs worker agents, worktree isolation, parallel sessions, when not to fan out — Part 9.
  - (h) **Overeager-agent safety**: least-privilege tools, permission modes, shell approval, do-not-touch zones, review-before-commit, disaster recovery — Part 10 (and reinforced in Part 6).
  - (i) **Unix-style composability**: `claude -p` piping, batch lint fixes, `git diff` review, CI log triage — Part 2 and Part 6.
  - (j) **Modern production-readiness checklist**: secrets scan, dependency risk, auth/authz, logging/metrics, error handling, rollback, rate limits, CI status, test coverage, accessibility, cost/perf, generated-code ownership — Part 10.
- **FR-005**: Each exercise README MUST list: prerequisites, a 1-line task summary, acceptance criteria (≥3 testable items), hints, expected duration (≤ block budget), and the link to its reference solution.
- **FR-006**: Each reference solution MUST run on a fresh laptop (Python 3.11+, Node 20+, Git, Claude Code installed) and produce the deliverable defined in the exercise within 5 minutes.
- **FR-007**: Slide artefacts (PDF, PPTX, HTML) MUST regenerate cleanly via `slides/deploy-pptx.sh --all` into the flat `slides/dist/{pdf,pptx,html}/` layout. Build MUST complete with zero errors.
- **FR-008**: Slide content MUST fit the 16:9 frame: no content overflow per `scripts/check-slide-overflow.sh --budget 22`; embedded SVGs sized with `h:` constraint (≤320px) when paired with text.
- **FR-009**: Total instruction duration across parts 01–10 MUST sum to 240 ± 10 minutes. Part 11 (Q&A · exam briefing · next steps) is instructor-led and does NOT require a slide deck unless added separately (see Q2).
- **FR-010**: Assessments under `assessments/` MUST include a knowledge quiz, a practical task, a code-review reflection, an answer key, and a rubric — all aligned to the 10 agenda parts and explicitly checking the May 2026 upgrade-pack items.
- **FR-011**: The reusable Skills library under `skills/` MUST cover: code-review, test-generation, refactor, documentation-generation, git-workflow, security-checklist, production-readiness-review, release-notes, best-of-n, claude-md-template. Each Skill MUST be project-agnostic (no repo-specific paths) and follow the contract at `specs/001-bootcamp-course-materials/contracts/skill.contract.md`.
- **FR-012**: A new `release-readiness` Skill MUST be added (May 2026 upgrade-pack item 2 project idea): it MUST check tests, docs, security, changelog, and deploy notes; it MUST be invocable as `/release-readiness` and pair with Part 10's production-readiness lab.
- **FR-013**: A new `mcp-context-brief` Skill MUST be added: it MUST capture the prompt shape for "ticket → code search → PR draft" so Part 9's MCP exercise has a durable artefact.
- **FR-014**: All cross-links between README, slides, exercises, solutions, skills, assessments, and student/instructor guides MUST resolve. Dead intra-repo links MUST cause the pre-flight audit to fail. (External URLs: see Q3.)
- **FR-015**: Off-agenda content (e.g., the beginner course in `slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, `specs/002-claude-beginner-course/`) MUST either (a) be moved under an `archive/` directory and excluded from the bootcamp's primary navigation, OR (b) be retained in place but explicitly labelled as "optional pre-bootcamp warm-up" in the README and student-guide, with the primary 10-part agenda never linking into it as a bootcamp module. [NEEDS CLARIFICATION: archive vs label-in-place — see Q1]
- **FR-016**: A pre-flight audit script (`scripts/preflight.sh` or a Makefile target) MUST verify FR-001 through FR-020 and exit non-zero on any violation, naming the offending file/line.
- **FR-017**: Each module's instructor notes MUST include a "cut line" — the slide that can be skipped if the block is running long, without losing the deliverable.
- **FR-018**: At least one exercise MUST give the student hands-on time with the official `anthropics/claude-code-action` (Part 6) — even if via a recorded demo when running offline.
- **FR-019**: At least one exercise MUST include a "forbidden files" scenario (Part 10 or Part 6) where the student configures Claude Code's permission modes / do-not-touch zones and verifies the agent respects them.
- **FR-020**: The polish-log convention from feature 004 MUST be preserved on every slide deck (HTML comment block at EOF) so dated notes can be added without breaking the build.

### Key Entities *(include if feature involves data)*

- **Module (Agenda Part)**: One of the 10 instructional blocks. Has a slide deck, an exercise, a reference solution, a duration in minutes, and links to relevant Skills.
- **Slide Deck**: A Marp markdown file at `slides/part-NN-*.md` with the canonical 12-slide layout. Builds to PDF + PPTX + HTML in `slides/dist/`.
- **Exercise**: A student-facing brief at `exercises/part-NN/README.md` with prerequisites, task, acceptance criteria, hints, and a link to the solution.
- **Reference Solution**: A working implementation at `exercises/part-NN/solution/` that satisfies the exercise's acceptance criteria.
- **Skill**: A reusable Claude Code workflow at `skills/<kebab>/SKILL.md` with `name` + `description` frontmatter and the 6 canonical H2 sections.
- **Assessment Item**: A quiz question, practical task, or reflection prompt under `assessments/`, mapped to specific agenda parts.
- **Audit Gate**: A check inside the pre-flight script that returns pass/fail with a precise pointer.
- **Polish-log Entry**: A dated HTML comment block at the EOF of a slide deck recording cohort-specific tweaks.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new student opening the repo on a fresh clone reaches `exercises/part-01/README.md` from `README.md` in under 60 seconds without instructor help.
- **SC-002**: 100% of agenda parts (01–10) have the complete bundle: slide deck + exercise README + reference solution + assessment rubric link. (Audit-enforced.)
- **SC-003**: `slides/deploy-pptx.sh --all` completes in under 10 minutes and produces exactly 30 artefacts in `slides/dist/` (10 PDF + 10 PPTX + 10 HTML) with zero errors.
- **SC-004**: The pre-flight audit returns RC=0 on a clean checkout of `main` and RC≠0 on any introduced FR-001..FR-020 violation.
- **SC-005**: Total instructional duration across parts 01–10 sums to 240 ± 10 minutes.
- **SC-006**: 100% of internal cross-links (README → slides, slides → exercises, exercises → solutions, exercises → skills, assessments → rubric) resolve. (Audit-enforced.)
- **SC-007**: Each reference solution runs to completion on a fresh laptop (Python 3.11, Node 20, Git, Claude Code installed) in under 5 minutes per exercise.
- **SC-008**: Each of the 5 headline May-2026 upgrades (Skills, MCP, Hooks, GitHub Actions, Multi-agent) appears in ≥1 slide deck AND is exercised hands-on in ≥1 exercise.
- **SC-009**: An instructor can deliver the full 4-hour bootcamp using only this repo (no external slide decks, no external notes), confirmed by a dry-run dress rehearsal.
- **SC-010**: After the workshop, ≥80% of students self-report on a 5-point scale that they "know what to do next Monday" (target ≥4/5 mean). Measured by instructor survey; repo provides the survey template.
- **SC-011**: No content marked `[NEEDS CLARIFICATION]` or `TODO` reaches the student-visible surface (README, slides, exercises). Internal specs may carry markers; published content may not.
- **SC-012**: Slide-overflow audit (`scripts/check-slide-overflow.sh --budget 22`) returns RC=0 on every published deck.

## Assumptions

- The bootcamp is one ~4-hour session split into 10 × ~20–24 minute instructional blocks plus a Q&A/exam-briefing block (Part 11), totalling roughly 240 minutes of taught content.
- The audience is working developers comfortable with Git, a shell, and at least one mainstream language (Python or JavaScript/TypeScript).
- Pre-work is mandatory and confirmed before the workshop starts: Claude Code installed, Python 3.11+, Node 20+, Git, a working IDE (VS Code or JetBrains).
- The repo is the **single source of truth** for the bootcamp: slides, exercises, solutions, skills, assessments. No external decks, no external runbooks.
- The May 2026 Anthropic feature set (Skills, Hooks, MCP, GitHub Actions, multi-agent / background sessions, bundled skills `/debug` `/verify` `/code-review` `/loop` `/batch`) is stable enough to demo. Where Anthropic's interface differs at delivery time, the instructor records the deviation in the per-deck polish-log; the rubric tolerates shape changes that don't affect correctness.
- Default delivery is on-line and at-keyboard: students follow along in their own environment. Offline / network-restricted fallbacks exist for the MCP and GitHub-Actions exercises (recorded demo or local mock).
- Beginner-tier content already in the repo is treated as optional warm-up; it is NOT a third audience tier inside the bootcamp itself.
- Build tooling is Marp CLI via `npx`, with the single self-contained theme `slides/themes/wow-beginner.css`. Marp CLI does NOT resolve CSS `@import` between themes registered via `--theme-set`; new themes (if added) MUST be self-contained.
- Part 11 (Q&A · exam briefing · next steps) is instructor-led with talking points; a slide deck is optional. [NEEDS CLARIFICATION: see Q2]
- Weekly CI re-runs of reference solutions are a follow-up effort, not part of this feature.

## Open Questions (≤3, prioritised by impact)

### Q1 — Retention strategy for beginner content (impact: scope + student experience)

**Context**: The repo carries a parallel beginner course (`slides/beginner/`, `exercises/beginner/`, `assessments/beginner/`, `specs/002-claude-beginner-course/`). The bootcamp agenda is 10 parts; beginner content is NOT on it. After a previous deletion, the beginner files were re-introduced.

**What we need to know**: How should off-agenda beginner content be retained?

**Suggested Answers**:

| Option | Answer                                                                                                                 | Implications                                                                                                          |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| A      | Move under `archive/beginner/` (slides, exercises, assessments) and exclude from primary navigation.                   | Cleanest student experience; some link breakage to fix; preserves history. **Recommended.**                           |
| B      | Keep in place but add a top-of-file banner "Pre-bootcamp warm-up (optional)" to each beginner file; README links to it under a separate "Warm-up" heading. | Minimal moves; relies on banners students may skip.                                                                   |
| C      | Delete the beginner course entirely.                                                                                   | Simplest; loses warm-up material that may be useful for some cohorts.                                                 |
| Custom | Provide your own answer                                                                                                | Describe the policy and the target directory layout.                                                                  |

**Your choice**: _[awaiting]_

### Q2 — Part 11 (Q&A · exam briefing · next steps) slide deck (impact: completeness)

**Context**: The agenda lists Part 11 as the closing block. No slide deck exists for it today.

**What we need to know**: Does Part 11 need a slide deck, or is it instructor-led from notes only?

**Suggested Answers**:

| Option | Answer                                                                                                                                  | Implications                                                                                       |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| A      | Add `slides/part-11-qa-exam-next-steps.md` covering common mistakes, prompting anti-patterns, certification rules, how to keep practising. | Completes the agenda; ~10 min extra build; aligns Part 11 with the canonical deck shape. **Recommended.** |
| B      | Keep Part 11 instructor-led; publish only talking points in `instructor-guide.md`.                                                      | Lighter touch; students leave without a slide reference.                                           |
| Custom | Provide your own answer                                                                                                                 | e.g., a single recap slide appended to Part 10.                                                    |

**Your choice**: _[awaiting]_

### Q3 — Pre-flight audit scope for external link checking (impact: tooling effort)

**Context**: FR-014 says all cross-links MUST resolve. Strict reading would include external URLs (`https://lucaberton.com/`, `https://github.com/anthropics/claude-code-action`, Anthropic docs).

**What we need to know**: Should the audit verify external URLs, or only intra-repo links?

**Suggested Answers**:

| Option | Answer                                                                                                              | Implications                                                                       |
| ------ | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| A      | Intra-repo links only (every `./x` or `specs/y` path resolves on disk). External URLs are validated by reviewers, not the audit. | Fast, deterministic, runs offline. **Recommended.**                                |
| B      | Intra-repo + external HEAD-check: the audit pings external URLs and warns on 4xx/5xx.                               | Catches link rot but requires network and adds 30–60 s; flaky in some venues.      |
| Custom | Provide your own answer                                                                                             | e.g., external check only as a separate `--with-network` flag.                     |

**Your choice**: _[awaiting]_
