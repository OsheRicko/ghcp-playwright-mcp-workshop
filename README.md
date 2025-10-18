# Playwright Workshop

一個全面的 Playwright Python 測試框架，用於網頁自動化和端到端測試

## 📁 專案結構

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
├── report/                         # 測試報告和截圖
│   ├── screenshot/
│   ├── xml/
│   └── html/
├── sample.py                       # 基本 Playwright 範例
├── sample_pytest.py               # Pytest-Playwright 範例
├── requirements.txt               # Python 相依性套件
├── pytest.ini                    # Pytest 設定檔
├── .gitignore
└── README.md
```

## 🚀 開始使用

### 前置需求

- Python 3.8+
- pip

### 安裝

1. 安裝相關套件：
    ```bash
    pip install -r requirements.txt
    ```

2. 安裝 playwright 瀏覽器執行檔：
    ```bash
    playwright install
    playwright install-deps
    ```

### 執行測試

1. 執行基本測試：
    ```bash
    python sample.py
    ```

2. 執行 pytest 測試檔案：
    ```bash
    pytest sample_pytest.py --junitxml=report/xml/sample_report.xml --html=report/html/report_sample.html --self-contained-html
    ```