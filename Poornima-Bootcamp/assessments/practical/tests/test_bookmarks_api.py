import pytest


class TestHappyPath:
    """Tests for successful operations."""

    def test_post_create_bookmark(self, client):
        """POST /bookmarks: Create a new bookmark and return 201."""
        payload = {
            "url": "https://python.org",
            "title": "Python Official",
            "tag": "coding"
        }
        response = client.post("/bookmarks", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["url"] == payload["url"]
        assert data["title"] == payload["title"]
        assert data["tag"] == payload["tag"]
        assert "id" in data
        assert isinstance(data["id"], int)
        assert data["id"] > 0

    def test_get_all_bookmarks(self, client):
        """GET /bookmarks: Return all bookmarks."""
        # Create multiple bookmarks
        bookmarks = [
            {"url": "https://python.org", "title": "Python", "tag": "coding"},
            {"url": "https://fastapi.io", "title": "FastAPI", "tag": "coding"},
            {"url": "https://news.ycombinator.com", "title": "HN", "tag": "news"}
        ]
        for bm in bookmarks:
            client.post("/bookmarks", json=bm)

        response = client.get("/bookmarks")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in item for item in data)
        assert all("url" in item for item in data)
        assert all("title" in item for item in data)
        assert all("tag" in item for item in data)

    def test_get_single_bookmark_by_id(self, client):
        """GET /bookmarks/{id}: Return a specific bookmark by ID."""
        # Create a bookmark
        create_response = client.post(
            "/bookmarks",
            json={"url": "https://python.org", "title": "Python", "tag": "coding"}
        )
        bookmark_id = create_response.json()["id"]

        response = client.get(f"/bookmarks/{bookmark_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bookmark_id
        assert data["url"] == "https://python.org"
        assert data["title"] == "Python"
        assert data["tag"] == "coding"


class TestErrorPath:
    """Tests for error conditions."""

    def test_get_nonexistent_bookmark_returns_404(self, client):
        """GET /bookmarks/{id}: Return 404 for missing bookmark."""
        response = client.get("/bookmarks/999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_delete_nonexistent_bookmark_returns_404(self, client):
        """DELETE /bookmarks/{id}: Return 404 for missing bookmark."""
        response = client.delete("/bookmarks/999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestBoundaryEdgeCases:
    """Tests for boundary and edge cases."""

    def test_filter_by_tag_no_matches_returns_empty_list(self, client):
        """GET /bookmarks?tag=nonexistent: Return empty list when no matches."""
        # Create bookmarks with specific tags
        client.post("/bookmarks", json={"url": "https://python.org", "title": "Python", "tag": "coding"})
        client.post("/bookmarks", json={"url": "https://news.ycombinator.com", "title": "HN", "tag": "news"})

        # Query for non-existent tag
        response = client.get("/bookmarks?tag=nonexistent")

        assert response.status_code == 200
        data = response.json()
        assert data == []
        assert isinstance(data, list)

    def test_filter_by_tag_returns_only_matching(self, client):
        """GET /bookmarks?tag=<t>: Return only bookmarks with matching tag."""
        # Create bookmarks with different tags
        client.post("/bookmarks", json={"url": "https://python.org", "title": "Python", "tag": "coding"})
        client.post("/bookmarks", json={"url": "https://fastapi.io", "title": "FastAPI", "tag": "coding"})
        client.post("/bookmarks", json={"url": "https://news.ycombinator.com", "title": "HN", "tag": "news"})

        response = client.get("/bookmarks?tag=coding")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["tag"] == "coding" for item in data)

    def test_delete_bookmark_removes_from_list(self, client):
        """DELETE /bookmarks/{id}: Verify deletion removes bookmark from list."""
        # Create bookmarks
        create1 = client.post("/bookmarks", json={"url": "https://python.org", "title": "Python", "tag": "coding"})
        create2 = client.post("/bookmarks", json={"url": "https://fastapi.io", "title": "FastAPI", "tag": "coding"})
        id1 = create1.json()["id"]
        id2 = create2.json()["id"]

        # Verify both exist
        all_response = client.get("/bookmarks")
        assert len(all_response.json()) == 2

        # Delete one
        delete_response = client.delete(f"/bookmarks/{id1}")
        assert delete_response.status_code == 204

        # Verify only one remains
        all_response = client.get("/bookmarks")
        assert len(all_response.json()) == 1
        assert all_response.json()[0]["id"] == id2

    def test_post_bookmark_with_special_characters(self, client):
        """POST /bookmarks: Handle special characters in URL and title."""
        payload = {
            "url": "https://example.com/path?query=value&other=123",
            "title": "Test & Special \"Chars\" 'Quote'",
            "tag": "test-tag_123"
        }
        response = client.post("/bookmarks", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["url"] == payload["url"]
        assert data["title"] == payload["title"]
        assert data["tag"] == payload["tag"]
