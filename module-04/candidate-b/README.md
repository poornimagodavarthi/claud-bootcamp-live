# Notes API — Candidate B (Python + FastAPI)

Single-file Notes API on FastAPI + Pydantic v2, persisting to `notes.db` (sqlite3, stdlib). Schema is created at startup.

## Run

```sh
pip install fastapi "uvicorn[standard]"
uvicorn app:app --reload   # http://localhost:8000
```
