import pytest
from unittest.mock import patch, Mock
from lxml import html

from scraper.fetcher import fetch_page_content
from scraper.parser import parse_page


# -----------------------------
# Test fetch_page_content
# -----------------------------

@patch("scraper.fetcher.requests.get")
def test_fetch_page_content_success(mock_get):
    # Fake HTML response
    fake_html = "<html><body><h2>Test Title</h2></body></html>"
    mock_response = Mock()
    mock_response.content = fake_html.encode("utf-8")
    mock_get.return_value = mock_response

    tree = fetch_page_content("https://example.com")

    assert tree is not None
    assert isinstance(tree, html.HtmlElement)


@patch("scraper.fetcher.requests.get")
def test_fetch_page_content_failure(mock_get):
    # Simulate request failure
    mock_get.side_effect = Exception("Network error")

    tree = fetch_page_content("https://example.com")

    assert tree is None


# -----------------------------
# Test parse_page
# -----------------------------

@patch("scraper.parser.fetch_page_content")
def test_parse_page_success(mock_fetch):
    fake_html = """
    <html>
        <body>
            <h2>News One</h2>
            <a href="https://example.com/1">Link</a>

            <h2>News Two</h2>
            <a href="https://example.com/2">Link</a>
        </body>
    </html>
    """
    mock_fetch.return_value = html.fromstring(fake_html)

    items = parse_page("https://example.com")

    assert len(items) == 2
    assert items[0]["title"] == "News One"
    assert items[0]["link"] == "https://example.com/1"


@patch("scraper.parser.fetch_page_content")
def test_parse_page_no_content(mock_fetch):
    mock_fetch.return_value = None

    items = parse_page("https://example.com")

    assert items == []
