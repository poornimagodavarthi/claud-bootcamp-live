## Summary
Completed Bookmarks API assessment: implemented 5-endpoint REST service, evaluated 2 candidates (winner: A at 9/9), delivered 9-test suite with code review.

## Why
Demonstrates FastAPI best practices (lifespan, Pydantic models), SQLite integration, and ability to evaluate implementation approaches against a rubric.

## What changed
- `service/bookmarks_app.py`: 5 endpoints with error handling
- `tests/test_bookmarks_api.py`: 9 tests (3 happy, 2 error, 4 edge); no mocking
- `tests/conftest.py`: isolated SQLite per test
- `candidates.md`, `REVIEW.md`: evaluation & code review findings

## How to test
```bash
cd practical && pip install fastapi pytest
pytest tests/test_bookmarks_api.py -v
```

## Risk
Pydantic v2 incompatibility (`.dict()` deprecated); init_db() lacks error handling; hardcoded DATABASE path. See REVIEW.md.

## Rollback
Remove: `service/`, `tests/`, `candidates.md`, `REVIEW.md`

## Reviewer checklist
- [ ] 9 tests pass (real SQLite, no mocking)
- [ ] All 5 endpoints return correct status codes
- [ ] Candidate A justified (modern patterns + type safety)
- [ ] Code review findings documented
- [ ] SQL injection safe (parameterized queries)
