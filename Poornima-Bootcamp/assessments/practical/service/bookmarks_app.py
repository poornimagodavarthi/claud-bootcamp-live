from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager, contextmanager
from typing import Optional
import sqlite3

DATABASE = "bookmarks.db"


class BookmarkCreate(BaseModel):
    url: str
    title: str
    tag: str


class Bookmark(BookmarkCreate):
    id: int


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
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                tag TEXT NOT NULL
            )
        """)
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/bookmarks", status_code=201, response_model=Bookmark)
def create_bookmark(bookmark: BookmarkCreate):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO bookmarks (url, title, tag) VALUES (?, ?, ?)",
            (bookmark.url, bookmark.title, bookmark.tag)
        )
        conn.commit()
        bookmark_id = cursor.lastrowid

    return {"id": bookmark_id, **bookmark.dict()}


@app.get("/bookmarks", response_model=list[Bookmark])
def list_bookmarks(tag: Optional[str] = None):
    with get_db() as conn:
        if tag:
            rows = conn.execute(
                "SELECT id, url, title, tag FROM bookmarks WHERE tag = ?", (tag,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT id, url, title, tag FROM bookmarks").fetchall()

    return [dict(row) for row in rows]


@app.get("/bookmarks/{bookmark_id}", response_model=Bookmark)
def get_bookmark(bookmark_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, url, title, tag FROM bookmarks WHERE id = ?", (bookmark_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    return dict(row)


@app.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bookmark not found")
