# Hook Fired — notes-api-smoke blocked a bad commit

## What was wired

`module-09/.claude/hooks.json` defines a `pre-commit` hook that delegates to
`module-09/.claude/smoke.sh`. The script boots the Notes API on port 18765
with `uv`, runs six curl assertions, and exits 1 if any FAIL is detected.
The git hook at `.git/hooks/pre-commit` calls this script before every commit.

## Bug introduced

One line added to `app.py` line 98 to force GET /notes → 500:

```python
raise HTTPException(status_code=500, detail="simulated bug")  # BUG
```

## Blocked commit output

```
── notes-api-smoke (pre-commit) ──────────────────────
PASS  POST /notes → 201
FAIL  GET  /notes → 200  (expected 200, got 500)
PASS  GET  /notes/1 → 200
PASS  PATCH /notes/1 → 200
PASS  GET  /notes/999 → 404
PASS  DELETE /notes/1 → 204
──────────────────────────────────────────────────────
Results: 5/6 passed
BLOCKED — fix the failing endpoints before committing.
exit code: 1
```

The commit was rejected. `git log --oneline -1` still shows the previous
commit — no new commit was created.

## Bug reverted

The `raise HTTPException` line was removed and the hook was re-run to
confirm ALL PASS before the fix was committed.
