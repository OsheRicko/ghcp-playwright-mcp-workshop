---
mode: 'agent'
description: 'Convert Playwright script into Pytest-Playwright compatible format'
tools: ['codebase', 'editFiles', 'runCommands', 'search', 'testFailure', 'terminalLastCommand']
---

# Task: Playwright Script to Pytest-Playwright Conversion

## Context
You are working with a UI test originally written using the basic Playwright Python API with `sync_playwright`. This script tests a flow on user provided url, and includes navigation, assertions, and screenshot on failure logic.

## Current State
The current test script:
- Uses `sync_playwright` directly to launch and control each browser (`chromium`, `firefox`, `webkit`)
- Has retry logic and failure screenshot handling
- Is written in a procedural format, not using `pytest`
- Browser is selected via a loop in code
- pytest configuration is set up in `pytest.ini`

## Goal
Refactor the test script into a **pytest-playwright** compatible format, using the `pytest-playwright` plugin’s fixtures and conventions.

## Target Format
The refactored test:
- Must use `pytest` and `pytest-playwright` fixtures
- Must define a test function using the `page` fixture
- Must support multiple browsers (via `--browser` CLI or `pytest-playwright` plugin parametrize mechanism)
- Must include the same assertions and error screenshot behavior
- Must use a regex `expect(...).to_have_url()` as needed

## Sample Input Script

```python
from playwright.sync_api import sync_playwright, expect
import re, os

def run_test(playwright, browser_name):
    browser = getattr(playwright, browser_name).launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://example.com/")
        expect(page.get_by_role("heading", name="Example Domain")).to_be_visible()
        page.get_by_text("This domain is for use in").click()
        page.get_by_role("link", name="More information...").click()
        expect(page).to_have_url("https://www.iana.org/help/example-domains")
        page.wait_for_load_state("networkidle")
    except Exception:
        os.makedirs("report/scrennshot", exist_ok=True)
        page.screenshot(path=f"report/scrennshot/error_{browser_name}.png")
        raise
    finally:
        context.close()
        browser.close()
```

## Expected Output Format

```python
import pytest
from playwright.sync_api import Page, expect
import os
import re

def test_example_domain(page: Page, browser_name: str):
    try:
        page.goto("https://example.com/")
        expect(page.get_by_role("heading", name="Example Domain")).to_be_visible()
        page.get_by_text("This domain is for use in").click()
        page.get_by_role("link", name="More information...").click()
        expect(page).to_have_url("https://www.iana.org/help/example-domains")
        page.wait_for_load_state("networkidle")
    except Exception:
        os.makedirs("report/scrennshot", exist_ok=True)
        page.screenshot(path="report/scrennshot/error_pytest_{browser_name}.png")
        raise

```

## Key Changes to Make
- Replace the manual playwright.chromium/... code with the built-in page fixture
- Use pytest-style function: def test_...()
- Remove manual loop over browsers — rely on pytest-playwright to handle multiple browsers (CLI param --browser)
- Ensure screenshot on error logic is preserved
- Use expect(page).to_have_url(re.compile(...)) for flexible, pattern-based URL validation instead of hardcoded strings
- Add log messages for clarity on test steps and errors

## Notes
- Do not modify the `pytest.ini` file, it is already set up for pytest-playwright.
- Don not modify the provided test scripts, always create new files for the refactored tests, file name could be <provided-file-name>_pytest.
- Ask the user for the URL to test first if not provided in the script.
- Pytest-playwright manages browser lifecycle automatically, so don’t include context.close() or browser.close() manually.
- The test runner (e.g. GitHub Actions) can pass in --browser flag to run across all browsers.
- Regex allows more flexibility (e.g. http/https support, domain variations) and is recommended for URL matching in dynamic web environments.

## Summary Instruction
At the end of the conversion, always provide the user with a ready-to-run pytest command like the following:

```
pytest <scenario>-pytest.py --junitxml=report\xml\<scenario>_report_<currebt-datetime>.xml --html=report\html\<scenario>_report_<currebt-datetime>.html --self-contained-html
```

Replace <scenario> with the actual file name of the converted test. This helps users immediately verify the test and generate reports in both JUnit XML and HTML format.