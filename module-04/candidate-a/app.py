"""Notes API — FastAPI + Pydantic v2 + sqlite3 (stdlib), persisting to SQLite.

Single process, schema initialised at startup. Run with:
    uvicorn app:app --reload
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

DB_PATH = "notes.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)


class NoteIn(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class Note(NoteIn):
    id: int
    created_at: str
    updated_at: str


app = FastAPI(title="Notes API")


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


def _row_to_note(row: sqlite3.Row) -> Note:
    return Note(**dict(row))


@app.post("/notes", response_model=Note, status_code=201)
def create_note(note: NoteIn) -> Note:
    ts = now_iso()
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO notes (title, body, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (note.title, note.body, ts, ts),
        )
        row = conn.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return _row_to_note(row)


@app.get("/notes", response_model=list[Note])
def list_notes(q: str | None = Query(default=None)) -> list[Note]:
    with get_conn() as conn:
        if q:
            like = f"%{q}%"
            rows = conn.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY id",
                (like, like),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM notes ORDER BY id").fetchall()
    return [_row_to_note(r) for r in rows]


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int) -> Note:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    return _row_to_note(row)


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteIn) -> Note:
    ts = now_iso()
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?",
            (note.title, note.body, ts, note_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="not found")
        row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return _row_to_note(row)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int) -> None:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="not found")
