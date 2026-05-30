---
name: code-review
description: Review a diff or file against a rubric and surface bugs, unsafe AI output, and readability issues ranked by severity.
---

## Purpose

Applies a structured rubric to a staged diff, file, or PR to identify
correctness bugs, unsafe AI-generated patterns, and readability issues.
Each finding is ranked by severity with a minimal proposed fix.

## When to use it

- Before merging a PR to catch bugs the author may have missed.
- After generating code with an AI tool to verify it is safe and correct.
- During a code review session when a second opinion is needed on a specific file.
- As a gate before deploying a change to a shared environment.

## Prompt body

```text
Review the following code as a strict, senior engineer.

Target: TARGET (a file path, diff, or the staged git diff)

Apply this rubric in order:
1. Correctness — off-by-one errors, null/None handling, unchecked return values.
2. Error paths — are all failure modes handled? Do errors surface with the right shape?
3. Type safety — implicit coercions, wrong types at boundaries, missing validation.
4. Security — injection, exposed secrets, unsafe deserialization, OWASP Top 10.
5. Readability — deeply nested logic, misleading names, missing early returns.

For each finding:
- State the severity: HIGH / MEDIUM / LOW
- Quote the exact line(s) involved
- Write one sentence describing the bug or risk
- Propose the smallest possible fix (code, not prose)

Stop after 10 findings. If none, say "No issues found."
Sort output: HIGH first, then MEDIUM, then LOW.
```

## Expected inputs

- `TARGET` — a file path (e.g. `./api/app.py`), `--staged` for the current git diff, or a pasted diff block.

## Expected outputs

- Ranked list of findings (severity, location, description, fix).
- At most 10 items, sorted HIGH → MEDIUM → LOW.
- "No issues found." if the code is clean.

## Worked example

**Scenario:** Review a newly written route handler before merging.

**Invocation:**
```
/code-review TARGET=api/routes/notes.py
```

**Expected output (excerpt):**
```
HIGH — api/routes/notes.py:47
`_row_to_note(row)` called without checking `row is None`.
Fix: add `if row is None: raise HTTPException(404)` before the call.

MEDIUM — api/routes/notes.py:31
User input `q` embedded in LIKE pattern without escaping `%` and `_`.
Fix: escape metacharacters before building the pattern string.

LOW — api/routes/notes.py:12
`@app.on_event("startup")` is deprecated in FastAPI ≥ 0.93.
Fix: replace with a lifespan context manager.
```
