import sys
import os
import tempfile
from pathlib import Path

import pytest

# Add service folder to path so we can import bookmarks_app
SERVICE_DIR = Path(__file__).parent.parent / "service"
sys.path.insert(0, str(SERVICE_DIR))


@pytest.fixture(scope="function")
def test_db_path():
    """Create a temporary SQLite database file for each test."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="function")
def app(test_db_path):
    """Create a fresh FastAPI app instance with isolated test database."""
    import importlib

    # Import and reload bookmarks_app with modified DATABASE
    if 'bookmarks_app' in sys.modules:
        del sys.modules['bookmarks_app']

    import bookmarks_app
    # Override the DATABASE before the app initializes
    bookmarks_app.DATABASE = test_db_path

    # Re-run init_db with the new database
    bookmarks_app.init_db()

    return bookmarks_app.app


@pytest.fixture(scope="function")
def client(app):
    """Create a TestClient for the FastAPI app."""
    from fastapi.testclient import TestClient
    return TestClient(app)
