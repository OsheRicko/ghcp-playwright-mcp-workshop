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
        page.get_by_role("link", name="Learn more").click()
        expect(page).to_have_url(re.compile(r"https?://www\.iana\.org/help/example-domains"))
        # expect(page).to_have_url("https://www.iana.org/help/example-domains")
        page.wait_for_load_state("networkidle")
        
        # Take screenshot on success
        screenshot_dir = os.path.join("report", "screenshot")
        os.makedirs(screenshot_dir, exist_ok=True)
        browser_name = page.context.browser.browser_type.name
        success_screenshot_path = os.path.join(screenshot_dir, f"success_pytest_{browser_name}.png")
        page.screenshot(path=success_screenshot_path)
        print(f"Success screenshot saved to {success_screenshot_path}")
    except Exception as e:
        screenshot_dir = os.path.join("report", "screenshot")
        os.makedirs(screenshot_dir, exist_ok=True)
        browser_name = page.context.browser.browser_type.name
        screenshot_path = os.path.join(screenshot_dir, f"error_pytest_{browser_name}.png")
        page.screenshot(path=screenshot_path)
        logging.error(f"Screenshot saved to {screenshot_path}")
        raise

