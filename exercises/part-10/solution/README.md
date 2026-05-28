# Reference solution — Module 10

> **Stop**: only open this after you have produced your own `readiness-report.md` against a prior module.

This module's deliverable is a **12-item production-readiness report**. The reference is a worked example against the Module 4 service.

```text
module-10/
└── readiness-report.md        # 12-item report + GO / NO-GO verdict
```

## Reference `readiness-report.md` (against Module 4 FastAPI service)

```markdown
# Production readiness — Module 4 service

Verdict: **NO-GO** (3 blockers).

| # | Item | Status | Evidence | Action if NOT |
|---|---|---|---|---|
| 1 | Secrets hygiene | ✓ | `.env` ignored; no keys in git history (`git log -p \| grep -iE 'api[_-]?key'`). | — |
| 2 | AuthN / AuthZ | ✗ | No auth on `/tasks` endpoints. | Add API-key middleware before public exposure. |
| 3 | Input validation | ✓ | Pydantic models reject empty `title`. | — |
| 4 | Error budgets | ✗ | No SLO defined. | Pick a 99.5% target for `/tasks`; alert on 5xx > 0.5%. |
| 5 | Idempotency | △ | `POST /tasks` not idempotent; client could double-submit. | Add `Idempotency-Key` header. |
| 6 | Observability | ✗ | No structured logs; no traces. | Add `structlog` + OTLP exporter. |
| 7 | Performance | ✓ | p95 < 50ms on 1k tasks (smoke). | — |
| 8 | Backwards compatibility | n/a | First release. | — |
| 9 | Disaster recovery | △ | SQLite file; no backup. | Document daily snapshot to S3. |
| 10 | Rollback | ✓ | Container image tagged per commit; previous tag re-deployable. | — |
| 11 | Permission scope | ✓ | Container runs as non-root UID 1000. | — |
| 12 | Human review | ✓ | This report counter-signed by senior eng. | — |
```

## How the `release-readiness` skill was used

The report was produced by invoking `skills/release-readiness/SKILL.md` with the Module 4 repo as input. The skill's "Outputs" section specifies the exact table shape above.

## Hooks that would have caught the blockers earlier

```json
{
  "hooks": {
    "pre_commit": [
      { "name": "no-secrets", "command": "gitleaks protect --staged" }
    ]
  }
}
```

A `pre_commit` hook running `gitleaks` would have prevented item #1 from ever needing to be on the checklist.

## Definition of done

- [ ] All 12 items addressed with a concrete status.
- [ ] Verdict line at the top: **GO** or **NO-GO** (with blocker count).
- [ ] At least one blocker mapped to an action item with an owner.
