import { Hono } from "hono";
import { serve } from "@hono/node-server";
import Database from "better-sqlite3";
import { z } from "zod";

const db = new Database("notes.db");
db.exec(`
  CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  )
`);

const NoteIn = z.object({ title: z.string().min(1), body: z.string() });
const NotePatch = z.object({
  title: z.string().min(1).optional(),
  body: z.string().optional(),
});

const now = () => new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const app = new Hono();

app.post("/notes", async (c) => {
  const parsed = NoteIn.safeParse(await c.req.json().catch(() => null));
  if (!parsed.success) return c.json({ error: "invalid body" }, 422);
  const t = now();
  const info = db
    .prepare("INSERT INTO notes (title, body, created_at, updated_at) VALUES (?, ?, ?, ?)")
    .run(parsed.data.title, parsed.data.body, t, t);
  const row = db.prepare("SELECT * FROM notes WHERE id = ?").get(info.lastInsertRowid);
  return c.json(row, 201);
});

app.get("/notes", (c) => {
  const q = c.req.query("q");
  const rows = q
    ? db
        .prepare("SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY id")
        .all(`%${q}%`, `%${q}%`)
    : db.prepare("SELECT * FROM notes ORDER BY id").all();
  return c.json(rows);
});

app.get("/notes/:id", (c) => {
  const id = Number(c.req.param("id"));
  const row = db.prepare("SELECT * FROM notes WHERE id = ?").get(id);
  if (!row) return c.json({ error: "not found" }, 404);
  return c.json(row);
});

app.patch("/notes/:id", async (c) => {
  const id = Number(c.req.param("id"));
  const row = db.prepare("SELECT * FROM notes WHERE id = ?").get(id) as
    | { title: string; body: string }
    | undefined;
  if (!row) return c.json({ error: "not found" }, 404);
  const parsed = NotePatch.safeParse(await c.req.json().catch(() => null));
  if (!parsed.success) return c.json({ error: "invalid body" }, 422);
  const title = parsed.data.title ?? row.title;
  const body = parsed.data.body ?? row.body;
  db.prepare("UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?").run(
    title,
    body,
    now(),
    id,
  );
  return c.json(db.prepare("SELECT * FROM notes WHERE id = ?").get(id));
});

app.delete("/notes/:id", (c) => {
  const id = Number(c.req.param("id"));
  const info = db.prepare("DELETE FROM notes WHERE id = ?").run(id);
  if (info.changes === 0) return c.json({ error: "not found" }, 404);
  return c.body(null, 204);
});

const port = Number(process.env.PORT ?? 8000);
serve({ fetch: app.fetch, port });
console.log(`Notes API listening on http://localhost:${port}`);

export { app };
