---
name: production-readiness-review
description: Run a full production-readiness review across observability, error handling, security, scalability, and operational concerns.
---

## Purpose

Evaluates a service or module against five production-readiness dimensions
— observability, error handling, security, scalability, and operability —
and produces a scored checklist with concrete remediation steps for every
gap found.

## When to use it

- Before deploying a new service or feature to a production environment for the first time.
- As a pre-launch gate when a team is about to cut a release candidate.
- After a major refactor to verify no operational concern was accidentally removed.
- When a postmortem reveals a gap that a pre-launch review should have caught.

## Prompt body

```text
Run a production-readiness review on TARGET.

TARGET: TARGET (a file, directory, or service description)

Evaluate each dimension below. For each item, mark PASS, FAIL, or N/A.
For every FAIL, write one sentence describing the gap and the smallest
change that closes it.

## 1. Observability
- [ ] Structured logging at INFO for key operations
- [ ] ERROR-level logging for all caught exceptions
- [ ] Health-check endpoint exists and returns 200 when healthy
- [ ] Key metrics are emitted (request count, latency, error rate)

## 2. Error handling
- [ ] All external calls (DB, HTTP, filesystem) have error handling
- [ ] Errors surface to callers with a consistent response shape
- [ ] Unhandled exceptions result in 500, not a silent hang or wrong status
- [ ] No bare `except: pass` or swallowed errors

## 3. Security
- [ ] All user input validated at the boundary
- [ ] No secrets hard-coded or logged
- [ ] Dependencies are pinned and free of known CVEs
- [ ] Auth/authz enforced on every protected route

## 4. Scalability
- [ ] No global mutable state shared across requests
- [ ] DB connections are pooled or scoped per request
- [ ] No unbounded queries (missing LIMIT on list endpoints)
- [ ] Long-running tasks are async or offloaded

## 5. Operability
- [ ] Service starts cleanly from a single command
- [ ] Graceful shutdown on SIGTERM
- [ ] Configuration via environment variables, not hard-coded values
- [ ] Runbook or README describes how to deploy and roll back

Print a summary table and an overall score: READY / NOT READY.
```

## Expected inputs

- `TARGET` — a file path, directory, or a plain-text description of the service being reviewed.

## Expected outputs

- A filled checklist for each of the 5 dimensions (PASS / FAIL / N/A per item).
- One remediation sentence per FAIL.
- A summary score table and overall `READY` or `NOT READY` verdict.

## Worked example

**Scenario:** Production-readiness review of a notes REST API before go-live.

**Invocation:**
```
/production-readiness-review TARGET=api/app.py
```

**Expected output (excerpt):**
```
## 1. Observability
- [FAIL] Structured logging — no logging present anywhere in the file.
  Fix: add `import logging` and log at INFO on each route entry.
- [FAIL] Health-check endpoint — no /health route exists.
  Fix: add `@app.get("/health") def health(): return {"status": "ok"}`.
- [N/A]  Metrics — out of scope for a single-file app.

## 2. Error handling
- [PASS] All DB calls wrapped in context manager with implicit rollback.
- [FAIL] Unhandled sqlite3.OperationalError returns inconsistent 500 shape.
  Fix: add a generic Exception handler emitting {"error": str(exc)}.

Overall: NOT READY — 4 FAILs across observability and error handling.
```
