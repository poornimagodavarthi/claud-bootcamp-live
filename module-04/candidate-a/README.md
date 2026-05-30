# Notes API (Track A)

FastAPI + Pydantic v2 + sqlite3, persisting to `notes.db` (schema initialised at startup).

    pip install "fastapi>=0.110" "uvicorn>=0.29" "pydantic>=2"
    uvicorn app:app --reload   # http://127.0.0.1:8000  (docs at /docs)
