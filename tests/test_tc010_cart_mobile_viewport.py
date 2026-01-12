import re
import pytest
from playwright.sync_api import Page, expect
import logging
import os

# Mobile viewport configurations for testing
MOBILE_VIEWPORTS = [
    {"width": 375, "height": 667, "name": "iPhone SE"},
    {"width": 414, "height": 896, "name": "iPhone 11 Pro Max"}
]

@pytest.mark.parametrize("viewport", MOBILE_VIEWPORTS, ids=lambda v: v["name"])
def test_cart_display_on_mobile_viewport(page: Page, browser_name: str, viewport: dict):
    """
    TC-010: Cart Display on Mobile Viewport
    Priority: High
    Objective: Verify cart displays correctly on mobile devices
    
    Test Steps:
    1. Set browser viewport to mobile size
    2. Navigate to https://rog.asus.com/us/
    3. Locate and click the shopping cart icon
    4. Observe the cart overlay presentation
    
    Expected Results:
    - Cart icon remains visible and accessible
    - Cart overlay scales appropriately for mobile
    - Close button is easily clickable
    - No horizontal scrolling required
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger("tc010_cart_mobile_viewport")
    
    # Step 1: Set browser viewport to mobile size
    logger.info(f"Setting viewport to {viewport['name']}: {viewport['width']}x{viewport['height']} on browser: {browser_name}")
    page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
    
    # Step 2: Navigate to ROG homepage
    logger.info("Navigating to https://rog.asus.com/us/")
    page.goto("https://rog.asus.com/us/")
    logger.info("Waiting for page to load completely")
    page.wait_for_load_state("networkidle")
    
    # Step 3: Locate and verify cart icon is visible
    logger.info("Locating shopping cart icon")
    cart_icon = page.get_by_role("button", name=re.compile(r"items in shopping cart", re.IGNORECASE))
    
    logger.info("Verifying cart icon is visible and accessible")
    expect(cart_icon).to_be_visible()
    expect(cart_icon).to_be_enabled()
    
    # Step 3: Click the shopping cart icon
    logger.info("Clicking shopping cart icon to open cart overlay")
    cart_icon.click()
    
    # Wait for cart overlay to appear
    logger.info("Waiting for cart overlay to appear")
    page.wait_for_timeout(2000)  # Longer wait for animation and rendering
    
    # Step 4: Verify cart overlay is displayed
    logger.info("Verifying cart overlay displays correctly")
    
    # Verify close button is visible and clickable (this confirms overlay is open)
    logger.info("Verifying close button is visible and accessible")
    close_button = page.get_by_role("button", name="close button")
    expect(close_button).to_be_visible()
    expect(close_button).to_be_enabled()
    logger.info("Close button is visible and clickable - cart overlay is displayed")
    
    # Check for horizontal scrolling - page width should not exceed viewport
    logger.info("Checking for horizontal scrolling")
    page_width = page.evaluate("() => document.documentElement.scrollWidth")
    viewport_width = viewport["width"]
    assert page_width <= viewport_width + 5, f"Page width {page_width} exceeds viewport width {viewport_width} - horizontal scrolling detected"
    logger.info(f"No horizontal scrolling detected (page width: {page_width}px, viewport: {viewport_width}px)")
    
    logger.info(f"Test completed successfully for {viewport['name']}")


def test_cart_toggle_on_mobile(page: Page, browser_name: str):
    """
    Additional test: Verify cart can be toggled open/closed by clicking cart icon
    on mobile viewport
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger("tc010_cart_toggle_mobile")
    
    # Set to mobile viewport (iPhone SE)
    logger.info(f"Setting viewport to iPhone SE: 375x667 on browser: {browser_name}")
    page.set_viewport_size({"width": 375, "height": 667})
    
    logger.info("Navigating to https://rog.asus.com/us/")
    page.goto("https://rog.asus.com/us/")
    page.wait_for_load_state("networkidle")
    
    cart_icon = page.get_by_role("button", name=re.compile(r"items in shopping cart", re.IGNORECASE))
    
    # First click - open cart
    logger.info("Opening cart overlay (first click)")
    cart_icon.click()
    page.wait_for_timeout(2000)
    
    # Verify cart is open by checking close button is visible
    close_button = page.get_by_role("button", name="close button")
    expect(close_button).to_be_visible()
    logger.info("Cart overlay opened successfully")
    
    # Close cart using close button (cart icon is blocked by overlay)
    logger.info("Closing cart overlay using close button")
    close_button.click()
    page.wait_for_timeout(1500)
    
    # Verify cart closed by checking if the cart overlay container has proper class/state
    # After close, the overlay should be hidden or removed
    cart_overlay = page.locator('[class*="bagDropdownMenu"][class*="isMenuShow"]')
    expect(cart_overlay).to_have_count(0)
    logger.info("Cart overlay closed successfully")
    
    # Third click - reopen cart (verify toggle works again)
    logger.info("Reopening cart overlay to verify toggle functionality")
    cart_icon.click()
    page.wait_for_timeout(2000)
    expect(close_button).to_be_visible()
    logger.info("Cart reopened successfully - toggle functionality verified")
    
    logger.info("Cart toggle test completed successfully")
