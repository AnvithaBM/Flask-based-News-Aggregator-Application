import pytest
import app
from unittest.mock import patch, MagicMock


# ------------------------
# 1. Success Case
# ------------------------
@patch("app.requests.get")
def test_fetch_articles_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "ok",
        "totalResults": 8,
        "articles": [
            {
                "title": "Test Article",
                "description": "This is a test description",
                "urlToImage": "http://example.com/image.jpg",
                "url": "http://example.com",
                "publishedAt": "2025-08-19T12:00:00Z",
                "source": {"name": "Example Source"}
            }
        ] * 4  # repeat 4 to simulate multiple articles
    }
    mock_get.return_value = mock_response

    articles, total_pages = app.fetch_articles(page=1, topic="technology")

    assert len(articles) == 4
    assert total_pages == 2  # since totalResults=8 and PAGE_SIZE=4
    assert articles[0]["title"] == "Test Article"
    assert articles[0]["source"] == "Example Source"


# ------------------------
# 2. API Error Case
# ------------------------
@patch("app.requests.get")
def test_fetch_articles_error_status(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "error"}
    mock_get.return_value = mock_response

    articles, total_pages = app.fetch_articles(page=1, topic="sports")

    assert articles == []
    assert total_pages == 1


# ------------------------
# 3. No Articles Case
# ------------------------
@patch("app.requests.get")
def test_fetch_articles_no_articles(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok", "totalResults": 0, "articles": []}
    mock_get.return_value = mock_response

    articles, total_pages = app.fetch_articles(page=1, topic="health")

    assert articles == []
    assert total_pages == 1


# ------------------------
# 4. Missing Fields Case
# ------------------------
@patch("app.requests.get")
def test_fetch_articles_missing_fields(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "ok",
        "totalResults": 1,
        "articles": [
            {
                # No title, description, image, etc.
                "source": {}
            }
        ]
    }
    mock_get.return_value = mock_response

    articles, total_pages = app.fetch_articles(page=1, topic="business")

    assert len(articles) == 1
    assert articles[0]["title"] is None
    assert articles[0]["content"] == ""
    assert articles[0]["source"] == "Unknown"
    assert total_pages == 1
