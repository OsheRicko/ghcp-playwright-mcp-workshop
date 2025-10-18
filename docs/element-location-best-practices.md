# Playwright 元素定位最佳實踐指引

## 核心原則

### 1. 優先使用使用者導向的定位器
**建議做法**:
```python
# 使用角色型定位器
page.get_by_role("button", name="比較")
page.get_by_role("checkbox", name="加入比較") 

# 使用標籤型定位器
page.get_by_label("價格範圍")
price_input = page.get_by_label("最低價格")

# 使用文字內容定位器
page.get_by_text("您只能比較4個產品")
```

**避免做法**:
```python
# 避免：依賴動態 ID
page.locator("#product-123456")  # ID 可能會變動

# 避免：過於具體的 CSS 選擇器
page.locator("div.container > div.row > div.col-md-4:nth-child(3)")
```

### 2. 處理動態元素參考 ID

#### 問題描述
在探索過程中發現，頁面互動後元素的參考 ID 會改變，導致後續操作失敗。

#### 解決策略

**策略 A: 即時重新定位**
```python
# 每次操作前重新取得元素參考
def get_current_snapshot():
    return mcp_playwright_browser_snapshot()

def click_element_by_content(element_description, text_content):
    snapshot = get_current_snapshot()
    # 在新的 snapshot 中尋找元素
    element = find_element_by_text(snapshot, text_content)
    mcp_playwright_browser_click(element=element_description, ref=element.ref)
```

**策略 B: 使用穩定的定位方式**
```python
# 使用相對穩定的屬性
page.locator("[data-testid='compare-checkbox']")
page.locator("[aria-label='加入產品比較']")
```

**策略 C: JavaScript 直接操作**
```python
# 當標準定位器失效時，使用 JavaScript 直接操作
def check_comparison_checkbox(product_index):
    js_code = f"""
    () => {{
        const checkboxes = document.querySelectorAll('input[type="checkbox"][data-purpose="compare"]');
        if (checkboxes[{product_index}]) {{
            checkboxes[{product_index}].click();
            return true;
        }}
        return false;
    }}
    """
    return mcp_playwright_browser_evaluate(function=js_code)
```

### 3. 元素等待策略

#### 明確等待條件
```python
# 等待元素可見
expect(page.locator(".product-grid")).to_be_visible()

# 等待文字出現
expect(page).to_have_text("查詢結果")

# 等待元素數量
expect(page.locator(".product-card")).to_have_count(5)
```

#### 避免硬編碼等待
```python
# 避免：任意等待時間
import time
time.sleep(3)  # 不確定的等待時間

# 推薦：條件式等待
page.wait_for_selector(".loading-spinner", state="hidden")
```

### 4. 多層次定位策略

#### 策略優先順序
1. **第一優先**: 使用者導向定位器
2. **第二優先**: 資料屬性定位器
3. **第三優先**: CSS 類別名稱
4. **最後手段**: JavaScript 直接操作

#### 實作範例
```python
def robust_element_click(page, element_description):
    """多層次元素定位和點擊"""
    
    # 策略 1: 角色型定位
    try:
        element = page.get_by_role("button", name=element_description)
        if element.is_visible():
            element.click()
            return True
    except:
        pass
    
    # 策略 2: 文字內容定位
    try:
        element = page.get_by_text(element_description)
        if element.is_visible():
            element.click()
            return True
    except:
        pass
    
    # 策略 3: CSS 選擇器
    try:
        element = page.locator(f"[data-testid='{element_description}']")
        if element.is_visible():
            element.click()
            return True
    except:
        pass
    
    # 策略 4: JavaScript 直接操作
    try:
        js_result = page.evaluate(f"""
            () => {{
                const elements = document.querySelectorAll('*');
                for (let el of elements) {{
                    if (el.textContent && el.textContent.includes('{element_description}')) {{
                        el.click();
                        return true;
                    }}
                }}
                return false;
            }}
        """)
        return js_result
    except:
        pass
    
    return False
```

## 常見陷阱與解決方案

### 陷阱 1: 過度依賴元素 ID
**問題**: 現代 Web 應用程式的元素 ID 經常是動態生成的
**解決**: 使用更穩定的定位方式

```python
# 脆弱的定位方式
page.click("#btn_1698745692341")

# 穩定的定位方式  
page.get_by_role("button", name="提交").click()
```

### 陷阱 2: 忽略頁面載入狀態
**問題**: 在頁面未完全載入時嘗試操作元素
**解決**: 確保頁面載入完成

```python
# 確保頁面載入完成
page.wait_for_load_state("networkidle")
page.wait_for_selector(".main-content")

# 然後再進行元素操作
page.get_by_role("button", name="搜尋").click()
```

### 陷阱 3: 單一定位策略
**問題**: 只使用一種定位方式，當該方式失效時測試中斷
**解決**: 實作容錯機制

```python
def safe_click(page, selectors_list):
    """嘗試多種選擇器直到成功"""
    for selector in selectors_list:
        try:
            element = page.locator(selector)
            if element.is_visible():
                element.click()
                return True
        except Exception as e:
            continue
    return False

# 使用範例
selectors = [
    "[data-testid='compare-btn']",
    ".compare-button",
    "button:has-text('比較')",
    "//button[contains(text(), '比較')]"
]
safe_click(page, selectors)
```

## 實用工具函式

### 元素存在性檢查
```python
def element_exists(page, selector, timeout=5000):
    """檢查元素是否存在"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        return True
    except:
        return False
```

### 智慧等待
```python
def smart_wait(page, condition_func, timeout=10):
    """智慧等待條件滿足"""
    import time
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(0.5)
    
    return False
```

### 錯誤恢復
```python
def retry_operation(operation_func, max_retries=3, delay=1):
    """重試機制"""
    import time
    
    for attempt in range(max_retries):
        try:
            return operation_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay)
    
    return None
```

## 最佳實踐總結

### 定位器穩定性排序（從高到低）
1. `get_by_role()` - 基於 ARIA 角色
2. `get_by_label()` - 基於標籤文字
3. `get_by_text()` - 基於可見文字
4. `get_by_testid()` - 基於測試 ID
5. `locator("[data-*]")` - 基於資料屬性
6. CSS 類別選擇器
7. CSS ID 選擇器（最不穩定）

### 效能最佳化建議
- 使用具體的定位器避免全頁搜尋
- 適當使用 `page.locator().first()` 限制範圍
- 善用 `page.locator().filter()` 精確定位
- 避免過度複雜的 CSS 選擇器

