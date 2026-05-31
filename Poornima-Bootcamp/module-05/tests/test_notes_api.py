"""Pytest suite for the Notes API (module-04/winner/app.py).

Covers: create, list, search, get-one, update (PATCH), delete, 404, 422.

The app is exercised in-process via starlette's TestClient, which is built on
httpx and drives the ASGI app through an in-memory transport — no network, no
HTTP mocks, and the lifespan handler (which calls init_schema) fires normally.
Each test gets an isolated SQLite database in a pytest tmp_path directory.

Run with:
    cd module-05 && pytest tests/ -v
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Generator

import pytest
from starlette.testclient import TestClient  # httpx-based, in-process

# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

# tests/ -> module-05 -> Poornima-Bootcamp, then into module-04/winner.
_WINNER_APP = Path(__file__).resolve().parents[2] / "module-04" / "winner" / "app.py"


def _load_module():
    """Import a fresh copy of the winner app module so each test is isolated."""
    spec = importlib.util.spec_from_file_location("notes_winner_app", _WINNER_APP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def client(tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    """TestClient (httpx-based) backed by a fresh SQLite DB per test."""
    mod = _load_module()
    # Patch DB_PATH before TestClient enters so the lifespan startup — which
    # calls init_schema() — creates the table in the temp DB, not the cwd.
    monkeypatch.setattr(mod, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(mod.app) as tc:
        yield tc


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _post(c: TestClient, title: str = "Hello", body: str = "World"):
    return c.post("/notes", json={"title": title, "body": body})


# ---------------------------------------------------------------------------
# CREATE  POST /notes  -> 201
# ---------------------------------------------------------------------------


def test_create_returns_201(client):
    assert _post(client).status_code == 201


def test_create_response_fields(client):
    data = _post(client, title="My note", body="Some content").json()
    assert data["title"] == "My note"
    assert data["body"] == "Some content"
    assert isinstance(data["id"], int)
    assert data["created_at"] == data["updated_at"]  # equal at creation
    assert data["created_at"].endswith("+00:00")  # ISO 8601 UTC


def test_create_ids_increment(client):
    id1 = _post(client).json()["id"]
    id2 = _post(client).json()["id"]
    assert id2 == id1 + 1


# ---------------------------------------------------------------------------
# LIST  GET /notes  -> 200
# ---------------------------------------------------------------------------


def test_list_empty(client):
    r = client.get("/notes")
    assert r.status_code == 200
    assert r.json() == []


def test_list_returns_all_in_order(client):
    _post(client, title="A", body="a")
    _post(client, title="B", body="b")
    r = client.get("/notes")
    assert r.status_code == 200
    assert [n["title"] for n in r.json()] == ["A", "B"]


# ---------------------------------------------------------------------------
# SEARCH  GET /notes?q=...  -> 200
# ---------------------------------------------------------------------------


def test_search_by_title(client):
    _post(client, title="Python tips", body="Use list comps")
    _post(client, title="Cooking guide", body="Boil water first")
    results = client.get("/notes", params={"q": "Python"}).json()
    assert len(results) == 1
    assert results[0]["title"] == "Python tips"


def test_search_by_body(client):
    _post(client, title="Tip", body="Use httpx for testing")
    _post(client, title="Other", body="Nothing relevant")
    results = client.get("/notes", params={"q": "httpx"}).json()
    assert len(results) == 1
    assert results[0]["body"] == "Use httpx for testing"


def test_search_no_match_returns_empty(client):
    _post(client, title="Note", body="content")
    assert client.get("/notes", params={"q": "zzznomatch"}).json() == []


def test_search_case_insensitive_ascii(client):
    # SQLite LIKE is case-insensitive for ASCII characters.
    _post(client, title="FastAPI", body="web framework")
    assert len(client.get("/notes", params={"q": "fastapi"}).json()) == 1


# ---------------------------------------------------------------------------
# GET ONE  GET /notes/{id}  -> 200 / 404
# ---------------------------------------------------------------------------


def test_get_one_returns_note(client):
    created = _post(client, title="Solo", body="alone").json()
    r = client.get(f"/notes/{created['id']}")
    assert r.status_code == 200
    assert r.json() == created


def test_get_one_404(client):
    r = client.get("/notes/9999")
    assert r.status_code == 404
    assert r.json() == {"error": "not found"}


# ---------------------------------------------------------------------------
# UPDATE  PATCH /notes/{id}  -> 200 / 404  (partial update)
# ---------------------------------------------------------------------------


def test_patch_title_only_preserves_body(client):
    nid = _post(client, title="Old", body="Keep me").json()["id"]
    r = client.patch(f"/notes/{nid}", json={"title": "New"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["body"] == "Keep me"


def test_patch_body_only_preserves_title(client):
    nid = _post(client, title="Keep me", body="Old body").json()["id"]
    r = client.patch(f"/notes/{nid}", json={"body": "New body"})
    assert r.status_code == 200
    assert r.json()["title"] == "Keep me"
    assert r.json()["body"] == "New body"


def test_patch_both_fields(client):
    nid = _post(client).json()["id"]
    r = client.patch(f"/notes/{nid}", json={"title": "T2", "body": "B2"})
    assert r.status_code == 200
    assert r.json()["title"] == "T2"
    assert r.json()["body"] == "B2"


def test_patch_404(client):
    r = client.patch("/notes/9999", json={"title": "X"})
    assert r.status_code == 404
    assert r.json() == {"error": "not found"}


# ---------------------------------------------------------------------------
# DELETE  DELETE /notes/{id}  -> 204 / 404
# ---------------------------------------------------------------------------


def test_delete_returns_204(client):
    nid = _post(client).json()["id"]
    assert client.delete(f"/notes/{nid}").status_code == 204


def test_delete_removes_note(client):
    nid = _post(client).json()["id"]
    client.delete(f"/notes/{nid}")
    assert client.get(f"/notes/{nid}").status_code == 404


def test_delete_does_not_affect_others(client):
    id1 = _post(client, title="Keep").json()["id"]
    id2 = _post(client, title="Gone").json()["id"]
    client.delete(f"/notes/{id2}")
    assert client.get(f"/notes/{id1}").status_code == 200


def test_delete_404(client):
    r = client.delete("/notes/9999")
    assert r.status_code == 404
    assert r.json() == {"error": "not found"}


# ---------------------------------------------------------------------------
# 422  Validation errors
# ---------------------------------------------------------------------------


def test_create_422_missing_title(client):
    assert client.post("/notes", json={"body": "no title"}).status_code == 422


def test_create_422_missing_body(client):
    assert client.post("/notes", json={"title": "no body"}).status_code == 422


def test_create_422_empty_title(client):
    assert client.post("/notes", json={"title": "", "body": "b"}).status_code == 422


def test_create_422_whitespace_title(client):
    # The strip-based validator rejects whitespace-only titles.
    assert client.post("/notes", json={"title": "   ", "body": "b"}).status_code == 422


def test_create_422_empty_body(client):
    assert client.post("/notes", json={"title": "t", "body": ""}).status_code == 422


def test_patch_422_empty_title(client):
    nid = _post(client).json()["id"]
    assert client.patch(f"/notes/{nid}", json={"title": ""}).status_code == 422


def test_patch_422_whitespace_body(client):
    nid = _post(client).json()["id"]
    assert client.patch(f"/notes/{nid}", json={"body": "   "}).status_code == 422
