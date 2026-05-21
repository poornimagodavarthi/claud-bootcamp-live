# Practical Task — Mini-Build (Graded)

> Worth **40%** of the final score. Time-box: **45 minutes** (do this after the live workshop, before submitting your zip).
> Graded against [`rubric.md`](rubric.md).

## Scenario

A peer hands you this two-line ask:

> "We need a tiny **Bookmarks API**. I need to save URLs with a title and tag, list them, search by tag, and delete. Use whatever stack you used for Notes."

You will deliver a runnable service plus the artefacts that prove you operated like a Tech Lead, not a code generator.

## What you will deliver

```text
assessments/practical/
├── service/             # the runnable service
├── PROMPT.md            # the GCOE prompt you used
├── candidates.md        # short notes on the 2 candidates you generated and which you picked
├── tests/               # at least 6 tests (3 happy, 2 error, 1 boundary)
├── REVIEW.md            # one-page output of `skills/code-review/SKILL.md` against your service
└── PR.md                # ≤ 40-line PR description from `skills/git-workflow/SKILL.md`
```

## Functional contract

The Bookmarks API exposes:

| Method | Path | Purpose |
|---|---|---|
| POST | `/bookmarks` | create `{url, title, tag}` |
| GET | `/bookmarks` | list all |
| GET | `/bookmarks?tag=<t>` | filter by tag (exact match) |
| GET | `/bookmarks/:id` | fetch one or 404 |
| DELETE | `/bookmarks/:id` | delete or 404 |

Persistence: SQLite. Track: same as your Module 4 winner (Python + FastAPI **or** Node + Hono).

## Process you must follow (graded)

1. **Plan.** Author `PROMPT.md` in GCOE form before writing any code.
2. **Best-of-2.** Open two independent chats, generate two candidates with the same prompt, pick a winner. Document in `candidates.md`.
3. **Tests.** Generate the suite using `skills/test-generation/SKILL.md`. Suite is green.
4. **Review.** Run `skills/code-review/SKILL.md` against the winner; capture the output in `REVIEW.md` and apply at least one fix.
5. **Ship.** Compose a PR description using `skills/git-workflow/SKILL.md`.

## Manual validation (for the grader)

```bash
cd assessments/practical/service
# Track A
uvicorn app:app --reload &
# Track B
npm run dev &

# Smoke
curl -X POST localhost:8000/bookmarks -H 'content-type: application/json' \
  -d '{"url":"https://example.com","title":"ex","tag":"misc"}'   # 201
curl localhost:8000/bookmarks                                    # 200
curl 'localhost:8000/bookmarks?tag=misc'                         # 200
curl localhost:8000/bookmarks/1                                  # 200
curl -X DELETE localhost:8000/bookmarks/1                        # 204
curl localhost:8000/bookmarks/99                                 # 404

# Tests
pytest -q     # or: npm test
```

All commands must exit 0 / show expected status.

## Definition of done

- [ ] `service/` runs with one command and passes the smoke script.
- [ ] `tests/` has ≥ 6 tests, all green.
- [ ] `PROMPT.md` follows GCOE.
- [ ] `candidates.md` shows two candidates and a justified pick.
- [ ] `REVIEW.md` captures `code-review` skill output **and** at least one applied fix.
- [ ] `PR.md` ≤ 40 lines with all six required sections.

## Anti-patterns (graded down)

- Skipping `PROMPT.md` and just regurgitating Claude's first reply.
- Fewer than two candidates.
- Tests that mock the SUT itself.
- `PR.md` that says *what* but not *why*.
