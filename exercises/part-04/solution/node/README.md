# Module 4 — Node + TypeScript Reference Solution

Notes API on Hono + Zod + better-sqlite3.

## Install

```bash
npm install
```

## Run

```bash
npm run dev
```

Server listens on `http://localhost:8000`.

## Smoke test

```bash
curl -X POST localhost:8000/notes -H 'content-type: application/json' \
  -d '{"title":"hi","body":"there"}'
curl localhost:8000/notes
curl 'localhost:8000/notes?q=hi'
curl localhost:8000/notes/1
curl -X PATCH localhost:8000/notes/1 -H 'content-type: application/json' \
  -d '{"body":"world"}'
curl -X DELETE localhost:8000/notes/1
curl localhost:8000/notes/999      # 404
```

State persists in `notes.db`.
