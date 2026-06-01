# GCOE Prompt: Bookmarks API

## Goal
Build a lightweight Bookmarks API using Python, FastAPI, and SQLite. The service should allow users to save, list, filter, and delete bookmarks.

## Context
1. **Stack:** Python 3.x, FastAPI, and `sqlite3` (standard library).
2. **Persistence:** Use a local SQLite database file named `bookmarks.db`.
3. **Endpoints:**
   - `POST /bookmarks`: Accept `{url, title, tag}`. Return 201 Created with the new bookmark.
   - `GET /bookmarks`: Return all bookmarks.
   - `GET /bookmarks?tag=<t>`: Return bookmarks filtered by an exact tag match.
   - `GET /bookmarks/{id}`: Return a single bookmark or a 404 error if missing.
   - `DELETE /bookmarks/{id}`: Delete the bookmark and return 204 No Content, or a 404 error if missing.
4. **Implementation:** Keep the logic in a single file named `bookmarks_app.py`.
5. **Robustness:** Ensure proper error handling for missing resources (404s) and database connection management.

## Output
A single, runnable `bookmarks_app.py` file containing the FastAPI application and SQLite integration.

## Examples
- `POST /bookmarks` data: `{"url": "https://python.org", "title": "Python Official", "tag": "coding"}`
- `GET /bookmarks?tag=coding` should return only items with the "coding" tag.
