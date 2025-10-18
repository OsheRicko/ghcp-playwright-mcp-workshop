# Playwright Best Practices
## Use locators
In order to write end to end tests we need to first find elements on the webpage. We can do this by using Playwright's built in locators. Locators come with auto waiting and retry-ability. Auto waiting means that Playwright performs a range of actionability checks on the elements, such as ensuring the element is visible and enabled before it performs the click. To make tests resilient, we recommend prioritizing user-facing attributes and explicit contracts.

### Good locator examples
```python
page.get_by_role('button', name='submit')
```
### Use chaining and filtering
- Locators can be chained to narrow down the search to a particular part of the page.
    ```python
    product = page.get_by_role('listitem').filter(has_text='Product 2')
    ```
- You can also filter locators by text or by another locator.
    ```python
    page.get_by_role('listitem').filter(has_text='Product 2').get_by_role('button', name='Add to cart').click()
    ```
### Prefer user-facing attributes to XPath or CSS selectors
Your DOM can easily change so having your tests depend on your DOM structure can lead to failing tests. For example consider selecting this button by its CSS classes. Should the designer change something then the class might change, thus breaking your test.

#### Bad example
```python
page.locator('button.buttonIcon.episode-actions-later')
```

#### Good example
Use locators that are resilient to changes in the DOM.
```python
page.get_by_role('button', name='submit')
```

## Use web first assertions
Assertions are a way to verify that the expected result and the actual result matched or not. By using web first assertions Playwright will wait until the expected condition is met. For example, when testing an alert message, a test would click a button that makes a message appear and check that the alert message is there. If the alert message takes half a second to appear, assertions such as to_be_visible() will wait and retry if needed.

### Good example
```python
expect(page.get_by_text('welcome')).to_be_visible()
```
### Bad example
```python
expect(page.get_by_text('welcome').is_visible()).to_be(True)
```
### Don't use manual assertions
Don't use manual assertions that are not awaiting the expect. In the code below the await is inside the expect rather than before it. When using assertions such as is_visible() the test won't wait a single second, it will just check the locator is there and return immediately.

#### Bad example
```python
expect(page.get_by_text('welcome').is_visible()).to_be(True)
```

#### Good example
Use web first assertions such as to_be_visible() instead.
```python
expect(page.get_by_text('welcome')).to_be_visible()
```