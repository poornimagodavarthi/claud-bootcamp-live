# Production Readiness Report — Notes API
**Target**: `Claude-Code-Bootcamp-live/module-09/app.py`
**Date**: 2026-05-30
**Reviewer**: Claude Code (production-readiness-review skill)

---

## 1. Security

**Status**: Would NOT hold up in production this week — every endpoint is open to any caller with network access.

| Check | Result |
|---|---|
| Input validated at boundary | PASS — Pydantic `min_length=1`, parameterised SQL queries |
| No secrets hard-coded or logged | PASS — no credentials in source |
| Dependencies pinned, no known CVEs | N/A — runtime deps injected via uvicorn; not pinned in a lockfile |
| Auth/authz on every route | FAIL — zero authentication on any endpoint |

**Biggest risk**: No authentication — any network-reachable client can read, create, edit, and delete all notes.

**Smallest next step**: Add a FastAPI dependency that checks a bearer token from `Authorization` header against `os.getenv("API_KEY")`; inject it into every router.

---

## 2. Observability

**Status**: Would NOT hold up — when the service misbehaves, operators are completely blind.

| Check | Result |
|---|---|
| Structured logging at INFO for key operations | FAIL — no `import logging`, zero log statements |
| ERROR-level logging for caught exceptions | FAIL — HTTP errors are re-raised, never logged |
| Health-check endpoint (`/health`) | FAIL — no such route exists |
| Key metrics emitted | FAIL — no metrics instrumentation |

**Biggest risk**: A DB failure or silent 500-storm produces no signal — the only way to notice is a user complaint.

**Smallest next step**: Add `@app.get("/health") def health(): return {"status": "ok"}` and a single `logging.basicConfig(level=logging.INFO)` call at module top; log note ID on each write operation.

---

## 3. Deployment

**Status**: Would NOT hold up — the database path is CWD-relative and there is no container or env-var config.

| Check | Result |
|---|---|
| Starts cleanly from a single command | PASS — `uvicorn app:app` works |
| Graceful shutdown on SIGTERM | PASS — uvicorn handles SIGTERM by default |
| Config via environment variables | FAIL — `DB_PATH = "notes.db"` is hard-coded |
| Container / deployment manifest exists | FAIL — no Dockerfile, no Compose file |

**Biggest risk**: Two deployments launched from different working directories silently create separate databases, making data routing invisible.

**Smallest next step**: Replace `DB_PATH = "notes.db"` with `DB_PATH = os.getenv("NOTES_DB_PATH", "notes.db")` — one line, zero behaviour change locally, fully configurable in any deployment environment.

---

## 4. Runbooks

**Status**: Would NOT hold up — there is no operator documentation at all beyond a one-line docstring.

| Check | Result |
|---|---|
| README describes how to start the service | FAIL — module docstring has one uvicorn command; no README |
| Troubleshooting steps documented | FAIL — absent |
| Env-var reference documented | FAIL — absent (and there are no env vars yet) |
| Backup / restore procedure documented | FAIL — SQLite file is undocumented |

**Biggest risk**: A new on-call engineer has no guidance — they cannot start, configure, back up, or diagnose the service without reading source.

**Smallest next step**: Create `module-09/README.md` with four sections: Start, Stop, Environment variables, Backup (`cp notes.db notes.db.bak`).

---

## 5. Rollback

**Status**: Would NOT hold up — there is no migration system and no documented rollback procedure.

| Check | Result |
|---|---|
| Schema changes are versioned / migratable | FAIL — `CREATE TABLE IF NOT EXISTS` with no version tracking |
| Rollback to previous release is documented | FAIL — no procedure |
| Data backup before deploys is documented | FAIL — no procedure |
| Previous artefact is retained for re-deploy | N/A — no artefact store in scope |

**Biggest risk**: A schema change on the next feature requires manual SQL or a file-replace, with no safety net if it breaks.

**Smallest next step**: Document in the runbook: "Before any deploy, run `cp notes.db notes.db.$(date +%Y%m%d%H%M%S).bak`." That buys a rollback path at zero code cost.

---

## Summary

| Axis | Score |
|---|---|
| Security | FAIL |
| Observability | FAIL |
| Deployment | FAIL |
| Runbooks | FAIL |
| Rollback | FAIL |

**Verdict: No-Go.** Unauthenticated endpoints, zero logging, no health check, and no deployment config make this a dev prototype, not a shippable service.
