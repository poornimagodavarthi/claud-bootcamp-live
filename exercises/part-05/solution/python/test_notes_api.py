"""Pytest suite for the Module 4 Notes API (Python track).

Run from a folder that has the module-4 reference solution alongside:
    pytest -q

Each test creates an in-memory SQLite DB by patching DB_PATH.
"""
from __future__ import annotations

import importlib
import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # Point the app at a fresh sqlite file per test
    db = tmp_path / "notes.db"
    monkeypatch.setenv("NOTES_DB", str(db))
    # The reference app uses a module-level DB_PATH; patch it then re-init
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "solution", "python"))
    if "app" in sys.modules:
        del sys.modules["app"]
    app_mod = importlib.import_module("app")
    app_mod.DB_PATH = str(db)
    app_mod._init_db()
    return TestClient(app_mod.app)


def test_create_returns_201_and_body(client):
    r = client.post("/notes", json={"title": "a", "body": "b"})
    assert r.status_code == 201
    j = r.json()
    assert j["id"] == 1
    assert j["title"] == "a"
    assert j["body"] == "b"
    assert j["created_at"] == j["updated_at"]


def test_create_invalid_body_returns_422(client):
    r = client.post("/notes", json={"title": "", "body": "b"})
    assert r.status_code == 422


def test_list_empty(client):
    r = client.get("/notes")
    assert r.status_code == 200
    assert r.json() == []


def test_list_after_creates(client):
    client.post("/notes", json={"title": "x", "body": "1"})
    client.post("/notes", json={"title": "y", "body": "2"})
    r = client.get("/notes")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_search_substring(client):
    client.post("/notes", json={"title": "alpha", "body": "one"})
    client.post("/notes", json={"title": "beta", "body": "two"})
    r = client.get("/notes", params={"q": "alp"})
    assert r.status_code == 200
    titles = [n["title"] for n in r.json()]
    assert titles == ["alpha"]


def test_get_one_404(client):
    r = client.get("/notes/999")
    assert r.status_code == 404


def test_patch_partial(client):
    client.post("/notes", json={"title": "t", "body": "b"})
    r = client.patch("/notes/1", json={"body": "B"})
    assert r.status_code == 200
    assert r.json()["title"] == "t"
    assert r.json()["body"] == "B"


def test_delete_204_then_404(client):
    client.post("/notes", json={"title": "t", "body": "b"})
    r = client.delete("/notes/1")
    assert r.status_code == 204
    r = client.delete("/notes/1")
    assert r.status_code == 404


def test_search_empty_query_returns_all(client):
    """Boundary: q="" should return all notes, not zero."""
    client.post("/notes", json={"title": "a", "body": "b"})
    r = client.get("/notes", params={"q": ""})
    assert r.status_code == 200
    assert len(r.json()) == 1
