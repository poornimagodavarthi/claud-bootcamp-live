# Grading Rubric — Claude Code Bootcamp

> **For instructors.** Scoring sheet for the certificate decision.
> **Distinct from** the student-authored *Code Review Rubric* at [`../exercises/part-05/code-review-rubric.md`](../exercises/part-05/code-review-rubric.md).

## Weights

| Component | Weight | Source |
|---|---:|---|
| Knowledge quiz | **40%** | [`knowledge-quiz.md`](knowledge-quiz.md) graded against [`answer-key.md`](answer-key.md) |
| Practical task | **40%** | [`practical-task.md`](practical-task.md) deliverables |
| Code review reflection | **20%** | [`code-review-reflection.md`](code-review-reflection.md) essay |
| **Pass threshold** | **≥ 70%** weighted total | |

## Knowledge quiz (40%)

- 20 questions, 2 points each, 40 points total.
- Each correct answer = 2 points; incorrect or blank = 0.
- Convert raw / 40 to a percentage. That percentage × 0.40 is the component contribution.

## Practical task (40 points)

| Criterion | Points | Notes |
|---|---:|---|
| Service runs and passes the smoke script | 8 | All seven curl commands return expected status. |
| Tests pass and meet shape requirement | 6 | ≥ 6 tests; ≥ 3 happy, ≥ 2 error, ≥ 1 boundary; no SUT mocks. |
| `PROMPT.md` follows GCOE | 6 | All four sections present and operational. |
| `candidates.md` documents 2 candidates + justified pick | 4 | Two distinct candidates; pick rationale references the 3-criterion rubric. |
| `REVIEW.md` from `code-review` skill + at least one applied fix | 6 | Output matches skill's "Outputs" shape; fix is visible in `service/` diff. |
| `PR.md` ≤ 40 lines, all six required sections + checklist | 4 | Six sections in order; reviewer checklist 3–5 items. |
| Conventions: clean repo, runnable from a fresh clone | 4 | No dead files; `README` (or equivalent) explains run + test. |
| Anti-pattern penalties | -2 each | Skipping GCOE, mocking the SUT, single-candidate, "what but not why" PR. |
| **Subtotal** | **/ 40** | |

Convert raw / 40 to a percentage. That percentage × 0.40 is the component contribution.

## Code review reflection (20 points)

| Criterion | Points |
|---|---:|
| Both bugs are real, traceable to the student's own deliverables, and have all four sub-points (symptom · cause · fix · detection) | 6 |
| Rubric reflection names specific items from the student's own `code-review-rubric.md` (earned · drop · missing) | 5 |
| Carry-over skill named exactly + concrete day-job mapping in 2–3 sentences | 4 |
| Constraint reflection is specific (not "yes, very much") | 3 |
| Format: 4 H2 sections in order, 400–700 words | 2 |
| **Subtotal** | **/ 20** |

That subtotal × 0.20 / 0.20 = direct percentage contribution (raw / 20 × 100% × 0.20).

## Aggregation

```text
total% = (quiz_correct/20)*40 + (practical/40)*40 + (reflection/20)*20
pass = total% >= 70
```

## Edge cases

- **Pre-work missing**: do not block grading. Note it in the LMS comment; pre-work is an entry condition, not a graded component.
- **Module-5 student rubric file missing**: Reflection's "rubric" section forfeits its 5 points (the student cannot reference items they did not author).
- **Practical: tracks mixed**: acceptable if both runtimes are functional; grade against the same criteria.
- **Late submission**: instructor discretion; default policy on the Packt LMS.

## Re-take policy

- Score < 70%: one re-take allowed within 30 days using the same answer key + this rubric.
- Re-take must include all three components.

## Issuance

On pass: render [`../certificate-template.md`](../certificate-template.md) with the student's name and completion date and deliver via the Packt LMS.

## Per-module assessment mapping

Each module 01–10 must surface in at least one assessment item. This table is the cross-reference the grader uses to confirm the student demonstrated learning on every part.

| Module | Module title | Primary assessment item | Where it's graded |
|---|---|---|---|
| Module 01 | Setup & AI-First Mindset | Pre-work smoke test + quiz Q on the plan/implement/test/review loop | Knowledge quiz |
| Module 02 | Prompting Like a Tech Lead | Quiz Q on GCOE; practical-task `PROMPT.md` | Quiz + Practical |
| Module 03 | Project Context with `CLAUDE.md` | Quiz Q on CLAUDE.md sections; practical-task uses a CLAUDE.md | Quiz + Practical |
| Module 04 | Best-of-N | Quiz Q on candidate generation; practical-task `candidates.md` | Quiz + Practical |
| Module 05 | Testing, Debugging & Self-Review | Quiz Q on `code-review` skill; reflection both bugs | Quiz + Reflection |
| Module 06 | Git Workflows (incl. `@claude` GitHub Action) | Quiz Q on `@claude` action; practical-task `PR.md` | Quiz + Practical |
| Module 07 | Multimodal | Quiz Q on screenshot-to-UI prompting; practical-task UI deliverable variant | Quiz + Practical |
| Module 08 | Refactor & Handoff Docs | Quiz Q on refactor scope; reflection carry-over skill | Quiz + Reflection |
| Module 09 | Skills, Hooks, MCP, Multi-agent | Quiz Q on each of the 4 pillars; practical-task SKILL.md authoring | Quiz + Practical |
| Module 10 | Production Readiness | Quiz Q on 12-item checklist; practical-task readiness report | Quiz + Practical |

## May 2026 coverage requirements

The rubric must score the student on each of the five May 2026 headline shifts. Without these the grade does not reflect today's Claude Code surface.

| Headline shift | Mandatory assessment evidence |
|---|---|
| **Skills** (bundled + author-your-own) | ≥1 quiz item + the `SKILL.md` artefact in the practical task |
| **MCP** (Model Context Protocol connectors, e.g., Jira / Slack / GitHub) | ≥1 quiz item; practical-task brief produced with the `mcp-context-brief` skill |
| **Hooks** (`.claude/hooks.json` pre-bash / post-edit / pre-commit) | ≥1 quiz item; reflection acknowledges at least one hook the student would adopt |
| **GitHub Action `@claude`** (`anthropics/claude-code-action`) | ≥1 quiz item; practical-task `PR.md` references how `@claude` would review it |
| **Multi-agent fan-out & background runs** | ≥1 quiz item; reflection names when NOT to fan out |

Grader instruction: if any cell in this table is empty in the student's submission, deduct **3 points** from the practical-task subtotal per missing cell.
