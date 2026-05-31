# Skill invocation — notes-api-smoke

Real output from running the `notes-api-smoke` skill against the system under
test, `module-09/notes_api.py` (the Module-4 winner, carried over).

## Invocation

```
/notes-api-smoke APP_PATH=module-09/notes_api.py PORT=18765
```

Under the hood the skill boots the app with `uv` and runs six curl assertions:

```bash
uv run --with fastapi --with uvicorn \
  uvicorn notes_api:app --port 18765 --log-level warning &
# POST /notes → 201, GET /notes → 200, GET /notes/<id> → 200,
# PATCH /notes/<id> → 200, GET /notes/999 → 404, DELETE /notes/<id> → 204
```

## Output (real run)

```
── notes-api-smoke (pre-commit) ──────────────────────
PASS  POST /notes → 201
PASS  GET  /notes → 200
PASS  GET  /notes/1 → 200
PASS  PATCH /notes/1 → 200
PASS  GET  /notes/999 → 404
PASS  DELETE /notes/1 → 204
──────────────────────────────────────────────────────
Results: 6/6 passed
ALL PASS — commit allowed.
exit code: 0
```

All six endpoints return the expected status codes, including the corrected
`PATCH` partial-update and the `{"error":"not found"}` 404 from the Module-4
winner. Exit code `0` means the pre-commit hook would allow the commit.
