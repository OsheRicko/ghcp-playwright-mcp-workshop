# Playwright MCP with GitHub Copilot Workshop

## 🧑‍💻 Playwright MCP Practice Steps

Below are the standard steps to practice Playwright MCP operations. Please complete them in order:
> 📢 **Note**: To ensure results match the lab environment, it is recommended to use the model suggested in the lab instructions.

### Lab 1: Environment Setup and Smoke Test
#### Environment Setup

1. **Open Codespace**
2. **Create a Python virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   playwright install-deps
   ```


#### Run Playwright Script

1. **Run the sample script**
   ```bash
    python sample.py
   ```
   - **Expected**: a success screenshot is generated under `report/screenshot/`.

2. **Run tests and generate reports**
   ```bash
   pytest sample_pytest.py /
       --junitxml=report/xml/sample_report.xml /
       --html=report/html/report_sample.html /
       --self-contained-html
   ```
   - **Expected**: success screenshots plus HTML and XML reports are generated under `report/`.
   - 💡 **Tips**: Install the **Live Preview (Microsoft)** extension to view HTML reports directly inside Codespaces.

---

### Lab 2: Use Playwright MCP for Testing

1. **Start Playwright MCP**: Open `.github/mcp.json`, find the `playwright` entry, and click **start**.
2. **Run tests via GitHub Copilot Chat**
    - Open GitHub Copilot Chat, switch to Agent mode, and use the `claude sonnet 4` model.
    - Enter the command:
        ```
        /playwright-explorer-website Browse to https://www.asus.com/tw/displays-desktops/gaming-tower-pcs/all-series/ and perform the following checks:
         1. Verify product comparison: search for products above 60,000, compare products, and show comparison results.
         2. Verify comparison limit: when more than 4 products are added to comparison, ensure no more items can be added.
        ```
   - **Expected**: screenshots under `report/screenshot/`, plus a summary report `website-exploration-summary.md` and suggested test cases file `proposed-test-cases.md`.

---

### Lab 3: Exploratory Testing and Test Case Generation

1. **Use `/clear` to start a new conversation**
2. **Run exploratory testing via GitHub Copilot Chat**
    - Open GitHub Copilot Chat, switch to Agent mode, and use the `claude sonnet 4` model.
    - Enter the command:
      ```
      /playwright-explorer-website.prompt.md Browse https://www.asus.com/tw/store/ and summarize the shopping cart functionality into a test case document.
      ```
    - **Expected**: shopping cart–related test cases are generated under `report/`.
---

### Lab 4: Generate Test Scripts

1. **Use `/clear` to start a new conversation**
2. **Select 1–2 test cases from the Lab 3 output** (to avoid long runs, select only a few cases).
3. **Generate tests via GitHub Copilot Chat**
    - Open GitHub Copilot Chat, switch to Agent mode, and use the `claude sonnet 4` model.
    - Enter the command:
      ```
      /playwright-generate-test Based on #selection, generate Playwright Python test scripts.
      ```
   - **Expected**: Python test scripts are generated under `tests/`, and running `pytest` produces HTML and XML test reports.
