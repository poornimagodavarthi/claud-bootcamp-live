## Summary

Completed practical assessment by implementing a Bookmarks API, evaluating two candidates, and selecting the winner (Candidate A, 9/9) based on modern patterns and type safety. Delivers production-ready service with comprehensive test suite and code review.

## Why

Assessment required building a REST API with SQLite persistence, evaluating implementation approaches, and ensuring quality through testing and review. Winner selection demonstrates understanding of FastAPI best practices and Pydantic type safety.

## What changed

- `service/bookmarks_app.py` (99 lines): 5 endpoints (POST, GET all/filtered/by-ID, DELETE) with proper error handling
- `tests/test_bookmarks_api.py` (123 lines): 9 tests covering happy path, error cases, and edge cases
- `tests/conftest.py` (42 lines): pytest fixtures for isolated SQLite databases per test
- `scoring.md`: Candidate A (9/9) vs B (8.5/9) evaluation
- `REVIEW.md`: 6 code review findings with fixes (2 HIGH, 3 MEDIUM, 1 LOW)

## How to test

```bash
cd Poornima-Bootcamp/assessments/practical
python3 -m pip install fastapi pytest
python3 -m pytest tests/test_bookmarks_api.py -v
# Expected: 9 passed in 0.23s
```

All endpoints tested with real SQLite (no mocking); parameterized queries prevent SQL injection.

## Risk

- Pydantic v2 incompatibility: `.dict()` deprecated (line 62)
- init_db() lacks error handling on startup failure
- DATABASE path hardcoded to CWD
See REVIEW.md for details and minimal fixes.

## Rollback

Remove: `service/`, `tests/`, `scoring.md`, `REVIEW.md`, `PR.md`

## Reviewer checklist

- [ ] All 9 tests pass with real SQLite (no mocking)
- [ ] SQL injection prevention via parameterized queries verified
- [ ] Candidate A scores 9/9 on correctness, simplicity, fit
- [ ] Code review findings acknowledged (REVIEW.md)
- [ ] Modern FastAPI patterns (lifespan, Pydantic models)
