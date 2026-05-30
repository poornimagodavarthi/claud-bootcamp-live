# Bug Fix Notes — module-04/winner/app.py

Bugs ranked by severity.

---

## 1. HIGH — `patch_note`: second SELECT can return `None`, crashing with `TypeError` (lines 143–147)

After the first `SELECT` confirms the note exists, a concurrent `DELETE` can win before `patch_note`'s `UPDATE` runs (A holds only a SHARED lock during the initial read, so B can acquire RESERVED and commit). The `UPDATE` silently affects 0 rows, the second `SELECT` returns `None`, and `_row_to_note(None)` calls `dict(None)` → `TypeError` → unhandled 500 instead of a clean 404.

**Fix:** Check `rowcount` after the UPDATE in `patch_note` the same way `update_note` does, and/or guard `row is None` before the final `_row_to_note`.

---

## 2. MEDIUM — LIKE wildcard injection in `list_notes` (lines 101–104)

The user-supplied `q` is embedded verbatim in `f"%{q}%"`. Any `%` or `_` in `q` acts as a SQL LIKE metacharacter, not a literal. A search for `"100%"` matches every note containing `"100"` followed by anything; `"_"` matches any single character. Not SQL injection (query is parameterised), but search results are silently wrong.

**Fix:** Escape `%`, `_`, and `\` in `q` and pass `ESCAPE '\'` to the LIKE clause.

---

## 3. MEDIUM — No-op PATCH mutates `updated_at` (lines 135–148)

If the client sends `{}` or omits both fields, `NotePatch` parses successfully with both fields `None`. The handler re-writes the existing `title` and `body` unchanged but stamps a new `updated_at`. An empty PATCH should be idempotent.

**Fix:** Short-circuit and return the current row without writing if `note.title is None and note.body is None`.

---

## 4. LOW — DB errors return a different error shape than HTTP errors (lines 76–78)

The custom exception handler maps `StarletteHTTPException` → `{"error": ...}`. An unhandled `sqlite3.OperationalError` (disk full, locked DB) falls through to FastAPI's default 500 handler, returning `{"detail": "Internal Server Error"}` — a different key. API clients can't treat all error responses uniformly.

**Fix:** Add a generic `Exception` handler that emits the same `{"error": ...}` shape.

---

## 5. LOW — No SQLite busy timeout (line 38)

`sqlite3.connect(DB_PATH)` uses the default busy timeout (effectively 0 ms in most builds). Under concurrent write load, a second writer receives `sqlite3.OperationalError: database is locked` immediately instead of waiting.

**Fix:** `sqlite3.connect(DB_PATH, timeout=5)`.

---

## 6. LOW — `@app.on_event("startup")` is deprecated (line 71)

FastAPI deprecated `on_event` in favour of the `lifespan` context manager. It still works but emits a deprecation warning at startup.

**Fix:** Convert to a `@asynccontextmanager` lifespan passed to `FastAPI(lifespan=...)`.

---

## Summary

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | HIGH | `patch_note` line 147 | `None` row crashes `_row_to_note` after concurrent delete |
| 2 | MEDIUM | `list_notes` line 101 | LIKE metacharacters in user query |
| 3 | MEDIUM | `patch_note` line 143 | Empty PATCH still updates `updated_at` |
| 4 | LOW | exception handler line 76 | DB errors return `{"detail":…}` not `{"error":…}` |
| 5 | LOW | `get_conn` line 38 | No busy timeout → immediate lock error under concurrency |
| 6 | LOW | line 71 | Deprecated `on_event` API |
