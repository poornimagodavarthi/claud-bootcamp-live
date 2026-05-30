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

> **Watch the diff — the #1 AI trap here.** "Start the app in-process" is
> ambiguous, and models often **paste a *copy* of the API into the test file**
> (look for a comment like `# app setup (copied from notes_api.py)` or an inline
> `create_app()`). That suite is green but worthless: it tests a frozen copy, so
> a real bug you fix in `notes_api.py` is never caught. Require the test to
> **import the real module** (e.g. `import notes_api` / `from notes_api import app`)
> and point it at a temp DB by patching the module's `DB_PATH`. If Claude copied
> the code, re-prompt: *"import the app from notes_api.py — do not redefine the
> routes in the test file."*
>
> Second trap: the 404 tests it writes usually assert only the **status code**,
> never the **body shape** — so the `{"detail":{"error":"not found"}}` vs
> `{"error":"not found"}` mismatch from Module 4 passes silently. Add at least one
> `assert r.json() == {"error": "not found"}` so the suite actually pins the contract.

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
Save it as code-review-rubric.md.
```

> **Watch the filename.** Models love to invent their own — a real run wrote
> `AI_CODE_REVIEW_RUBRIC.md`. The deliverable is `module-05/code-review-rubric.md`;
> if Claude picks a different name, rename it (or add "Save it as
> `code-review-rubric.md`" to the prompt) so your folder matches the expected layout.

### Manual validation steps

Paste one command at a time (interactive zsh does not treat `#` as a comment):

```bash
pytest -q
npm test
```

Expected sequence:

- On the fixed code, `pytest -q` (track A) / `npm test` (track B) is all green.
- After injecting the two bugs from `BUGS.md`, `pytest -q` goes red — that's expected.
- After applying your fixes, `pytest -q` is green again.

Confirm `code-review-rubric.md` is one page or less and is a checklist (not prose).

### Expected deliverable

Do **all** your work inside one folder, `module-05/`:

```text
module-05/
├── tests/                 # the generated + fixed test suite
├── bug-fix-notes.md       # the 2 seeded bugs, end-to-end
└── code-review-rubric.md  # YOUR rubric (write your own — see note below)
```

> `exercises/part-05/code-review-rubric.md` (already in this repo) is a **worked
> sample** to read for ideas. It is *not* a deliverable — write your own
> `module-05/code-review-rubric.md` that reflects *your* blind spots.

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
| Tests stay green after you edit `notes_api.py` | The suite **copied** the app instead of importing it — re-prompt to `import notes_api` and patch `DB_PATH`. |
| 404 tests pass but body shape is wrong | Suite only asserts the status code — add `assert r.json() == {"error":"not found"}`. |
| `pip install` fails (`pyexpat`/dylib, Python 3.14) | Use `uv run --with pytest --with fastapi --with httpx pytest -q` — no global install needed. |
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

### Review checklist — what a real Haiku run got wrong

A live `GENERATE TESTS` run (Haiku, against the Module 4 `notes_api.py` winner)
produced a 498-line, 30-test suite that ran green — and still had three defects a
reviewer must catch. Use these as the "common AI deviations" for this module:

1. **Copied the SUT into the test file instead of importing it.** The suite opened
   with `# App setup (copied from notes_api.py)` and redefined `create_app()`,
   schemas, and every route inline. Consequence: the tests exercise a *frozen copy*
   — fix a bug in `notes_api.py` and the suite stays green, which defeats the whole
   point. **Fix:** `import notes_api`, patch `notes_api.DB_PATH` to a temp file,
   `TestClient(notes_api.app)`. (The reference fixture in `python/test_notes_api.py`
   shows the import-and-patch pattern.) **The kicker:** in the same run, the `SELF-REVIEW`
   prompt did *not* flag this — it described the copied app as "embedded for self-contained
   testing" (a feature!) and its ranked bug list named only trivia (an unused import, a
   theoretical timestamp race, a hard-coded `999`). The model will rationalise its own
   biggest mistake. That is the whole case for human review: AI self-review is a useful
   first pass, never the last word.
2. **404 tests assert only the status code, never the body.** `test_get_note_not_found_404`
   checks `status_code == 404` but not the JSON — so the Module 4
   `{"detail":{"error":"not found"}}` vs spec `{"error":"not found"}` mismatch is
   invisible. **Fix:** add `assert r.json() == {"error": "not found"}` to pin the contract.
3. **Imported but unused `unittest.mock.patch`** — despite the prompt saying "no mocks".
   Dead import; remove it. Cheap tell that the model pattern-matched a template.

A suite can be large, well-formatted, and fully green while testing the wrong thing.
That is exactly the lesson of Module 5: green is necessary, not sufficient — read the diff.

#### Environment note

The reference run hit a broken system Python (3.14, `pyexpat` dylib mismatch), so
`pip install` failed. `uv` was the working path — no global install needed:

```bash
uv run --with pytest --with fastapi --with httpx pytest -q
```

### Code review rubric

There is **no reference** for `code-review-rubric.md` — it is your authored artefact and the module 5 deliverable. The instructor grades it against `assessments/rubric.md`'s "Code review reflection" criteria.

### Definition of done

See `../README.md`. The `code-review` skill output goes in `REVIEW.md`; at least **one applied fix** must be visible in the working diff.
