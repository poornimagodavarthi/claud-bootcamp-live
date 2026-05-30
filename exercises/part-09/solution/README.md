# Reference solution — Module 9

> **Stop**: only open this after you have authored your own `notes-api-smoke` skill, wired the hook, and run the MCP action.

This module's deliverable is a **runnable bundle** built around the Notes API from Module 4:

```text
module-09/
├── notes_api.py                    # carried over from Module 4 (system under test)
├── skill/
│   └── SKILL.md                    # notes-api-smoke — runnable worked example
├── .claude/
│   └── hooks.json                  # pre-commit hook that runs the skill
├── invocation.md                   # real PASS/FAIL output
├── hook-fired.md                   # proof the hook blocked a broken commit
├── mcp-run.md                      # 5-line brief + real issue URL / dry-run call
└── multi-agent-compare.md          # stretch — fan-out comparison
```

## Reference `SKILL.md` (skeleton — your Body must be project-agnostic)

```markdown
---
name: notes-api-smoke
description: Boot a single-file FastAPI notes app and assert its 5 CRUD endpoints plus the 404 probe, printing PASS/FAIL per check.
---

## Purpose
Verify a notes API is wired correctly in one command, so a teammate can trust
it before building on top.

## When to use
Before committing changes to a notes-style CRUD API, or in a pre-commit hook.

## Body
1. Boot the app under test on the given port.
2. POST a note → expect 201; capture the id.
3. GET /notes and GET /notes/{id} → expect 200.
4. PATCH /notes/{id} → expect 200.
5. DELETE /notes/{id} → expect 204.
6. GET /notes/999 → expect 404.
7. Print `PASS <check>` or `FAIL <check>` per step; exit non-zero on any FAIL.

## Inputs
- module_path: path to the app module (default `notes_api.py`).
- port: free TCP port (default 8099).

## Outputs
- One `PASS`/`FAIL` line per check, then a final `RESULT: PASS|FAIL`.

## Worked example
```bash
PORT=8099
uv run --with fastapi --with uvicorn uvicorn notes_api:app --port "$PORT" &
SRV=$!; sleep 2
fail=0
code=$(curl -s -o /tmp/n.json -w '%{http_code}' -X POST localhost:$PORT/notes \
  -H 'content-type: application/json' -d '{"title":"a","body":"b"}')
[ "$code" = 201 ] && echo "PASS create" || { echo "FAIL create ($code)"; fail=1; }
id=$(sed -n 's/.*"id":\([0-9]*\).*/\1/p' /tmp/n.json)
[ "$(curl -s -o /dev/null -w '%{http_code}' localhost:$PORT/notes)" = 200 ] \
  && echo "PASS list" || { echo "FAIL list"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' localhost:$PORT/notes/$id)" = 200 ] \
  && echo "PASS get" || { echo "FAIL get"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' -X PATCH localhost:$PORT/notes/$id \
  -H 'content-type: application/json' -d '{"title":"z"}')" = 200 ] \
  && echo "PASS patch" || { echo "FAIL patch"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE localhost:$PORT/notes/$id)" = 204 ] \
  && echo "PASS delete" || { echo "FAIL delete"; fail=1; }
[ "$(curl -s -o /dev/null -w '%{http_code}' localhost:$PORT/notes/999)" = 404 ] \
  && echo "PASS 404" || { echo "FAIL 404"; fail=1; }
kill $SRV
[ "$fail" = 0 ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }
```
```

## Reference `.claude/hooks.json`

```json
{
  "hooks": {
    "pre_commit": [
      {
        "name": "notes-api-smoke",
        "command": "uv run --with fastapi --with uvicorn bash skill/run.sh notes_api.py 8099"
      }
    ]
  }
}
```

The hook **must exit non-zero on FAIL** — that is what blocks the commit. A hook
that only echoes a warning is not a guardrail.

## Reference `hook-fired.md` (what proof looks like)

```text
$ git commit -m "wip"
FAIL list (500)
RESULT: FAIL
husky/pre-commit: hook exited with code 1 — commit aborted
$ git checkout -- notes_api.py    # reverted the injected bug
```

## Reference `mcp-run.md` (5-line brief + result)

```markdown
Task: file the smoke-test result as a GitHub issue.
Server: github (scope: repo acme/notes only).
Allowed: open ONE issue. Forbidden: everything else (no merges, no other repos).
Stop: when the issue is created (capture URL).

Result: opened https://github.com/acme/notes/issues/42
  title: "notes-api-smoke: PASS on 2026-05-30"
# If no MCP server is configured, record the dry-run instead:
# would call: github.create_issue(repo="acme/notes",
#   title="notes-api-smoke: PASS on 2026-05-30", body=<skill output>)
```

## Multi-agent fan-out (stretch)

The reference comparison smoke-tested **three candidate APIs**:
1. Single agent runs the skill against all three in sequence.
2. Lead + 2 workers — each worker tests one candidate, lead picks the winner.
3. Two `git worktree`-isolated agents on competing fixes.

The takeaway captured in `multi-agent-compare.md`: fan-out helps when the checks are
**independent per candidate**; it hurts when the agents must agree on a single shared
verdict and end up re-litigating each other's output.

## Definition of done

See `../README.md`.
