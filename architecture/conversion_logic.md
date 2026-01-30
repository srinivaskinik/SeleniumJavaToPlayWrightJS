# SOP: Selenium Java to Playwright TS Conversion Logic

## 1. Core Principles
- **Async/Await**: All Playwright interactions must be awaited.
- **Locators**: Prefer `user-facing` locators (Role, Text) where possible, but fallback to CSS/XPath for strict migration.
- **Assertions**: Convert JUnit/TestNG assertions to `expect()` wrappers.

## 2. Locator Mapping Strategy

| Source (Java) | Target (Playwright TS) | Note |
| :--- | :--- | :--- |
| `By.id("foo")` | `page.locator('#foo')` | |
| `By.cssSelector(".bar")` | `page.locator('.bar')` | |
| `By.xpath("//div")` | `page.locator('//div')` | |
| `By.name("baz")` | `page.locator('[name="baz"]')` | |
| `By.className("cls")` | `page.locator('.cls')` | Handle multiple classes carefully |
| `By.linkText("Click Me")` | `page.getByText('Click Me', { exact: true })` | |
| `By.partialLinkText("Click")` | `page.getByText('Click')` | |

## 3. Action Mapping Strategy

| Source (Java) | Target (Playwright TS) | Note |
| :--- | :--- | :--- |
| `.click()` | `await .click()` | |
| `.sendKeys("text")` | `await .fill("text")` | `fill` clears and types. `type` appends. Prefer `fill`. |
| `.getText()` | `await .innerText()` | |
| `.getAttribute("href")` | `await .getAttribute('href')` | |
| `.isDisplayed()` | `await .isVisible()` | Usually used inside an assertion |
| `driver.get("url")` | `await page.goto("url")` | |
| `driver.navigate().to("url")` | `await page.goto("url")` | |

## 4. Wait Strategy

**Rule:** Remove explicit `WebDriverWait` blocks. Replace with auto-retrying assertions.

**Pattern:**
```java
WebDriverWait wait = new WebDriverWait(driver, 10);
wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("foo")));
```

**Target:**
*Implicitly handled by the next action or assertion.*
```typescript
await expect(page.locator('#foo')).toBeVisible();
```

## 5. Assertion Mapping

| Source (Java) | Target (Playwright TS) |
| :--- | :--- |
| `assertEquals(a, b)` | `expect(a).toBe(b)` |
| `assertTrue(elem.isDisplayed())` | `await expect(locator).toBeVisible()` |
| `assertTrue(elem.getText().contains("foo"))` | `await expect(locator).toContainText("foo")` |

## 6. Structure Skeleton

**Input (Java Class):**
```java
public class LoginTest {
    @Test
    public void testLogin() { ... }
}
```

**Output (Playwright Spec):**
```typescript
import { test, expect } from '@playwright/test';

test('testLogin', async ({ page }) => {
    // ... converted steps
});
```
