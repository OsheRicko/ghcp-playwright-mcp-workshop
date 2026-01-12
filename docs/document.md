# Playwright Workshop

A comprehensive Playwright Python testing framework for web automation and end-to-end testing.

## 📁 Project Structure

```
playwright-workshop/
├── .github/
│   ├── instructions/
│   │   └── playwright-python.instructions.md
│   ├── prompts/
│   │   ├── pytest-playwright.prompt.md
│   │   ├── playwright-generate-test.prompt.md
│   │   └── playwright-explorer-website.prompt.md
│   └── chatmodes/
│       └── playwright-expert.chatmode.md
├── .vscode/
│   └── mcp.json
├── report/                         # Test reports and screenshots
│   ├── screenshot/
│   ├── xml/
│   └── html/
├── sample.py                       # Basic Playwright example
├── sample_pytest.py               # Pytest-Playwright example
├── requirements.txt               # Python dependencies
├── pytest.ini                    # Pytest configuration
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Install Playwright browsers:
    ```bash
    playwright install
    playwright install-deps
    ```

### Running Tests

1. Run the basic script:
    ```bash
    python sample.py
    ```

2. Run the pytest test file:
    ```bash
    pytest sample_pytest.py --junitxml=report/xml/sample_report.xml --html=report/html/report_sample.html --self-contained-html
    ```