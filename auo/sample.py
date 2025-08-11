import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("http://localhost:5138/")
        expect(page.get_by_role("heading", name="Smart Cat Tech. Purrsonalized.")).to_be_visible()
        page.get_by_role("link", name="About us").click()
        expect(page).to_have_url("http://localhost:5138/about")
        page.wait_for_load_state("networkidle")
        page.close()
    except Exception as e:
        print(f"Test failed in Microsoft Edge: {e}")
        screenshot_dir = os.path.join("report", "screenshot")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"error_edge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
    finally:
        context.close()
        browser.close()


with sync_playwright() as playwright:
    try:
        print("Running test in Microsoft Edge...")
        run(playwright)
        print("Test completed successfully.")
    except Exception as e:
        print(f"Test failed: {e}")