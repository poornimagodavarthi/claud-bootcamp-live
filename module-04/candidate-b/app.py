import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from uvicorn import run


DATABASE = "notes.db"


class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: str
    updated_at: str


@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()


def get_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def row_to_note(row: sqlite3.Row) -> Note:
    return Note(
        id=row["id"],
        title=row["title"],
        body=row["body"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/notes", response_model=list[Note])
def list_notes(q: str | None = Query(None)):
    with get_db() as conn:
        if q:
            rows = conn.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY created_at DESC",
                (f"%{q}%", f"%{q}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM notes ORDER BY created_at DESC"
            ).fetchall()
        return [row_to_note(row) for row in rows]


@app.post("/notes", response_model=Note, status_code=201)
def create_note(data: NoteCreate):
    now = get_now()
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO notes (title, body, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (data.title, data.body, now, now),
        )
        conn.commit()
        note_id = cursor.lastrowid
    return Note(
        id=note_id,
        title=data.title,
        body=data.body,
        created_at=now,
        updated_at=now,
    )


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="not found")
    return row_to_note(row)


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, data: NoteCreate):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="not found")

        now = get_now()
        conn.execute(
            "UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?",
            (data.title, data.body, now, note_id),
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
    return row_to_note(row)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="not found")

        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=3000)
