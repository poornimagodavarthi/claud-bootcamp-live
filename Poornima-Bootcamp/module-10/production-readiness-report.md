# Production Readiness Report — Notes API

**Target**: `Poornima-Bootcamp/module-09/notes_api.py` (FastAPI + SQLite, single file)
**Date**: 2026-05-30
**Reviewer**: Claude Code (production-readiness-review skill)

---

## 1. Security

**This week?** No — every route is unauthenticated, so any network-reachable client can read, write, and delete all notes.

**Biggest risk**: Zero auth/authz on every endpoint — total data exposure and tampering.

**Smallest next step**: Add one FastAPI dependency that checks a bearer token against `os.getenv("API_KEY")` and apply it to all routes.

## 2. Observability

**This week?** No — there is no logging, no `/health` route, and no metrics, so operators are blind when it misbehaves.

**Biggest risk**: A DB failure or 500-storm emits no signal — you learn about outages from users.

**Smallest next step**: Add `@app.get("/health")` returning `{"status":"ok"}` (enables liveness probes) and a top-level `logging.basicConfig(level=INFO)`.

## 3. Deployment

**This week?** No — it only starts via a dev command, the DB path is hard-coded to CWD, and there is no container or env config.

**Biggest risk**: The CWD-relative `notes.db` is ephemeral and single-node — restarts/scaling silently fork or lose data.

**Smallest next step**: `DB_PATH = os.getenv("NOTES_DB_PATH", "notes.db")` — one line, configurable in any environment.

## 4. Runbooks

**This week?** No — there is no operator documentation for deploying, configuring, or recovering the service.

**Biggest risk**: On-call has no guidance to start, back up, or diagnose it — slow, error-prone incident response.

**Smallest next step**: Add `module-09/README.md` with four sections: Start, Environment variables, Health check, Backup/Restore.

## 5. Rollback

**This week?** Partial — code rollback via git is trivial, but there is no DB backup or migration/versioning safety net.

**Biggest risk**: A bad data or schema change can't be cleanly reverted — no backup, no migration history.

**Smallest next step**: Make pre-deploy a backup step: `cp notes.db notes.db.$(date +%Y%m%d%H%M%S).bak`.

---

**Verdict — No-Go.** Every endpoint is unauthenticated, there's no logging or health check, and the DB path is hard-coded — a working prototype, not a production service.

> Note: `notes_api.py` has been aligned to the Module-4 winner (lifespan startup, PATCH-only partial update, strip-based validation). The findings above hold for the winner unchanged, and the module-09 smoke hook still passes 6/6.
