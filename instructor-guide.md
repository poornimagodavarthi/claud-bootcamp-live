# Instructor Guide — Claude Code Bootcamp

> For: Luca Berton and licensed Packt instructors delivering the
> *Claude Code Bootcamp — Build 10 Real-World Projects with Claude Code in One Day*.
> Companion to: [`README.md`](README.md), [`student-guide.md`](student-guide.md), [`assessments/rubric.md`](assessments/rubric.md).

## Pre-flight checklist

Run this **the morning of delivery**, in order:

- [ ] **Environment.** Clone the repo, run `cd slides && ./deploy-pptx.sh --all`. All 11 PPTX/PDF/HTML decks produced (10 modules + Part 11 closing block). If Marp can't find Chromium, set `CHROME_PATH`.
- [ ] **Pre-delivery audit.** `bash scripts/preflight.sh` exits `RC=0`. See [Pre-delivery audit (`scripts/preflight.sh`)](#pre-delivery-audit-scriptspreflightsh) below for the 15 gates and how to interpret failures.
- [ ] **Reference solutions.** Smoke-test each `exercises/part-NN/solution/` per [`student-guide.md`](student-guide.md). All commands exit 0.
- [ ] **Claude Code account.** Logged into a working tier; `claude --version` (or your CLI/IDE equivalent) responds.
- [ ] **AV.** Screen sharing rehearsed at 16:9. Microphone tested. Recording on (if delivery contract requires).
- [ ] **Pre-work entry-condition.** All registered students submitted `module-00-prework/hello-claude.txt` to the Packt LMS at least 1 hour before start. Students without pre-work are paired or moved to async cohort.
- [ ] **Time-of-day check.** Workshop starts 09:00 AM EST. Have the schedule table from [`README.md`](README.md#schedule) visible on a second screen.

## Pre-delivery audit (`scripts/preflight.sh`)

Single command, 15 gates, ~3 seconds. Run from the repo root.

```bash
bash scripts/preflight.sh                       # all gates
bash scripts/preflight.sh --gate audit.slide-anatomy   # one gate (smoke-test)
bash scripts/preflight.sh --verbose             # show every check
```

### Return codes

| RC | Meaning | Action |
|---:|---|---|
| 0 | All block gates PASS; WARNs may exist. | Safe to deliver. |
| 1 | One or more **block** gates FAIL. | Fix before delivery. |
| 2 | Internal script error (bad invocation, missing file). | File an issue against `scripts/preflight.sh`. |
| 64 | Unsupported environment (bash too old, missing `find` or `awk`). | Use the documented environment. |

### The 15 gates

| Gate | Severity | What it checks |
|---|---|---|
| `audit.module-bundle` | block | Every module 01–10 + Part 11 has slide + exercise + solution (Part 11: slide only). |
| `audit.slide-anatomy` | block | Each deck has H1 + the 13 required H2 sections in the canonical order. |
| `audit.slide-theme` | block | Every deck declares `theme: wow-beginner`. |
| `audit.slide-overflow` | block | No slide exceeds the 22-line content budget. |
| `audit.duration-sum` | block | Σ `<!-- duration: NN min -->` markers for part-01..10 = 240 ± 5 min. |
| `audit.exercise-anatomy` | block | Each exercise README has the 9 required H2 sections. |
| `audit.solution-presence` | block | Each `exercises/part-NN/solution/` has an entry-point file (`README.md` / `run.sh` / `solution.*`). |
| `audit.skill-contract` | block | All 12 catalogued skills present; each `SKILL.md` has the 6 required H2 sections. |
| `audit.assessment-coverage` | block | All 5 assessment files present; rubric references modules 01–10; May-2026 topics covered. |
| `audit.cross-links` | block | Every intra-repo markdown link resolves. |
| `audit.bundle-coverage` | block | Skills · MCP · Hooks · GitHub Actions · Multi-agent each mentioned in ≥1 deck AND ≥1 exercise. |
| `audit.no-clarifications-in-published` | block | No `[NEEDS CLARIFICATION:` markers in published surfaces (slides/exercises/skills/assessments/README/student-guide). |
| `audit.archive-isolation` | block | Only the single, labelled README section "Optional pre-bootcamp warm-up (archived)" links into `archive/`. |
| `audit.dist-freshness` | warn | Every deck has a corresponding artefact under `slides/dist/{pdf,pptx,html}/`. Stale or missing → WARN, not block. |
| `audit.contrast` | block | Slide theme passes WCAG-AA contrast for text vs background. |

### Interpreting failures

Every FAIL prints `file:line` (or `file:` if the issue is whole-file). Fix the file, re-run. Most failures are 30-second edits.

If `audit.dist-freshness` is the only WARN and you have time for a 7-minute rebuild, run `( cd slides && ./deploy-pptx.sh --all )` to clear it. Otherwise the WARN is acceptable for delivery — the `.pptx` exports are not the source of truth.

### Injection round-trip (verify the audit catches breakage)

Once per release, prove the audit is live by deliberately breaking one thing and confirming the gate catches it:

```bash
# 1. Break the slide anatomy of one deck (delete the Promise section heading)
sed -i.bak '/^## Promise$/d' slides/part-01-setup-mindset.md
bash scripts/preflight.sh --gate audit.slide-anatomy
# Expected: RC=1, message pointing at slides/part-01-setup-mindset.md (missing 'Promise')
mv slides/part-01-setup-mindset.md.bak slides/part-01-setup-mindset.md
```

```bash
# 2. Inject a NEEDS CLARIFICATION marker
echo '<!-- [NEEDS CLARIFICATION: round-trip test] -->' >> README.md
bash scripts/preflight.sh --gate audit.no-clarifications-in-published
# Expected: RC=1, message pointing at README.md:<lineno>
git checkout README.md
```

If either round-trip does not produce the expected RC=1 + file pointer, the audit is silently broken — open an issue against `scripts/preflight.sh` before delivering.

## Live schedule (300 min total)

| Block | Minutes | Cumulative |
|---|---:|---:|
| Welcome + pre-work verification | 5 | 5 |
| Module 1 (mindset only — 20 min) | 20 | 25 |
| Modules 2–4 | 76 | 101 |
| Break #1 | 15 | 116 |
| Modules 5–6 | 50 | 166 |
| Break #2 (lunch) | 30 | 196 |
| Modules 7–9 | 76 | 272 |
| Module 10 + exam briefing | 18 | 290 |
| Wrap, certificate path, Q&A | 10 | 300 |

Adjust break placement to your cohort, but instruction-minute totals must remain at 240.

## Per-module timing & facilitation

### Module 1 — Welcome, Setup & AI-First Mindset (20 min)

- **Goal:** room is aligned on the Plan→Implement→Test→Review→Commit loop and pre-work has worked for everyone.
- **Live time:** mindset content (15 min) + 5-min pre-work verification.
- **Do not** run install steps live. Pre-work is mandatory; struggling students pair with neighbors.
- **Facilitation tip:** open with a Claude Code demo on a known repo, not a slide.
- **Common blocker:** student logged into wrong Claude tier. Fallback: read-only mode + pair with neighbor.

### Module 2 — Prompting Like a Tech Lead (24 min)

- **Goal:** student ships a CLI Task Manager via one big prompt, then iterates.
- **Live time:** concept (6) + demo (4) + lab (12) + checkpoint (2).
- **Facilitation tip:** show the prompt, then **delete one constraint** mid-demo and re-run. Discuss diff.
- **Common blocker:** student writes a vague prompt. Coach: re-state Goal, Constraints, Output format, Examples.
- **If running short:** skip stretch (multi-language CLI args).

### Module 3 — Project Context with CLAUDE.md (22 min)

- **Goal:** every student commits a real `CLAUDE.md` to a repo of their choice.
- **Live time:** concept (5) + demo (5) + lab (10) + checkpoint (2).
- **Facilitation tip:** open the `skills/claude-md-template/SKILL.md` live to show how skills accelerate authoring.
- **Common blocker:** student adds too much. Coach: every line must change Claude's behavior — if not, delete.
- **If running short:** allow students to skip the conventions section.

### Module 4 — Build Faster with Best-of-N (30 min)

- **Goal:** student ships a Notes API via Best-of-N selection from 3 candidates.
- **Live time:** concept (6) + demo (6) + lab (15) + checkpoint (3).
- **Facilitation tip:** generate N=3 candidates with the same prompt, score each on the **3-criterion rubric** (correctness, simplicity, fit), then commit the winner. Show the *losing* candidates so students see the lift.
- **Common blocker:** students compare candidates by feel. Force the rubric. The skill `skills/best-of-n/SKILL.md` gives them the script.
- **If running short:** drop N from 3 to 2.

### Module 5 — Testing, Debugging & Self-Review (28 min)

- **Goal:** student ships a pytest suite for the module 4 API + 2 fixed bugs + a personal **Code Review Rubric** at `exercises/part-05/code-review-rubric.md`.
- **Live time:** concept (6) + demo (6) + lab (13) + checkpoint (3).
- **Facilitation tip:** plant a deliberate AI-generated off-by-one bug live; ask Claude to find it via `skills/code-review/SKILL.md`. Make the rubric the **discriminator** for what counts as "done" the rest of the day.
- **Common blocker:** students conflate the **student-built** Code Review Rubric with the **instructor grading rubric** at `assessments/rubric.md`. They are different. Reinforce.
- **If running short:** ship 1 bug fix instead of 2.

### Module 6 — Git Workflows for Safe AI Dev (22 min)

- **Goal:** student opens a feature branch, asks Claude to write commit + PR text, and "merges" (or simulates the merge).
- **Live time:** concept (5) + demo (4) + lab (11) + checkpoint (2).
- **Facilitation tip:** use the `skills/git-workflow/SKILL.md` live to generate the PR description from the diff.
- **Common blocker:** students push to `main`. Coach the branch flow explicitly.
- **If running short:** skip the PR template variant.

### Module 7 — Multimodal: Screenshot to UI (30 min)

- **Goal:** student ships a single-page Dashboard UI matching `exercises/part-07/wireframe.png`.
- **Live time:** concept (5) + demo (5) + lab (17) + checkpoint (3).
- **Facilitation tip:** demo with the **sketch** variant, lab with the **canonical** variant. The lift is bigger when starting from a hand sketch.
- **Common blocker:** student ships a UI that doesn't visually match. Use `wireframe.png` side-by-side as the rubric. Push back hard on "close enough" — multimodal precision is the point.
- **If running short:** ship the layout only, skip stretch (theming/animations).

### Module 8 — Refactoring & Documentation at Scale (24 min)

- **Goal:** student refactors a module under written constraints and ships `HANDOFF.md` + `ARCHITECTURE.md`.
- **Live time:** concept (5) + demo (5) + lab (12) + checkpoint (2).
- **Facilitation tip:** the constraint list is what saves you from runaway refactors. Show one with constraints, one without; compare diff size.
- **Common blocker:** Claude rewrites everything. Tighten constraints (e.g., "no new files", "preserve public API").
- **If running short:** skip `ARCHITECTURE.md`, ship only `HANDOFF.md`.

### Module 9 — Commands, Hooks & Reusable Workflows (22 min)

- **Goal:** student authors at least one new `SKILL.md` of their own using the contract in `specs/001-bootcamp-course-materials/contracts/skill.contract.md`.
- **Live time:** concept (5) + demo (5) + lab (10) + checkpoint (2).
- **Facilitation tip:** open `skills/code-review/SKILL.md` live as the worked example, then have students copy + adapt it.
- **Common blocker:** student's skill is repo-specific. Reinforce FR-018: project-agnostic.
- **If running short:** skip the hooks subsection.

### Module 10 — Production Readiness (18 min)

- **Goal:** student picks one prior project and ships a **Production Readiness Report** across 5 axes (security, observability, deployment, runbooks, rollback).
- **Live time:** concept (4) + demo (4) + lab (8) + checkpoint (2).
- **Facilitation tip:** invoke `skills/production-readiness-review/SKILL.md` against the module 4 API to demo end-to-end.
- **Common blocker:** report is too long, no actions. Force the per-axis "1 risk + 1 next step".
- **If running short:** drop to 3 axes (security, observability, deployment).

## Pre-work verification

Each student's submission zip must contain `module-00-prework/hello-claude.txt` — a copy of Claude Code's reply to the smoke-test prompt in [`student-guide.md`](student-guide.md#mandatory-pre-work-30-min). At grading time:

- File exists.
- File is non-empty (≥ 200 chars typical).
- Reply mentions Python or Node.js (proves Claude saw the local environment).

If pre-work is missing, mark the pre-work component as 0% and proceed with grading the rest. Pre-work is not weighted in the 40/40/20 score; it is an entry condition only.

## Common student blockers

| Blocker | Fix |
|---|---|
| Wrong Claude Code tier (no `claude` command). | Use the IDE plugin path or fall back to read-only pair-programming with a neighbor. |
| Windows native shell. | Move to WSL2; refer to `student-guide.md`. |
| Marp/Chromium fails on first build. | Set `CHROME_PATH`. Worst case: render HTML and screenshot. |
| Claude hallucinates dependencies. | Pull the package list from the deck's "Suggested Claude Code prompts" — every prompt is dependency-explicit. |
| Module overrun. | Use the per-module "If running short" cuts above. |
| Student stuck mid-lab. | Open the matching `exercises/part-NN/solution/` privately, diff against student's work, coach the gap. |

## Grading workflow

1. **Download** the student's zip from the Packt LMS.
2. **Verify pre-work**: `module-00-prework/hello-claude.txt` exists and is non-empty.
3. **Per-module check**: open `module-NN/`, run the solution's validation commands against the student's deliverable. Reference solutions live at [`exercises/part-NN/solution/`](exercises/).
4. **Quiz**: grade `assessments/` against [`assessments/answer-key.md`](assessments/answer-key.md). 40% weight.
5. **Practical**: score the practical task against [`assessments/rubric.md`](assessments/rubric.md). 40% weight.
6. **Reflection**: score the code review reflection against the rubric. 20% weight.
7. **Compute total**: weighted sum. ≥70% = pass.
8. **Record** the score in the Packt LMS. Issue the certificate from [`certificate-template.md`](certificate-template.md) if pass.

Target: complete grading for one student in **≤ 30 minutes**.

## Certificate issuance

1. Open [`certificate-template.md`](certificate-template.md).
2. Replace placeholders: `{{STUDENT_NAME}}`, `{{COMPLETION_DATE}}`, `{{INSTRUCTOR_NAME}}` (default: Luca Berton), `{{WORKSHOP_TITLE}}`.
3. Render to PDF (e.g., `pandoc certificate-template.md -o certificate.pdf`) or via Packt's certificate pipeline if endorsed branding requires it.
4. Deliver to student via the Packt LMS.

## Maintenance

- Spec Kit feature: [`specs/001-bootcamp-course-materials/`](specs/001-bootcamp-course-materials/).
- Constitution: [`.specify/memory/constitution.md`](.specify/memory/constitution.md).
- Run `bash scripts/validate.sh` before every release. The validator enforces structure, terminology, durations, and the forbidden-tokens regex (FR-027b).

---

**Endorsed by Packt Certification · LLM Engineering by Packt**
