# Notes API — Candidate A (Python + FastAPI)

## Run

```sh
pip install fastapi uvicorn pydantic
uvicorn app:app --reload
```

API is available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/notes` | Create a note (`{"title":"...","body":"..."}`) → 201 |
| `GET` | `/notes?q=<term>` | List all notes, optionally filtered by search term → 200 |
| `GET` | `/notes/{id}` | Fetch a single note → 200 / 404 |
| `PATCH` | `/notes/{id}` | Update title and/or body → 200 / 404 |
| `DELETE` | `/notes/{id}` | Delete a note → 204 / 404 |
