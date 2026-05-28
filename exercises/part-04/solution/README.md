# Reference solution — Module 4

> **Stop**: only open this after you have produced your own `candidates.md` and chosen a winner.

Two parallel tracks ship under this directory. Pick the one matching your stack and diff your work against it:

| Track | Path | Run |
|---|---|---|
| Python (FastAPI + SQLite) | [`python/`](python/) | `pip install -r python/requirements.txt && uvicorn python.app:app --reload` |
| Node.js (Hono + better-sqlite3) | [`node/`](node/) | `cd node && npm i && npm start` |

## What to compare in `candidates.md`

The reference run produced **two candidates**: one with the route layer split out and one with everything in `app.py`. The winner (the split version) was picked against the 3-criterion rubric:

| Criterion | Weight | Why split version won |
|---|---|---|
| Correctness | 0.4 | Both pass the smoke script; tied. |
| Maintainability | 0.4 | Split version isolates persistence from routing → easier tests. |
| Speed-to-ship | 0.2 | Single-file version was 12 lines shorter; minor win. |

If your `candidates.md` doesn't articulate the trade-off this concretely, refine the rationale before submitting.

## Definition of done

See `../README.md`. Note: at least **two distinct candidates** are required — variants of the same approach don't count.
