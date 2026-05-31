# Code Review Rubric — AI-Generated Code

One yes/no per check. Any **No** = file a bug before merging.

---

## 1. None / empty propagation
**Does every function that consumes a return value handle `None` and empty collections explicitly?**
Look for: result of `.fetchone()`, `.get()`, list indexing, or regex match passed directly into another call without a guard.

## 2. Error-path consistency
**Do all error paths return the same response shape as the happy path?**
Look for: one handler emitting `{"error": …}` while another emits `{"detail": …}`; DB exceptions that bypass the custom error handler; bare `raise` that leaks a stack trace to the caller.

## 3. User input reaching pattern-matching unescaped
**Is every user-supplied string sanitized before use in LIKE, regex, format strings, or shell commands?**
Look for: `f"%{q}%"` in a LIKE clause; `re.compile(user_input)`; `subprocess` with a constructed string. Parameterised queries protect against injection but not against wildcard/metacharacter misinterpretation.

## 4. Check-then-act without holding a lock
**Is every read-then-write sequence (exists → insert, fetch → update, select → delete) atomic or guarded?**
Look for: two separate DB round-trips with no transaction isolation, `rowcount` not checked after the write, or a second `SELECT` that assumes the first read is still valid.

## 5. Resource cleanup on all paths
**Are all acquired resources (connections, file handles, locks) released on both success and exception paths?**
Look for: `conn.commit()` inside `try` with only `finally: conn.close()` — confirm an exception skips commit and still closes. Check that the happy-path `return` does not bypass a `finally` block.

## 6. Numeric and collection boundaries
**Do all numeric operations and collection accesses handle zero, negative, and single-element inputs without special-casing at the call site?**
Look for: division by `len(xs)` without a zero check; `items[0]` on an unguarded list; `range(n - 1)` where `n` could be 0; pagination `offset` arithmetic that goes negative.

## 7. Type assumptions at boundaries
**Are types validated at every external boundary (HTTP body, CLI arg, env var, DB column) before use?**
Look for: `int(request.args["id"])` without try/except; `os.environ["PORT"]` used as a string where an int is expected; a SQLite `TEXT` column passed to arithmetic; Pydantic model fields typed `str` but used as `int` downstream.

## 8. Exhaustiveness of conditional logic
**Does every `if/elif` chain or `match` statement have an explicit `else` / `default` that either handles or deliberately raises?**
Look for: a PATCH handler that silently no-ops when all fields are `None`; a state machine that ignores unknown states; an enum match that drops unrecognised values without logging.

---

## Quick checklist (print and mark)

- [ ] 1. None / empty propagation
- [ ] 2. Error-path consistency
- [ ] 3. User input reaching pattern-matching unescaped
- [ ] 4. Check-then-act without holding a lock
- [ ] 5. Resource cleanup on all paths
- [ ] 6. Numeric and collection boundaries
- [ ] 7. Type assumptions at boundaries
- [ ] 8. Exhaustiveness of conditional logic
