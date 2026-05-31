# Hook Fired — notes-api-smoke blocked a bad commit

## What was wired

`module-09/.claude/hooks.json` defines a single `pre-commit` hook
(`notes-api-smoke`) whose command boots `notes_api.py` on port 18765 with `uv`,
runs the skill's six curl assertions, and exits `1` if any FAIL is detected. A
thin `.git/hooks/pre-commit` shim invokes that command before every commit, so a
non-zero exit aborts the commit.

## Bug introduced

One line added to `notes_api.py` inside `list_notes` (the `GET /notes` handler)
to force a 500:

```python
def list_notes(q: str | None = Query(default=None)) -> list[Note]:
    raise RuntimeError("simulated bug")  # BUG
```

## Blocked commit output (real run)

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

The non-zero exit rejected the commit — `git log --oneline -1` still showed the
previous commit, and no new commit was created.

## Bug reverted

The `raise RuntimeError` line was removed and the hook re-run to confirm
`ALL PASS` (6/6, exit 0 — see `invocation.md`) before committing for real.
