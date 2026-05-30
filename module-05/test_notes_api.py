"""Pytest suite for the Notes API (module-04/winner/app.py).

Covers: create, list, search, get-one, PUT update, PATCH update,
        delete, 404 errors, and 422 validation errors.

Run with:
    cd module-05 && pytest test_notes_api.py -v

Each test gets an isolated SQLite DB in a pytest tmp_path directory.
The app is started in-process via starlette.testclient.TestClient (which
is built on httpx) — no network, no HTTP mocks, lifespan events fire normally.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Generator

import pytest
from starlette.testclient import TestClient

# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

_WINNER_APP = Path(__file__).resolve().parent.parent / "module-04" / "winner" / "app.py"


def _load_module():
    """Import a fresh copy of the app module so each fixture gets its own app."""
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
    # Patch before TestClient enters so the startup event uses the temp DB.
    monkeypatch.setattr(mod, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(mod.app) as tc:
        yield tc


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _post(c: TestClient, title: str = "Hello", body: str = "World") -> TestClient:
    return c.post("/notes", json={"title": title, "body": body})


# ---------------------------------------------------------------------------
# CREATE  POST /notes
# ---------------------------------------------------------------------------


def test_create_returns_201(client):
    assert _post(client).status_code == 201


def test_create_response_fields(client):
    r = _post(client, title="My note", body="Some content")
    data = r.json()
    assert data["title"] == "My note"
    assert data["body"] == "Some content"
    assert isinstance(data["id"], int)
    assert "created_at" in data
    assert "updated_at" in data


def test_create_ids_increment(client):
    id1 = _post(client).json()["id"]
    id2 = _post(client).json()["id"]
    assert id2 == id1 + 1


# ---------------------------------------------------------------------------
# LIST  GET /notes
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
    titles = [n["title"] for n in r.json()]
    assert titles == ["A", "B"]


# ---------------------------------------------------------------------------
# SEARCH  GET /notes?q=...
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
    results = client.get("/notes", params={"q": "fastapi"}).json()
    assert len(results) == 1


# ---------------------------------------------------------------------------
# GET ONE  GET /notes/{id}
# ---------------------------------------------------------------------------


def test_get_one_returns_note(client):
    created = _post(client, title="Solo", body="alone").json()
    r = client.get(f"/notes/{created['id']}")
    assert r.status_code == 200
    assert r.json() == created


def test_get_one_404(client):
    r = client.get("/notes/9999")
    assert r.status_code == 404
    assert "error" in r.json()


# ---------------------------------------------------------------------------
# UPDATE (PUT)  PUT /notes/{id}
# ---------------------------------------------------------------------------


def test_put_updates_fields(client):
    nid = _post(client, title="Old", body="Old body").json()["id"]
    r = client.put(f"/notes/{nid}", json={"title": "New", "body": "New body"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New"
    assert data["body"] == "New body"


def test_put_returns_updated_at(client):
    nid = _post(client).json()["id"]
    r = client.put(f"/notes/{nid}", json={"title": "X", "body": "Y"})
    assert "updated_at" in r.json()


def test_put_404(client):
    r = client.put("/notes/9999", json={"title": "X", "body": "Y"})
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# UPDATE (PATCH)  PATCH /notes/{id}
# ---------------------------------------------------------------------------


def test_patch_title_only(client):
    nid = _post(client, title="Old", body="Keep me").json()["id"]
    r = client.patch(f"/notes/{nid}", json={"title": "New"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["body"] == "Keep me"


def test_patch_body_only(client):
    nid = _post(client, title="Keep me", body="Old body").json()["id"]
    r = client.patch(f"/notes/{nid}", json={"body": "New body"})
    assert r.status_code == 200
    assert r.json()["title"] == "Keep me"
    assert r.json()["body"] == "New body"


def test_patch_both_fields(client):
    nid = _post(client).json()["id"]
    r = client.patch(f"/notes/{nid}", json={"title": "T2", "body": "B2"})
    assert r.json()["title"] == "T2"
    assert r.json()["body"] == "B2"


def test_patch_404(client):
    r = client.patch("/notes/9999", json={"title": "X"})
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# DELETE  DELETE /notes/{id}
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
    assert client.delete("/notes/9999").status_code == 404


# ---------------------------------------------------------------------------
# 422  Validation errors
# ---------------------------------------------------------------------------


def test_create_422_missing_title(client):
    assert client.post("/notes", json={"body": "no title"}).status_code == 422


def test_create_422_missing_body(client):
    assert client.post("/notes", json={"title": "no body"}).status_code == 422


def test_create_422_empty_title(client):
    assert client.post("/notes", json={"title": "", "body": "b"}).status_code == 422


def test_create_422_empty_body(client):
    assert client.post("/notes", json={"title": "t", "body": ""}).status_code == 422


def test_put_422_missing_title(client):
    nid = _post(client).json()["id"]
    assert client.put(f"/notes/{nid}", json={"body": "b"}).status_code == 422


def test_put_422_empty_title(client):
    nid = _post(client).json()["id"]
    assert client.put(f"/notes/{nid}", json={"title": "", "body": "b"}).status_code == 422


def test_put_422_empty_body(client):
    nid = _post(client).json()["id"]
    assert client.put(f"/notes/{nid}", json={"title": "t", "body": ""}).status_code == 422


def test_patch_422_empty_title(client):
    nid = _post(client).json()["id"]
    assert client.patch(f"/notes/{nid}", json={"title": ""}).status_code == 422


def test_patch_422_empty_body(client):
    nid = _post(client).json()["id"]
    assert client.patch(f"/notes/{nid}", json={"body": ""}).status_code == 422
