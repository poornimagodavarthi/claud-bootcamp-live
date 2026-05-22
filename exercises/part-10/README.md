# Module 10 — Production Readiness Report

## Goal

Pick one project from today and write a one-page **Production Readiness Report** with a go / no-go verdict.

## Scenario

Hiring managers and tech leads want to know: would you ship what you built? Today you answer that, honestly, across 5 axes.

## Starter instructions

1. Pick one module you'd actually be willing to defend. The Notes API (module 4) is the typical pick.
2. Open `skills/production-readiness-review/SKILL.md`.
3. Create `module-10/`.

## Claude Code prompt to use

```text
PRODUCTION READINESS
Use the production-readiness-review skill against the project at <path>.

For each of the 5 axes (Security, Observability, Deployment, Runbooks, Rollback):
- One sentence answering: would this hold up in production this week?
- The single biggest risk.
- The single smallest next step that materially reduces the risk.

End with a one-line go / no-go verdict and the rationale (≤ 25 words).
```

## Manual validation steps

1. Open `production-readiness-report.md`.
2. Confirm 5 axes present, each with status + risk + next step.
3. Confirm the verdict line exists and is decisive ("Go" or "No-Go" — not "maybe").
4. Confirm rationale is ≤ 25 words.

## Expected deliverable

```text
module-10/
└── production-readiness-report.md
```

## Definition of done

- [ ] All 5 axes covered: Security, Observability, Deployment, Runbooks, Rollback.
- [ ] Each axis has status, biggest risk, smallest next step.
- [ ] Verdict line: Go / No-Go.
- [ ] Rationale ≤ 25 words.
- [ ] Report fits on one page.

## Stretch challenge

For one "yellow" axis, actually do the smallest next step. Commit the change. Document in `module-10/follow-up.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Everything "green" | Be honest. After one workshop, it's not all green. Re-score. |
| Vague next steps | "Improve security" is not a step. "Add input validation to POST /notes" is. |
| Report > 1 page | Trim. One line per axis component if needed. |
| No verdict | The verdict is the point. Add it. |
