# BUGS.md — Module 5 seeded bugs

> **Instructor**: do not share before students have generated their own test suite.
> **Students**: inject these into your module-4 winner before running self-review.

## Bug 1 — off-by-one in search

**File:** `app.py` (Python) or `src/index.ts` (Node)
**Where:** the `/notes` GET handler with `q=` parameter.

Replace the SQL clause:

```sql
WHERE title LIKE ? OR body LIKE ?
```

with:

```sql
WHERE title LIKE ? AND body LIKE ?
```

This silently breaks search: only notes that match `q` in *both* fields are returned. Tests that search for a substring present in only one field will fail.

## Bug 2 — missing 404 on PATCH for unknown id

**Where:** the PATCH handler.

Remove the "row not found → 404" guard. The handler proceeds to UPDATE a non-existent row; SQLite reports zero affected rows but the handler still returns 200 with stale data (or crashes on `None`-row access).

Expected test failure: `test_patch_partial` style tests against an unknown id should return 404; with the bug they return 200 or 500.

---

## Self-review prompt

After injecting both bugs, run the prompt below in Claude Code and confirm Claude finds both.

```text
You are reviewing a stranger's PR. The diff is below.
Enumerate every potential bug (off-by-one, null handling, race, error path,
type coercion). Rank by severity. Propose the smallest possible fix per item.
Do not write code yet — just the list.
```
