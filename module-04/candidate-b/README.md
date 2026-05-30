# Notes API

A simple REST API for managing notes, built with FastAPI, Pydantic v2, and SQLite.

## Setup & Run

```bash
pip install -r requirements.txt
python3 app.py
```

The API runs on `http://localhost:3000`. Persist to SQLite is automatic (`notes.db`).

## Endpoints

- `POST /notes` — Create note (201)
- `GET /notes?q=<search>` — List notes (200)
- `GET /notes/:id` — Get note (200 or 404)
- `PUT /notes/:id` — Update note (200 or 404)
- `DELETE /notes/:id` — Delete note (204 or 404)
