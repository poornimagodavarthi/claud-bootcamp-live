# Reference solution — Module 5

> **Stop**: only open this after you have produced your own `tests/`, `BUGS.md` fix, and `code-review-rubric.md`.

This module ships three artefacts:

```text
solution/
├── BUGS.md          # the planted-bug catalogue + reference fix for each
├── python/          # reference test suite (pytest)
└── node/            # reference test suite (vitest)
```

## What to compare

| Your artefact | Reference | Compare on |
|---|---|---|
| `tests/` | `python/tests/` or `node/tests/` | shape (≥6 tests, ≥3 happy, ≥2 error, ≥1 boundary), no SUT mocks |
| Bug fixes | `BUGS.md` | did you find both planted bugs? did your fix touch the minimum surface? |
| `code-review-rubric.md` | (you author this — there is no canonical version) | rubric has at least 6 items, each operational |

## Review checklist — what a real Haiku run got wrong

A live `GENERATE TESTS` run (Haiku, against the Module 4 `notes_api.py` winner)
produced a 498-line, 30-test suite that ran green — and still had three defects a
reviewer must catch. Use these as the "common AI deviations" for this module:

1. **Copied the SUT into the test file instead of importing it.** The suite opened
   with `# App setup (copied from notes_api.py)` and redefined `create_app()`,
   schemas, and every route inline. Consequence: the tests exercise a *frozen copy*
   — fix a bug in `notes_api.py` and the suite stays green, which defeats the whole
   point. **Fix:** `import notes_api`, patch `notes_api.DB_PATH` to a temp file,
   `TestClient(notes_api.app)`. (The reference fixture in `python/test_notes_api.py`
   shows the import-and-patch pattern.) **The kicker:** in the same run, the `SELF-REVIEW`
   prompt did *not* flag this — it described the copied app as "embedded for self-contained
   testing" (a feature!) and its ranked bug list named only trivia (an unused import, a
   theoretical timestamp race, a hard-coded `999`). The model will rationalise its own
   biggest mistake. That is the whole case for human review: AI self-review is a useful
   first pass, never the last word.
2. **404 tests assert only the status code, never the body.** `test_get_note_not_found_404`
   checks `status_code == 404` but not the JSON — so the Module 4
   `{"detail":{"error":"not found"}}` vs spec `{"error":"not found"}` mismatch is
   invisible. **Fix:** add `assert r.json() == {"error": "not found"}` to pin the contract.
3. **Imported but unused `unittest.mock.patch`** — despite the prompt saying "no mocks".
   Dead import; remove it. Cheap tell that the model pattern-matched a template.

A suite can be large, well-formatted, and fully green while testing the wrong thing.
That is exactly the lesson of Module 5: green is necessary, not sufficient — read the diff.

### Environment note

The reference run hit a broken system Python (3.14, `pyexpat` dylib mismatch), so
`pip install` failed. `uv` was the working path — no global install needed:

```bash
uv run --with pytest --with fastapi --with httpx pytest -q
```

## Code review rubric

There is **no reference** for `code-review-rubric.md` — it is your authored artefact and the module 5 deliverable. The instructor grades it against `assessments/rubric.md`'s "Code review reflection" criteria.

## Definition of done

See `../README.md`. The `code-review` skill output goes in `REVIEW.md`; at least **one applied fix** must be visible in the working diff.
