# Module 4 — Notes API (Best-of-N)

## Goal

Generate three independent candidate Notes APIs, score on the 3-criterion rubric, and ship the winner.

## Scenario

A small team needs a Notes service. You will use Best-of-N: produce 3 candidates, score, pick. The losers are evidence of the lift; keep them.

## Starter instructions

1. Pick a track:
   - **Track A — Python**: FastAPI + Pydantic v2 + sqlite3 stdlib.
   - **Track B — Node + TypeScript**: Hono + Zod + better-sqlite3.
2. Create `module-04/` and three subfolders: `candidate-a/`, `candidate-b/`, `candidate-c/`.
3. Open three **separate** Claude Code chats. Each chat = one candidate.

## Claude Code prompt to use

```text
GOAL
Build a small Notes API persisting to SQLite.

CONSTRAINTS
- Track A: Python 3.11 with FastAPI + Pydantic v2 + the sqlite3 stdlib module.
- Track B: TypeScript on Node 20 with Hono + Zod + better-sqlite3.
- One process. No migrations framework — initialise the schema at startup.
- HTTP status codes: 201 on create, 200 on read/update, 204 on delete, 404 on missing, 422 on invalid body.
- Timestamps in ISO 8601 UTC.

OUTPUT FORMAT
- A runnable project (single source file is fine) plus a 5-line README with the run command.

EXAMPLES
- POST /notes {"title":"a","body":"b"} → 201 {"id":1,"title":"a","body":"b","created_at":"...","updated_at":"..."}
- GET /notes?q=spec → 200 [matching notes]
- GET /notes/999 → 404 {"error":"not found"}
```

Then for each candidate, score using:

```text
Candidate: [a|b|c]
Correctness (0–3): can I exercise all five endpoints with curl?
Simplicity   (0–3): is the source single-glance readable?
Fit          (0–3): does it follow CLAUDE.md conventions?
Total: __ / 9
Notes:
```

## Manual validation steps

For each candidate, start the server and:

```bash
curl -X POST localhost:8000/notes -H 'content-type: application/json' \
  -d '{"title":"hi","body":"there"}'                  # 201
curl localhost:8000/notes                             # 200
curl 'localhost:8000/notes?q=hi'                      # 200
curl localhost:8000/notes/1                           # 200
curl -X PATCH localhost:8000/notes/1 -H 'content-type: application/json' \
  -d '{"body":"world"}'                               # 200
curl -X DELETE localhost:8000/notes/1                 # 204
curl localhost:8000/notes/999                         # 404
```

Adjust port to whatever the candidate chose.

## Expected deliverable

```text
module-04/
├── candidate-a/
├── candidate-b/
├── candidate-c/
├── scoring.md       # rubric scores + one paragraph per candidate
└── winner/          # exact copy of the winning candidate
```

A reference solution lives at `solution/` (Python and Node tracks) once the lab is complete.

## Definition of done

- [ ] All three candidates exist and were generated **independently** (separate chats).
- [ ] `scoring.md` has rubric scores and per-candidate justification.
- [ ] `winner/` runs end-to-end against the curl commands above.
- [ ] Losers archived, not deleted.

## Stretch challenge

Pick the *second-place* candidate. In `module-04/runner-up-notes.md`, write the smallest patch that would have made it the winner.

## Troubleshooting

| Symptom | Fix |
|---|---|
| All three candidates feel the same | Use *separate* chats — same chat = iteration, not BoN. |
| Tied scores | Tie-breaker: simpler source wins. |
| Track B: better-sqlite3 native build fails | Ensure Node 20 LTS, not 21+; on macOS `xcode-select --install`. |
| Track A: Pydantic v1 imports | Re-prompt with "Pydantic v2" reinforced. |
