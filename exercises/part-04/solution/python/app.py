"""Notes API (FastAPI + Pydantic v2 + sqlite3 stdlib).

Run:
    uvicorn app:app --reload

Endpoints:
    POST   /notes       create
    GET    /notes?q=    list (optional substring search on title+body)
    GET    /notes/{id}  fetch
    PATCH  /notes/{id}  update
    DELETE /notes/{id}  delete
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DB_PATH = "notes.db"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _init_db() -> None:
    with sqlite3.connect(DB_PATH) as cx:
        cx.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT NOT NULL,
                body       TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    cx = sqlite3.connect(DB_PATH)
    cx.row_factory = sqlite3.Row
    try:
        yield cx
        cx.commit()
    finally:
        cx.close()


class NoteIn(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=0)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    body: str | None = None


class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: str
    updated_at: str


_init_db()
app = FastAPI(title="Notes API")


@app.post("/notes", response_model=Note, status_code=201)
def create_note(note: NoteIn) -> Note:
    now = _now()
    with _conn() as cx:
        cur = cx.execute(
            "INSERT INTO notes (title, body, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (note.title, note.body, now, now),
        )
        row = cx.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return Note(**dict(row))


@app.get("/notes", response_model=list[Note])
def list_notes(q: str | None = None) -> list[Note]:
    with _conn() as cx:
        if q:
            like = f"%{q}%"
            rows = cx.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY id",
                (like, like),
            ).fetchall()
        else:
            rows = cx.execute("SELECT * FROM notes ORDER BY id").fetchall()
    return [Note(**dict(r)) for r in rows]


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int) -> Note:
    with _conn() as cx:
        row = cx.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    return Note(**dict(row))


@app.patch("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, patch: NoteUpdate) -> Note:
    with _conn() as cx:
        row = cx.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="not found")
        title = patch.title if patch.title is not None else row["title"]
        body = patch.body if patch.body is not None else row["body"]
        cx.execute(
            "UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?",
            (title, body, _now(), note_id),
        )
        row = cx.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return Note(**dict(row))


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int) -> None:
    with _conn() as cx:
        cur = cx.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="not found")
