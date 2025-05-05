import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.ui
class TestExample:
    def test_open_url(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.example.com")
            assert page.title() == "Example Domain"
            browser.close()
