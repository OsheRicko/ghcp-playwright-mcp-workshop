---
description: 'Playwright Python AI test generation guidelines based on official documentation'
applyTo: '**'
---

# Playwright Python Test Generation Guidelines

## Test Authoring Principles

### Code Quality Standards
- **Locators**: Prefer user-centric, role-based locators such as `get_by_role`, `get_by_label`, and `get_by_text` to improve stability and accessibility.  
- **Assertions**: Use auto-retrying, web-first assertion APIs such as `expect(page).to_have_title(...)`. Unless you specifically need to test visibility changes, avoid `expect(locator).to_be_visible()`; more specific assertions are usually more reliable.  
- **Timeouts**: Rely on Playwright's built-in auto-waiting. Avoid hard-coded sleeps or arbitrarily increasing default timeouts.  
- **Clarity**: Use descriptive test names (for example, `def test_navigation_link_works():`) to clearly express intent. Only add comments when the logic is complex; do not comment on trivial actions like clicking a button.

### Test Structure
- **Imports**: Every test file should start with `from playwright.sync_api import Page, expect`.  
- **Fixtures**: Use `page: Page` as a test function parameter to interact with the browser page.  
- **Setup Steps**: Put navigation steps such as `page.goto()` at the start of each test. If multiple tests share the same setup, use standard Pytest fixtures.

### File Organization
- **Location**: Store test files in a dedicated `tests/` directory or follow the existing project structure.  
- **Naming**: Test files should follow the `test_<feature_or_page>.py` naming convention so that Pytest can discover them automatically.  
- **Scope**: Prefer one test file per major application feature or page.

---

## Assertion Best Practices
- **Element Count**: Use `expect(locator).to_have_count()` to validate the number of matched elements.  
- **Text Content**: Use `expect(locator).to_have_text()` for exact matches, or `expect(locator).to_contain_text()` for partial matches.  
- **Navigation Verification**: Use `expect(page).to_have_url()` to validate the page URL.  
- **Assertion Style**: Prefer `expect` over traditional `assert` for more stable UI tests.

## Examples

```python
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")

def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")

def test_has_title(page: Page):
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.get_by_role("link", name="Get started").click()
    
    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
```

## Test Execution Strategy

1. **Run tests**: Use the `pytest` command in the terminal to execute tests.
2. **Debug failures**: Analyze the root cause of any failed tests and fix the underlying issues.