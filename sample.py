import re
from playwright.sync_api import sync_playwright, expect
import os

def run_test(playwright, browser_name):
    browser = getattr(playwright, browser_name).launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://example.com/")
        expect(page.get_by_role("heading", name="Example Domain")).to_be_visible()
        page.get_by_text("This domain is for use in").click()
        page.get_by_role("link", name="More information...").click()
        expect(page).to_have_url(re.compile(r"https?://www\.iana\.org/help/example-domains"))
        # expect(page).to_have_url("https://www.iana.org/help/example-domains")
        page.wait_for_load_state("networkidle")
    except Exception as e:
        # Ensure screenshot directory exists
        screenshot_dir = os.path.join("report", "scrennshot")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"error_{browser_name}.png")
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        raise
    finally:
        context.close()
        browser.close()

with sync_playwright() as playwright:
    for browser_name in ["chromium", "firefox", "webkit"]:
        try:
            print(f"Running test in {browser_name}...")
            run_test(playwright, browser_name)
        except Exception as e:
            print(f"Test failed in {browser_name}: {e}")
