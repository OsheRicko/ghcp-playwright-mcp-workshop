# Playwright MCP with GitHub Copilot Workshop

## 🧑‍💻 Playwright MCP 操作步驟練習

以下為練習 Playwright MCP 操作的標準步驟，請依序完成：
> 📢 **注意**：為確保產生結果符合 lab 環境，建議使用指示中建議的模型進行操作

### Lab 1 : 環境準備及測試
#### 環境準備

1. **開啟 Codespace**
2. **建立 python 虛擬環境**
    ```
    python -m venv venv
    source venv/bin/activate
    ```
2. **安裝相依套件**
   ```bash
   pip install -r requirements.txt
   playwright install
   playwright install-deps
   ```


#### 測試 playwright 腳本執行

1. **執行測試檔案**
   ```bash
    python sample.py
   ```
   - **預期**：於 `report/screenshot/` 中顯示成功截圖

2. **執行測試並產生報告**
   ```bash
   pytest sample_pytest.py /
       --junitxml=report/xml/sample_report.xml /
       --html=report/html/report_sample.html /
       --self-contained-html
   ```
   - **預期**: 於 `report/screenshot/` 中顯示成功截圖及 html 和 xml 報告
   - 💡 **Tips**: 於 extension 中安裝 **Live Preview (Microsoft)** 可於 Codespace 中瀏覽 html 頁面

---

### Lab 2 : 使用 Playwright MCP 進行測試

1. **啟動 Playwright MCP**: 瀏覽至 `.github/mcp.json`，找到 `playwright` 並點選 start
2. **透過 GitHub Copilot Chat 進行測試**
    - 開啟 GitHub Copilot Chat 視窗，選擇 Agent 模式，模型使用 `claude sonnet 4`
    - 輸入指令
        ```
        /playwright-explorer-website 瀏覽至 https://www.asus.com/tw/displays-desktops/gaming-tower-pcs/all-series/ 進行以下測試驗證
         1. 確認產品比較功能：查詢 60,000 以上的產品，進行產品比較並顯示比較結果
         2. 確認產品比較上線功能：當操作產品比較超過 4 個以上則無法增加
        ```
   - **預期**:  於 `report/screenshot/` 中顯示截圖，產生總結報告 `website-exploration-summary.md` 及建議的測試案例 `proposed-test-cases.md` 檔案

---

### Lab 3 : 進行探索測試並產生測試案例

1. **使用 `/clear` 開啟新的對話**
2. **透過 GitHub Copilot Chat 進行測試**
    - 開啟 GitHub Copilot Chat 視窗，選擇 Agent 模式，模型使用 `claude sonnet 4` 
    - 輸入指令
      ```
      /playwright-explorer-website.prompt.md 瀏覽 https://www.asus.com/tw/store/ 並將購物車的功能整理成測試案例文件
      ```
    - **預期**: 於 `report/` 產生購物車功能相關的測試案例
---

### Lab 4 : 產生測試腳本

1. **使用 `/clear` 開啟新的對話**
2. **反白選取 1-2 個 Lab 3 產生的測試文件中的測試案例** (為避免執行過久，建議選取少量測試案例)
3. **透過 GitHub Copilot Chat 進行測試**
    - 開啟 GitHub Copilot Chat 視窗，選擇 Agent 模式，模型使用 `claude sonnet 4` 
    - 輸入指令
      ```
      /playwright-generate-test 參考 #selection 產生測試腳本
      ```
   - **預期**: 於 `tests/` 生成 python 測試腳本並透過執行 pytest 指令產生 html 及 xml 測試報告
