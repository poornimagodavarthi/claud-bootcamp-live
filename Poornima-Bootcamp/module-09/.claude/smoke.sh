#!/usr/bin/env bash
# pre-commit smoke test for the Notes API.
# Exits 1 if any endpoint returns an unexpected status code.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
APP_DIR="$REPO_ROOT/Claude-Code-Bootcamp-live/module-09"
PORT=18765   # high port to avoid conflicts
BASE="http://127.0.0.1:$PORT"
PASS=0; FAIL=0

echo "── notes-api-smoke (pre-commit) ──────────────────────"

# Kill any leftover server on this port
lsof -ti :"$PORT" | xargs kill -9 2>/dev/null || true

uv run --with fastapi --with uvicorn \
  uvicorn "app:app" --port "$PORT" --app-dir "$APP_DIR" \
  --log-level warning &
SERVER_PID=$!
sleep 2

check() {
  local label="$1" expected="$2"; shift 2
  local actual
  actual=$(curl -s -o /dev/null -w "%{http_code}" "$@")
  if [ "$actual" = "$expected" ]; then
    echo "PASS  $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL  $label  (expected $expected, got $actual)"
    FAIL=$((FAIL + 1))
  fi
}

NOTE_ID=$(curl -s -X POST "$BASE/notes" \
  -H "Content-Type: application/json" \
  -d '{"title":"smoke","body":"test"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "0")

check "POST /notes → 201"             201 \
  -X POST "$BASE/notes" -H "Content-Type: application/json" -d '{"title":"t","body":"b"}'
check "GET  /notes → 200"             200 "$BASE/notes"
check "GET  /notes/$NOTE_ID → 200"    200 "$BASE/notes/$NOTE_ID"
check "PATCH /notes/$NOTE_ID → 200"   200 \
  -X PATCH "$BASE/notes/$NOTE_ID" -H "Content-Type: application/json" -d '{"title":"updated"}'
check "GET  /notes/999 → 404"         404 "$BASE/notes/999"
check "DELETE /notes/$NOTE_ID → 204"  204 -X DELETE "$BASE/notes/$NOTE_ID"

kill "$SERVER_PID" 2>/dev/null

echo "──────────────────────────────────────────────────────"
echo "Results: $PASS/6 passed"

if [ "$FAIL" -gt 0 ]; then
  echo "BLOCKED — fix the failing endpoints before committing."
  exit 1
fi

echo "ALL PASS — commit allowed."
exit 0
