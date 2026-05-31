---
name: notes-api-smoke
description: Boot a single-file FastAPI notes app and assert all 5 CRUD endpoints return the correct HTTP status codes.
---

## Purpose

Starts a single-file FastAPI notes application using `uv` and runs six
curl assertions — one per endpoint plus a 404 guard — printing PASS or
FAIL for each. Requires no pre-installed environment beyond `uv`.

## When to use it

- After writing or modifying a notes API to verify every endpoint is wired up before committing.
- As a pre-merge gate to catch HTTP status-code regressions in CI or during review.
- When onboarding a deployed notes API to confirm the server is healthy end-to-end.
- After refactoring route handlers to ensure no endpoint silently stopped responding.

## Prompt body

```text
Run a smoke test against the single-file FastAPI notes app at APP_PATH on PORT.

Steps:
1. Derive the Python module name from APP_PATH (strip the directory and .py suffix).
   Start the server in the background:
     uv run --with fastapi --with uvicorn \
       uvicorn <module>:app --port <PORT> --app-dir <dir-of-APP_PATH> \
       --log-level warning &
   Wait 2 seconds for startup.

2. Run the following six assertions in order using curl.
   For each, print "PASS  <label>" if the HTTP status code matches, or
   "FAIL  <label>  (expected <X>, got <Y>)" if it does not.

   a. POST /notes  body={"title":"smoke","body":"test"}  → 201
      Capture the `id` field from the JSON response for use in c, d, f.
   b. GET  /notes                                        → 200
   c. GET  /notes/<id>                                   → 200
   d. PATCH /notes/<id>  body={"title":"updated"}        → 200
   e. GET  /notes/999                                    → 404
   f. DELETE /notes/<id>                                 → 204

3. Kill the background server.

4. Print a summary line: "Results: N/6 passed"
   If all six pass, print "ALL PASS". Otherwise print "SOME FAILED".
```

## Expected inputs

- `APP_PATH` — path to the single-file FastAPI app (e.g. `./api/app.py`). The file must expose a FastAPI instance named `app`.
- `PORT` — port to run the server on (default: `8000`). Must be free before the skill runs.

## Expected outputs

- Six lines of `PASS` / `FAIL` with labels, printed to stdout as each check completes.
- A summary line showing how many of the six assertions passed.
- `ALL PASS` or `SOME FAILED` as the final line.

## Worked example

**Scenario:** Smoke-test the notes API in `module-09/app.py` on port 8000.

**Invocation:**
```
/notes-api-smoke APP_PATH=module-09/app.py PORT=8000
```

**Runnable bash block:**

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_PATH="module-09/app.py"
PORT=8000
APP_DIR="$(dirname "$APP_PATH")"
MODULE="$(basename "$APP_PATH" .py)"
BASE="http://127.0.0.1:$PORT"
PASS=0; FAIL=0

# Boot the server
uv run --with fastapi --with uvicorn \
  uvicorn "${MODULE}:app" --port "$PORT" --app-dir "$APP_DIR" \
  --log-level warning &
SERVER_PID=$!
sleep 2

check() {
  local label="$1" expected="$2"; shift 2
  local actual
  actual=$(curl -s -o /dev/null -w "%{http_code}" "$@")
  if [ "$actual" = "$expected" ]; then
    echo "PASS  $label"
    ((PASS++)) || true
  else
    echo "FAIL  $label  (expected $expected, got $actual)"
    ((FAIL++)) || true
  fi
}

# Create a note and capture its id
NOTE_ID=$(curl -s -X POST "$BASE/notes" \
  -H "Content-Type: application/json" \
  -d '{"title":"smoke","body":"test"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

check "POST /notes → 201"          201 \
  -X POST "$BASE/notes" \
  -H "Content-Type: application/json" \
  -d '{"title":"smoke","body":"test"}'

check "GET  /notes → 200"          200 "$BASE/notes"
check "GET  /notes/$NOTE_ID → 200" 200 "$BASE/notes/$NOTE_ID"

check "PATCH /notes/$NOTE_ID → 200" 200 \
  -X PATCH "$BASE/notes/$NOTE_ID" \
  -H "Content-Type: application/json" \
  -d '{"title":"updated"}'

check "GET  /notes/999 → 404"      404 "$BASE/notes/999"
check "DELETE /notes/$NOTE_ID → 204" 204 -X DELETE "$BASE/notes/$NOTE_ID"

kill "$SERVER_PID" 2>/dev/null

echo "---"
echo "Results: $((PASS + FAIL > 0 ? PASS : 0))/6 passed"
[ "$FAIL" -eq 0 ] && echo "ALL PASS" || echo "SOME FAILED"
```

**Expected output:**
```
PASS  POST /notes → 201
PASS  GET  /notes → 200
PASS  GET  /notes/1 → 200
PASS  PATCH /notes/1 → 200
PASS  GET  /notes/999 → 404
PASS  DELETE /notes/1 → 204
---
Results: 6/6 passed
ALL PASS
```
