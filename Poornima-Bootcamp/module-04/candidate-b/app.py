"""Notes API — FastAPI + Pydantic v2 + sqlite3 (stdlib).

Single-process, single-file. Schema is initialised at startup; no migration
framework. Persists to notes.db in the current working directory.
"""

from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

DB_PATH = "notes.db"


def now_iso() -> str:
    """Current time as ISO 8601 in UTC, second precision."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema() -> None:
    with connect() as conn:
        conn.execute(
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_schema()
    yield


app = FastAPI(title="Notes API", lifespan=lifespan)


class NoteCreate(BaseModel):
    title: str
    body: str

    @field_validator("title", "body")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v


class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None

    @field_validator("title", "body")
    @classmethod
    def not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("must not be blank")
        return v


class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: str
    updated_at: str


def row_to_note(row: sqlite3.Row) -> Note:
    return Note(**dict(row))


def not_found() -> JSONResponse:
    return JSONResponse(status_code=404, content={"error": "not found"})


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
    ts = now_iso()
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO notes (title, body, created_at, updated_at) "
            "VALUES (?, ?, ?, ?)",
            (note.title, note.body, ts, ts),
        )
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return row_to_note(row)


@app.get("/notes")
def list_notes(q: str | None = Query(default=None)) -> list[Note]:
    with connect() as conn:
        if q:
            like = f"%{q}%"
            rows = conn.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? "
                "ORDER BY id",
                (like, like),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM notes ORDER BY id").fetchall()
    return [row_to_note(r) for r in rows]


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
    if row is None:
        return not_found()
    return row_to_note(row)


@app.patch("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
        if row is None:
            return not_found()
        current = dict(row)
        title = note.title if note.title is not None else current["title"]
        body = note.body if note.body is not None else current["body"]
        ts = now_iso()
        conn.execute(
            "UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?",
            (title, body, ts, note_id),
        )
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
    return row_to_note(row)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    with connect() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        if cur.rowcount == 0:
            return not_found()
    return None
