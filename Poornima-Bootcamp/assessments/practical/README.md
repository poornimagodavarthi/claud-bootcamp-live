# Bookmarks API — Practical Assessment

## Quick Start

### Run the API
```bash
cd service
python3 -m pip install fastapi uvicorn
python3 bookmarks_app.py
```

Server starts on `http://0.0.0.0:8000`

### Run Tests
```bash
python3 -m pip install pytest
pytest tests/test_bookmarks_api.py -v
```

Expected: **9/9 tests passing**

## API Endpoints

| Method | Endpoint | Status | Notes |
|--------|----------|--------|-------|
| POST | `/bookmarks` | 201 | Create bookmark |
| GET | `/bookmarks` | 200 | List all |
| GET | `/bookmarks?tag=<t>` | 200 | Filter by tag |
| GET | `/bookmarks/{id}` | 200 / 404 | Get one |
| DELETE | `/bookmarks/{id}` | 204 / 404 | Delete |

## Test Commands

```bash
# Create
curl -X POST http://localhost:8000/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"url": "https://python.org", "title": "Python", "tag": "coding"}'

# List all
curl http://localhost:8000/bookmarks

# Filter by tag
curl "http://localhost:8000/bookmarks?tag=coding"

# Get one
curl http://localhost:8000/bookmarks/1

# Delete
curl -X DELETE http://localhost:8000/bookmarks/1
```

## Files

- **`service/bookmarks_app.py`** — FastAPI service (5 endpoints, SQLite)
- **`tests/`** — 9 tests (conftest + test suite; no mocking)
- **`candidates.md`** — Evaluation of 2 candidates (A: 9/9 winner vs B: 8.5/9)
- **`PROMPT.md`** — GCOE prompt (Goal, Context, Output, Examples)
- **`REVIEW.md`** — Code review findings (6 items with fixes)
- **`PR.md`** — Pull request body (Summary, Why, What, How, Risk, Rollback, Checklist)
- **`scoring.md`** — Detailed rubric scoring for both candidates

## Assessment Status

✅ All 5 endpoints working  
✅ 9/9 tests passing (no mocking, real SQLite)  
✅ Candidate evaluation complete (A wins 9/9)  
✅ Code review with findings documented  
✅ PR-ready with proper format  

See `scoring.md` and `candidates.md` for detailed evaluation.
