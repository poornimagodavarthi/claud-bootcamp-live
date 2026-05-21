# Module 5 — Testing, Debugging & Self-Review

## Goal

Generate a real test suite for your module-4 Notes API, fix two seeded bugs, and author your personal **Code Review Rubric**.

## Scenario

The winning Notes API "looks right". You don't ship code on vibes. Today you generate tests, plant two AI-style bugs, fix them via self-review, and write the rubric you'll use for the rest of your career on AI-generated code.

> **Note on naming**: this module produces *two* rubric-shaped artefacts. The student-authored one — `code-review-rubric.md` — lives in this folder. The instructor's grading rubric — `assessments/rubric.md` — is separate. Don't confuse them.

## Starter instructions

1. `cd` into your module-4 winner folder.
2. Create `module-05/`.
3. Read `solution/BUGS.md` only **after** you've generated your own test suite.

## Claude Code prompt to use

```text
GENERATE TESTS
Read the Notes API in this folder. Write a pytest suite (or vitest if Node)
covering: create, list, search, get-one, update, delete, 404, 422.
Use httpx (or fetch) and a temp SQLite DB per test. No network. No mocks
of HTTP — start the app in-process.
```

```text
SELF-REVIEW
You are reviewing a stranger's PR. The diff is below.
Enumerate every potential bug (off-by-one, null handling, race, error path,
type coercion). Rank by severity. Propose the smallest possible fix per item.
Do not write code yet — just the list.
```

```text
RUBRIC
Draft a one-page code review rubric for AI-generated code.
5–8 checks. Each check is a yes/no question that takes ≤ 30 seconds to answer.
Optimize for catching the kinds of bugs Claude tends to miss
(boundaries, error paths, hidden assumptions about types).
```

## Manual validation steps

```bash
# Track A
pytest -q                  # all green on fixed code
# Track B
npm test                   # all green on fixed code

# After injecting two bugs from BUGS.md
pytest -q                  # red — that's expected
# After applying fixes
pytest -q                  # green again
```

Confirm `code-review-rubric.md` is one page or less and is a checklist (not prose).

## Expected deliverable

```text
exercises/part-05/code-review-rubric.md   # YOUR rubric (committed here)
module-05/
├── tests/                                # full test suite
├── bug-fix-notes.md                      # 2 bugs end-to-end
└── code-review-rubric.md                 # copy of above for the submission zip
```

## Definition of done

- [ ] Test suite green on the fixed code.
- [ ] Two seeded bugs found, fixed, and documented in `bug-fix-notes.md` (symptom, cause, Claude's diagnosis, your fix).
- [ ] `code-review-rubric.md` is ≤ 1 page, is a checklist, and contains at least one item that is *not* in `skills/code-review/SKILL.md`.

## Stretch challenge

Add property-based tests using `hypothesis` (Python) or `fast-check` (Node) for the search endpoint.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Tests pass even with bugs | Suite is too shallow — add boundary cases (empty body, q="", id=0). |
| Self-review returns "looks good" | Frame it as a stranger's PR, not your own. |
| Rubric reads like prose | Convert each item to a yes/no question. |
| Confused which rubric is which | Student rubric = this folder. Instructor rubric = `assessments/rubric.md`. |
