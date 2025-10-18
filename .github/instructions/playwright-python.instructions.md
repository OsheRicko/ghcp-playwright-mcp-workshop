---
description: '根據官方文件的 Playwright Python AI 測試生成指引'
applyTo: '**'
---

# Playwright Python 測試生成指引

## 測試撰寫準則

### 程式碼品質標準
- **定位器（Locators）**：優先使用以使用者為中心的角色型定位器（如 `get_by_role`、`get_by_label`、`get_by_text`），以提升穩定性與可存取性  
- **斷言（Assertions）**：使用自動重試、以網頁為中心的斷言 API，例如 `expect(page).to_have_title(...)`除非特別要測試元素可見性變化，否則避免使用 `expect(locator).to_be_visible()`，因為更具體的斷言通常更可靠  
- **逾時設定（Timeouts）**：依賴 Playwright 內建的自動等待機制，避免使用硬編碼等待或任意增加預設逾時時間  
- **可讀性（Clarity）**：使用具描述性的測試名稱（例如 `def test_navigation_link_works():`）以清楚表達意圖僅在邏輯複雜時撰寫註解，不要為簡單動作（如「點擊按鈕」）加註說明

### 測試結構
- **匯入（Imports）**：每個測試檔案都應以 `from playwright.sync_api import Page, expect` 開頭  
- **測試治具（Fixtures）**：使用 `page: Page` 作為測試函式參數，以便操作瀏覽器頁面  
- **設定步驟（Setup）**：在每個測試函式開頭放置導覽步驟，例如 `page.goto()`若多個測試共用相同設定動作，請使用標準 Pytest fixtures 管理

### 檔案組織
- **位置（Location）**：將測試檔案存放於專用的 `tests/` 目錄，或依專案現有結構存放  
- **命名（Naming）**：測試檔案必須遵循 `test_<功能或頁面>.py` 命名慣例，以便 Pytest 自動發現  
- **範圍（Scope）**：建議每個主要應用功能或頁面使用一個測試檔案

---

## 斷言最佳實踐
- **元素數量**：使用 `expect(locator).to_have_count()` 驗證定位器所找到的元素數量  
- **文字內容**：使用 `expect(locator).to_have_text()` 進行精確比對，或 `expect(locator).to_contain_text()` 進行部分比對  
- **導覽驗證**：使用 `expect(page).to_have_url()` 驗證頁面 URL  
- **斷言風格**：優先使用 `expect` 而非傳統 `assert`，以獲得更穩定的 UI 測試行為

## 範例

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

## 測試執行策略

1. **執行**: 使用終端機命令 pytest 來執行測試
2. **除錯失敗**: 分析測試失敗的原因，並針對根本問題進行修正