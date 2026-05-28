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

## Code review rubric

There is **no reference** for `code-review-rubric.md` — it is your authored artefact and the module 5 deliverable. The instructor grades it against `assessments/rubric.md`'s "Code review reflection" criteria.

## Definition of done

See `../README.md`. The `code-review` skill output goes in `REVIEW.md`; at least **one applied fix** must be visible in the working diff.
