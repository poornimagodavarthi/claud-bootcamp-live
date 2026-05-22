// Vitest suite for the Module 4 Notes API (Node track).
//
// We import the Hono `app` from the Module-4 reference solution. Each test
// uses a fresh in-memory request via `app.request` — no real network.
import { describe, it, expect, beforeEach } from "vitest";
import { app } from "../../../part-04/solution/node/src/index.js";

// Helpers
async function post(path: string, body: unknown) {
  return app.request(path, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
}
async function patch(path: string, body: unknown) {
  return app.request(path, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
}

describe("Notes API", () => {
  beforeEach(async () => {
    // Wipe table between tests (better-sqlite3 file persists by design)
    // Using direct SQL via the same connection isn't trivial here without
    // exposing it, so we rely on monotonically increasing ids and only
    // assert on properties that don't depend on absolute id values.
  });

  it("POST /notes returns 201 with created body", async () => {
    const r = await post("/notes", { title: "a", body: "b" });
    expect(r.status).toBe(201);
    const j = (await r.json()) as { id: number; title: string; body: string };
    expect(j.title).toBe("a");
    expect(j.body).toBe("b");
    expect(typeof j.id).toBe("number");
  });

  it("POST /notes with empty title returns 422", async () => {
    const r = await post("/notes", { title: "", body: "b" });
    expect(r.status).toBe(422);
  });

  it("GET /notes returns an array", async () => {
    const r = await app.request("/notes");
    expect(r.status).toBe(200);
    expect(Array.isArray(await r.json())).toBe(true);
  });

  it("GET /notes/:id with unknown id returns 404", async () => {
    const r = await app.request("/notes/9999999");
    expect(r.status).toBe(404);
  });

  it("PATCH /notes/:id partial update keeps unspecified fields", async () => {
    const created = await post("/notes", { title: "t", body: "b" });
    const { id } = (await created.json()) as { id: number };
    const r = await patch(`/notes/${id}`, { body: "B" });
    expect(r.status).toBe(200);
    const j = (await r.json()) as { title: string; body: string };
    expect(j.title).toBe("t");
    expect(j.body).toBe("B");
  });

  it("DELETE /notes/:id 204 then 404", async () => {
    const created = await post("/notes", { title: "x", body: "y" });
    const { id } = (await created.json()) as { id: number };
    const r1 = await app.request(`/notes/${id}`, { method: "DELETE" });
    expect(r1.status).toBe(204);
    const r2 = await app.request(`/notes/${id}`, { method: "DELETE" });
    expect(r2.status).toBe(404);
  });
});
