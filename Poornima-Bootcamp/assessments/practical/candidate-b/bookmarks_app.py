import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel

DB_FILE = "bookmarks.db"

app = FastAPI(title="Bookmarks API")


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bookmarks (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                url   TEXT NOT NULL,
                title TEXT NOT NULL,
                tag   TEXT NOT NULL
            )
            """
        )


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


class BookmarkIn(BaseModel):
    url: str
    title: str
    tag: str


@app.on_event("startup")
def startup():
    init_db()


@app.post("/bookmarks", status_code=201)
def create_bookmark(payload: BookmarkIn) -> dict:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO bookmarks (url, title, tag) VALUES (?, ?, ?)",
            (payload.url, payload.title, payload.tag),
        )
        row = conn.execute(
            "SELECT * FROM bookmarks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return row_to_dict(row)


@app.get("/bookmarks")
def list_bookmarks(tag: Optional[str] = Query(default=None)) -> list[dict]:
    with get_conn() as conn:
        if tag is not None:
            rows = conn.execute(
                "SELECT * FROM bookmarks WHERE tag = ?", (tag,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM bookmarks").fetchall()
    return [row_to_dict(r) for r in rows]


@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM bookmarks WHERE id = ?", (bookmark_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return row_to_dict(row)


@app.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int) -> Response:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM bookmarks WHERE id = ?", (bookmark_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Bookmark not found")
        conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
    return Response(status_code=204)
