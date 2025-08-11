import re
import pytest
from playwright.sync_api import Page, expect
import logging
import os
from datetime import datetime

def test_home_page(page: Page):
    try:
        page.goto("http://localhost:5138/")
        expect(page.get_by_role("heading", name="Smart Cat Tech. Purrsonalized.")).to_be_visible()
        page.get_by_role("link", name="About us").click()
        expect(page).to_have_url("http://localhost:5138/about")
        page.wait_for_load_state("networkidle")
        # page.close()
    except Exception as e:
        logging.info(f"Test failed in Microsoft Edge: {e}")
        screenshot_dir = os.path.join("report", "screenshot")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"error_edge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        page.screenshot(path=screenshot_path)
        logging.error(f"Screenshot saved to {screenshot_path}")
        raise