# 04. Best-of-N

Module 04 · 30 min

## Build Faster with Best-of-N

**The first answer is rarely the best. Generate three; score; ship the winner.**

### Theory · Best-of-N (4 min)

> **Generate N independent candidates → score on a rubric → pick the winner.** N = 3 is the sweet spot.

- **Independent** — each candidate gets its own fresh prompt context. *Not* "now improve it" (that's iteration).
- **Score on a rubric**, not vibes. Three criteria:
  - **Correctness** — passes the manual test plan?
  - **Simplicity** — could a junior maintain it?
  - **Fit** — matches `CLAUDE.md` conventions and repo style?

**Without the rubric you pick by gut and the lift disappears. Correctness gates everything.**

### Best-of-N, scored

![Best-of-N: generate N candidates, score on Correctness, Simplicity, Fit, pick the winner](resources/04-bon-scoring.png)

Generate **N** independent candidates → score on **Correctness · Simplicity · Fit** → keep the winner.

### Reference · The 3-criterion scorecard

| Criterion | Question | Weight |
|---|---|---|
| **Correctness** | Does it pass every step of the manual test plan? | Gate — fail here = out |
| **Simplicity** | Could a junior maintain it next quarter? | High |
| **Fit** | Does it follow `CLAUDE.md` + repo style? | Medium |

Record a one-paragraph justification per candidate in `scoring.md`. **Never delete losers before scoring.**

### Reference · Common mistakes

- One candidate + "improve it" ×3 (iteration, not BoN).
- Skipping the rubric → picking by vibe → no lift.
- Choosing the "elegant" one that fails the test plan (correctness is the gate).

### Live demo · Three candidates, one winner (6 min)

**The reusable prompt — paste it verbatim for A, B, and C:**

```text
GOAL: A REST Notes API: create, list, get, delete a note.
CONSTRAINTS: Python 3.11 + FastAPI; persist to SQLite ./notes.db;
  return JSON; 404 on missing id; no other third-party deps.
OUTPUT: one runnable app + a curl test plan covering all 4 routes.
EXAMPLES: POST /notes {"text":"hi"} -> 201 + id;
  GET /notes/999 (missing) -> 404 {"error":"not found"}.
```

`/clear` before **each** candidate → paste the **same** prompt → save to `candidate-a|b|c/`. Then score side-by-side and commit the winner.

> Variance must come from the model, **not** the prompt. Never say "now do it differently."

### Your turn · Notes API, Best-of-3 (13 min)

**Exercise**: [`exercises/part-04/README.md`](#hands-on-exercise--module-04)

Build a Notes API (SQLite `notes.db`), then generate **3 candidates** and score them:

```text
POST /notes · GET /notes?q= · GET /notes/:id · PATCH /notes/:id · DELETE /notes/:id
Status: 201 create · 200 read/update · 204 delete · 404 missing · 422 invalid
```

Track A: Python (FastAPI + Pydantic v2). Track B: Node (Hono + Zod + better-sqlite3).

**Deliverables**: `candidate-{a,b,c}/`, `scoring.md` (scores + justification), `winner/` (clean copy).

**Success signal**: all five endpoints respond with correct status codes via curl.

### Done & next (1 min)

**Definition of done**

- [ ] Three candidates in `module-04/candidate-{a,b,c}/`.
- [ ] `scoring.md` with scores + one-paragraph justification each.
- [ ] `winner/` runs end-to-end; losers archived (not deleted).

**Next** — we trust the winner only after we *test* it and review like a stranger's PR.
**Module 5 — Testing, Debugging & Self-Review.**

## Hands-on exercise — Module 04 {#hands-on-exercise--module-04}

> **Companion repository** — Work this exercise from the live files in the [Claude Code Bootcamp repository](https://github.com/lucab85/Claude-Code-Bootcamp): [`exercises/part-04/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-04/README.md).
> Reference solution: [`exercises/part-04/solution/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-04/solution/README.md).

## Module 4 — Notes API (Best-of-N)

### Goal

Generate three independent candidate Notes APIs, score on the 3-criterion rubric, and ship the winner.

### Scenario

A small team needs a Notes service. You will use Best-of-N: produce 3 candidates, score, pick. The losers are evidence of the lift; keep them.

### Starter instructions

1. Pick a track:
   - **Track A — Python**: FastAPI + Pydantic v2 + sqlite3 stdlib.
   - **Track B — Node + TypeScript**: Hono + Zod + better-sqlite3.
2. Create `module-04/` and three subfolders: `candidate-a/`, `candidate-b/`, `candidate-c/`.
3. Open three **separate** Claude Code chats. Each chat = one candidate.

### Claude Code prompt to use

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

### Manual validation steps

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

### Expected deliverable

```text
module-04/
├── candidate-a/
├── candidate-b/
├── candidate-c/
├── scoring.md       # rubric scores + one paragraph per candidate
└── winner/          # exact copy of the winning candidate
```

A reference solution lives at `solution/` (Python and Node tracks) once the lab is complete.

### Definition of done

- [ ] All three candidates exist and were generated **independently** (separate chats).
- [ ] `scoring.md` has rubric scores and per-candidate justification.
- [ ] `winner/` runs end-to-end against the curl commands above.
- [ ] Losers archived, not deleted.

### Stretch challenge

Pick the *second-place* candidate. In `module-04/runner-up-notes.md`, write the smallest patch that would have made it the winner.

### Troubleshooting

| Symptom | Fix |
|---|---|
| All three candidates feel the same | Use *separate* chats — same chat = iteration, not BoN. |
| Tied scores | Tie-breaker: simpler source wins. |
| Track B: better-sqlite3 native build fails | Ensure Node 20 LTS, not 21+; on macOS `xcode-select --install`. |
| Track A: Pydantic v1 imports | Re-prompt with "Pydantic v2" reinforced. |

## Solution — Module 04 {#solution--module-04}

## Reference solution — Module 4

> **Stop**: only open this after you have produced your own `candidates.md` and chosen a winner.

Two parallel tracks ship under this directory. Pick the one matching your stack and diff your work against it:

| Track | Path | Run |
|---|---|---|
| Python (FastAPI + SQLite) | `python/` | `pip install -r python/requirements.txt && uvicorn python.app:app --reload` |
| Node.js (Hono + better-sqlite3) | `node/` | `cd node && npm i && npm start` |

### What to compare in `candidates.md`

The reference run produced **two candidates**: one with the route layer split out and one with everything in `app.py`. The winner (the split version) was picked against the 3-criterion rubric:

| Criterion | Weight | Why split version won |
|---|---|---|
| Correctness | 0.4 | Both pass the smoke script; tied. |
| Maintainability | 0.4 | Split version isolates persistence from routing → easier tests. |
| Speed-to-ship | 0.2 | Single-file version was 12 lines shorter; minor win. |

If your `candidates.md` doesn't articulate the trade-off this concretely, refine the rationale before submitting.

### Definition of done

See `../README.md`. Note: at least **two distinct candidates** are required — variants of the same approach don't count.
