# 05. Testing & Debugging

Module 05 · 28 min

## Testing, Debugging & Self-Review

**Untested AI code is a guess. Make Claude review its own work as a stranger's PR.**

### Theory · Test, then self-review (4 min)

**Test pyramid for AI code**: many cheap unit tests · a few integration tests on the happy path · always cover **error paths**.

> **Self-review prompt**: ask Claude to find bugs *as if reviewing a stranger's PR.* The framing kills sycophancy.

- Off-by-one and **boundary** bugs are Claude's blind spot — always test boundaries.
- Bundled skills cut prompt repetition: `/debug` · `/verify` · `/code-review` · `/loop` · `/batch`.
- You ship a **personal** `code-review-rubric.md` — your blind spots, not the instructor's.

### The test-and-review loop

![Test and debug loop: write tests, find the bug, self-review, fix, re-run](resources/05-test-debug-loop.png)

Tests → find the bug → **self-review as a stranger** → fix → re-run until green.

### Reference · The self-review prompt

```text
Review this code as if it were a stranger's pull request.
List every bug, edge case, and boundary error you can find.
Be specific: file, line, symptom, and the fix. Do not be polite.
```

Test in-process with a temp SQLite DB per test — **no network, no HTTP mocks, never mock the system under test.**

### Reference · Common mistakes

- Tests that mock the system under test (useless).
- Self-review without the "stranger's PR" framing (sycophantic output).
- Copying the skill rubric verbatim — your rubric must reflect *your* blind spots.
- Confusing the student rubric with the instructor grading rubric (different files).

### Live demo · Plant a bug, catch it (6 min)

1. Open the Module 4 winner; ask for a test suite (pytest + httpx, or vitest + fetch). Run → green.
2. Plant one off-by-one bug live (e.g. a pagination boundary).
3. Paste the **self-review prompt** verbatim:

```text
Review this code as if it were a stranger's PR you must approve.
List concrete bugs with file, line, and a minimal fix. Don't say "looks good".
```

4. Claude finds it → fix → re-run. Repeat with a second seeded bug.

**Success signal**: the self-review names the bug's file, line, and fix — not "looks good".

### Your turn · Suite + 2 bugs + your rubric (11 min)

**Exercise**: [`exercises/part-05/README.md`](#hands-on-exercise--module-05)

1. Write a full suite: create, list, search, get-one, update, delete, 404, 422.
2. Plant **two** seeded bugs (from the reference), use the self-review prompt to fix them.
3. Author `code-review-rubric.md` — ≤ 1 page, 5–8 checks, focused on Claude's blind spots.

**Deliverables**: green suite · `bug-fix-notes.md` (symptom → cause → diagnosis → fix) · personal rubric.

**Success signal**: tests pass on fixed code; rubric has ≥ 1 check not in `skills/code-review/SKILL.md`.

### Done & next (1 min)

**Definition of done**

- [ ] Test suite runs green on fixed code.
- [ ] `bug-fix-notes.md` documents both bugs (symptom, cause, diagnosis, fix).
- [ ] Personal rubric with ≥ 1 original check.

**Next** — tested code earns a safe path to main: branches, atomic commits, a real PR.
**Module 6 — Git Workflows for Safe AI Dev.**

## Hands-on exercise — Module 05 {#hands-on-exercise--module-05}

> **Companion repository** — Work this exercise from the live files in the [Claude Code Bootcamp repository](https://github.com/lucab85/Claude-Code-Bootcamp): [`exercises/part-05/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-05/README.md).
> Reference solution: [`exercises/part-05/solution/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-05/solution/README.md).

## Module 5 — Testing, Debugging & Self-Review

### Goal

Generate a real test suite for your module-4 Notes API, fix two seeded bugs, and author your personal **Code Review Rubric**.

### Scenario

The winning Notes API "looks right". You don't ship code on vibes. Today you generate tests, plant two AI-style bugs, fix them via self-review, and write the rubric you'll use for the rest of your career on AI-generated code.

> **Note on naming**: this module produces *two* rubric-shaped artefacts. The student-authored one — `code-review-rubric.md` — lives in this folder. The instructor's grading rubric — `assessments/rubric.md` — is separate. Don't confuse them.

### Starter instructions

1. `cd` into your module-4 winner folder.
2. Create `module-05/`.
3. Read `solution/BUGS.md` only **after** you've generated your own test suite.

### Claude Code prompt to use

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

### Manual validation steps

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

### Expected deliverable

```text
exercises/part-05/code-review-rubric.md   # YOUR rubric (committed here)
module-05/
├── tests/                                # full test suite
├── bug-fix-notes.md                      # 2 bugs end-to-end
└── code-review-rubric.md                 # copy of above for the submission zip
```

### Definition of done

- [ ] Test suite green on the fixed code.
- [ ] Two seeded bugs found, fixed, and documented in `bug-fix-notes.md` (symptom, cause, Claude's diagnosis, your fix).
- [ ] `code-review-rubric.md` is ≤ 1 page, is a checklist, and contains at least one item that is *not* in `skills/code-review/SKILL.md`.

### Stretch challenge

Add property-based tests using `hypothesis` (Python) or `fast-check` (Node) for the search endpoint.

### Troubleshooting

| Symptom | Fix |
|---|---|
| Tests pass even with bugs | Suite is too shallow — add boundary cases (empty body, q="", id=0). |
| Self-review returns "looks good" | Frame it as a stranger's PR, not your own. |
| Rubric reads like prose | Convert each item to a yes/no question. |
| Confused which rubric is which | Student rubric = this folder. Instructor rubric = `assessments/rubric.md`. |

## Solution — Module 05 {#solution--module-05}

## Reference solution — Module 5

> **Stop**: only open this after you have produced your own `tests/`, `BUGS.md` fix, and `code-review-rubric.md`.

This module ships three artefacts:

```text
solution/
├── BUGS.md          # the planted-bug catalogue + reference fix for each
├── python/          # reference test suite (pytest)
└── node/            # reference test suite (vitest)
```

### What to compare

| Your artefact | Reference | Compare on |
|---|---|---|
| `tests/` | `python/tests/` or `node/tests/` | shape (≥6 tests, ≥3 happy, ≥2 error, ≥1 boundary), no SUT mocks |
| Bug fixes | `BUGS.md` | did you find both planted bugs? did your fix touch the minimum surface? |
| `code-review-rubric.md` | (you author this — there is no canonical version) | rubric has at least 6 items, each operational |

### Code review rubric

There is **no reference** for `code-review-rubric.md` — it is your authored artefact and the module 5 deliverable. The instructor grades it against `assessments/rubric.md`'s "Code review reflection" criteria.

### Definition of done

See `../README.md`. The `code-review` skill output goes in `REVIEW.md`; at least **one applied fix** must be visible in the working diff.
