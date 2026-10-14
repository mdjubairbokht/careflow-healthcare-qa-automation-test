"""Standalone Playwright fixtures, without a pytest browser plugin."""
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()
