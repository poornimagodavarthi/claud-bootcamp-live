# Bug Fix Notes — module-04/winner/app.py

Bugs ranked by severity. Line numbers refer to the current winner (candidate B:
PATCH partial update + strip-based validation, no custom exception handler).

---

## 1. HIGH — `update_note`: second SELECT can return `None`, crashing with `TypeError` (lines 137–155)

`update_note` (the `PATCH` handler) first `SELECT`s the row and returns a clean
404 if it is missing (lines 139–143). But the initial `SELECT` takes no write
lock, so a concurrent `DELETE` on another connection can commit before the
`UPDATE` at line 148 runs. The `UPDATE` then affects 0 rows, the re-`SELECT` at
lines 152–154 returns `None`, and `row_to_note(None)` calls `dict(None)` →
`TypeError` → an unhandled 500 instead of a clean 404.

**Fix:** Check `cur.rowcount` after the `UPDATE` and return `not_found()` if it is
0, and/or guard `row is None` before the final `row_to_note(row)`.

---

## 2. MEDIUM — LIKE wildcard injection in `list_notes` (line 114)

The user-supplied `q` is embedded verbatim in `like = f"%{q}%"`. Any `%` or `_`
in `q` acts as a SQL LIKE metacharacter, not a literal. A search for `"100%"`
matches every note containing `"100"` followed by anything; `"_"` matches any
single character. Not SQL injection (the query is parameterised), but search
results are silently wrong.

**Fix:** Escape `%`, `_`, and `\` in `q` and add `ESCAPE '\'` to the LIKE clause.

---

## 3. MEDIUM — No-op PATCH still mutates `updated_at` (lines 137–151)

If the client sends `{}` or omits both fields, `NoteUpdate` parses successfully
with both fields `None`. The handler coalesces back to the existing `title` and
`body` (lines 145–146) but still issues an `UPDATE` that stamps a new
`updated_at` (lines 147–151). An empty PATCH should be idempotent.

**Fix:** Short-circuit and return the current row without writing when
`note.title is None and note.body is None`.

---

## 4. LOW — Error response shapes are inconsistent (lines 91–92 vs framework defaults)

`not_found()` returns `{"error": "not found"}` for 404s, but nothing routes other
errors through that shape. A 422 validation error returns FastAPI's default
`{"detail": [...]}`, and an unhandled `sqlite3.OperationalError` (disk full,
locked DB) falls through to the default 500 handler returning
`{"detail": "Internal Server Error"}`. API clients can't treat all error
responses uniformly.

**Fix:** Register exception handlers (`RequestValidationError`, generic
`Exception`) that emit the same `{"error": ...}` envelope as `not_found()`.

---

## 5. LOW — No SQLite busy timeout (line 26)

`connect()` calls `sqlite3.connect(DB_PATH)` with the default busy timeout
(effectively 0 ms in most builds). Under concurrent write load, a second writer
receives `sqlite3.OperationalError: database is locked` immediately instead of
waiting.

**Fix:** `sqlite3.connect(DB_PATH, timeout=5)`.

---

## Summary

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | HIGH | `update_note` lines 152–155 | `None` row crashes `row_to_note` after concurrent delete |
| 2 | MEDIUM | `list_notes` line 114 | LIKE metacharacters in user query |
| 3 | MEDIUM | `update_note` lines 147–151 | Empty PATCH still updates `updated_at` |
| 4 | LOW | `not_found` lines 91–92 | 422/500 errors return `{"detail":…}` not `{"error":…}` |
| 5 | LOW | `connect` line 26 | No busy timeout → immediate lock error under concurrency |

> Note: the previous revision also flagged a deprecated `@app.on_event("startup")`
> handler. The current winner already uses an `@asynccontextmanager` `lifespan`
> (lines 46–52), so that issue no longer applies.
