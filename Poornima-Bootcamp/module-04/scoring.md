# scoring.md — Module 4 Best-of-N

Two candidates for the same Notes API prompt (FastAPI + Pydantic v2 + sqlite3),
each run through the same curl smoke test. Scored against the stricter course
smoke test from `exercises/part-04/solution/scoring.example.md` (adds a blank-title
`"   "` case and a `PATCH` partial-update case on top of the base spec).

## Smoke-test results

| Smoke case | Spec wants | Candidate A | Candidate B |
|---|---|---|---|
| POST create | 201 | 201 PASS | 201 PASS |
| Blank title `"   "` | 422 | 422 PASS | 422 PASS |
| GET list | 200 | 200 PASS | 200 PASS |
| PATCH partial | 200 | 200 PASS | 200 PASS |
| DELETE | 204 | 204 PASS | 204 PASS |
| 404 body | `{"error":"not found"}` | `{"detail":"not found"}` PARTIAL | `{"error":"not found"}` PASS |

## Per-candidate scores

```text
Candidate: a
Correctness (0–3): 3   all 6 codes match spec (201/422/200/200/204/404)
Simplicity   (0–3): 3   single file, PATCH + validator helpers, one glance
Fit          (0–3): 2   wrapped 404 body {"detail":...}; timestamp via strftime,
                        not the prescribed isoformat(timespec="seconds")
Total: 8 / 9
Notes: Modern lifespan handler, partial PATCH, blank-title 422. Loses a point on
       the wrapped 404 envelope vs the spec's bare {"error":"not found"}.
```

```text
Candidate: b
Correctness (0–3): 3   all 6 codes match spec, including exact 404 body
Simplicity   (0–3): 3   single file, separate NoteCreate/NoteUpdate, clear helpers
Fit          (0–3): 3   {"error":"not found"} 404, isoformat(timespec="seconds")
                        timestamps, modern str|None hints, 5-line README present
Total: 9 / 9
Notes: Matches every smoke case outright. The only axis that separates the two —
       the 404 body — goes to B. Same forced third-party FastAPI dep as A.
```

## Decision

**Winner: Candidate B (9 / 9 vs 8 / 9).**

Both candidates now satisfy the full smoke test (POST/blank-title/GET/PATCH/DELETE),
so correctness and simplicity tie. The deciding axis is the **404 body**: B returns
the spec's bare `{"error":"not found"}`, while A wraps it as `{"detail":"not found"}`.
B also matches the house timestamp convention (`isoformat(timespec="seconds")`)
where A uses `strftime`.

Candidate A is kept as evidence: same prompt, but it shipped the wrapped 404
envelope and a non-prescribed timestamp format — small misses that Best-of-N exists
to surface.

The winning source should be copied verbatim into `winner/`.
```text
History: candidate B originally implemented PUT (full replace) and used
Field(min_length=1), which accepted whitespace-only titles. It was corrected to a
PATCH partial update with a strip-based blank-title validator to pass the stricter
course smoke test.
```
