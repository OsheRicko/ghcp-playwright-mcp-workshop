import re
import pytest
from playwright.sync_api import Page, expect
import logging
import os

def test_example_domain(page: Page):
    try:
        page.goto("https://example.com/")
        expect(page.get_by_role("heading", name="Example Domain")).to_be_visible()
        page.get_by_text("This domain is for use in").click()
        page.get_by_role("link", name="More information...").click()
        expect(page).to_have_url(re.compile(r"https?://www\.iana\.org/help/example-domains"))
        # expect(page).to_have_url("https://www.iana.org/help/example-domains")
        page.wait_for_load_state("networkidle")
    except Exception as e:
        screenshot_dir = os.path.join("report", "scrennshot")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, "error_pytest.png")
        page.screenshot(path=screenshot_path)
        logging.error(f"Screenshot saved to {screenshot_path}")
        raise

