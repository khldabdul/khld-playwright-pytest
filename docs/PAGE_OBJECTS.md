# Page Object Model Guide

Complete guide to using and creating Page Objects in the Playwright-Pytest framework.

## Table of Contents

- [What is Page Object Model?](#what-is-page-object-model)
- [Benefits](#benefits)
- [Basic Structure](#basic-structure)
- [Creating Page Objects](#creating-page-objects)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Advanced Patterns](#advanced-patterns)

---

## What is Page Object Model?

Page Object Model (POM) is a design pattern that creates an object repository for web UI elements. Each page of the application has a corresponding Page Object class that encapsulates:
- Web elements (locators)
- Actions on those elements
- Page-specific logic

```
Test ←→ Page Object ←→ Web Page
```

---

## Benefits

✅ **Maintainability** - UI changes require updates in one place  
✅ **Reusability** - Page objects used across multiple tests  
✅ **Readability** - Tests read like business logic  
✅ **Less Code Duplication** - Common actions centralized  
✅ **Easier Debugging** - Clear separation of concerns

---

## Basic Structure

### Directory Layout

```
apps/e2e/sauce_demo/
├── pages/
│   ├── __init__.py        # Export all pages
│   ├── base_page.py       # Shared functionality
│   ├── login_page.py      # Login page object
│   ├── inventory_page.py  # Product listing
│   └── cart_page.py       # Shopping cart
└── tests/
    └── e2e/
        ├── test_login.py  # Login tests
        └── test_cart.py   # Cart tests
```

### Page Object Template

```python
"""Login Page Object."""

import allure
from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for Sauce Demo login page."""
    
    def __init__(self, page: Page):
        """Initialize with Playwright page."""
        self.page = page
        
        # Locators
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")
    
    @allure.step("Navigate to login page")
    def navigate(self, base_url: str):
        """Navigate to login page."""
        self.page.goto(base_url)
    
    @allure.step("Login with {username}")
    def login(self, username: str, password: str):
        """Perform login action."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    @allure.step("Verify login error")
    def verify_error(self, expected_text: str):
        """Verify error message."""
        expect(self.error_message).to_contain_text(expected_text)
```

---

## Creating Page Objects

### Step 1: Identify Page Elements

Inspect the page and identify:
- Input fields
- Buttons
- Links
- Text elements
- Containers

### Step 2: Define Locators

```python
class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Prefer data-testid or unique IDs
        self.add_to_cart_button = page.locator("[data-test='add-to-cart']")
        
        # Use CSS selectors for complex elements
        self.product_title = page.locator(".inventory_item_name")
        
        # Use text for stable elements
        self.checkout_button = page.get_by_role("button", name="Checkout")
        
        # Parametrized locators (see advanced patterns)
        self.product_by_name = lambda name: page.locator(
            f"text={name}"
        ).locator("../..")  # Navigate to parent
```

### Step 3: Add Actions

```python
    @allure.step("Add {product_name} to cart")
    def add_product_to_cart(self, product_name: str):
        """Add specific product to cart."""
        product = self.product_by_name(product_name)
        product.locator("[data-test^='add-to-cart']").click()
    
    @allure.step("Get product count")
    def get_product_count(self) -> int:
        """Get number of products on page."""
        return self.product_title.count()
```

### Step 4: Add Verifications

```python
    @allure.step("Verify product exists: {product_name}")
    def verify_product_exists(self, product_name: str):
        """Verify product is visible."""
        expect(self.product_by_name(product_name)).to_be_visible()
    
    @allure.step("Verify cart badge shows {count}")
    def verify_cart_count(self, count: int):
        """Verify shopping cart badge."""
        cart_badge = self.page.locator(".shopping_cart_badge")
        expect(cart_badge).to_have_text(str(count))
```

---

## Best Practices

### 1. Single Responsibility

Each Page Object represents ONE page or component:

```python
# ✅ Good: Focused page object
class LoginPage:
    """Only login functionality."""
    pass

class InventoryPage:
    """Only product listing."""
    pass

# ❌ Bad: Mixed responsibilities
class LoginAndInventoryPage:
    """Handles both login and products."""
    pass
```

### 2. Return Page Objects

Methods that navigate should return the target page:

```python
class LoginPage:
    def login(self, username: str, password: str) -> 'InventoryPage':
        """Login and return inventory page."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        
        # Return next page for chaining
        from .inventory_page import InventoryPage
        return InventoryPage(self.page)

# Usage in test
def test_add_to_cart(login_page):
    inventory = login_page.login("user", "pass")
    inventory.add_product_to_cart("Backpack")
```

### 3. Use Allure Steps

Wrap actions with `@allure.step()` for reporting:

```python
@allure.step("Fill shipping address")
def fill_shipping_address(self, address_data: dict):
    """Fill shipping form."""
    self.first_name.fill(address_data["first_name"])
    self.last_name.fill(address_data["last_name"])
    # Allure report shows "Fill shipping address" as a step
```

### 4. Hide Implementation Details

Tests shouldn't know about locators:

```python
# ✅ Good: Test doesn't know about locators
def test_login():
    login_page.login("user", "pass")
    assert login_page.is_logged_in()

# ❌ Bad: Test knows too much
def test_login():
    page.locator("#username").fill("user")
    page.locator("#password").fill("pass")
    page.locator("button").click()
```

### 5. Group Related Locators

```python
class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Shipping form locators
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        
        # Payment locators
        self.card_number = page.locator("#card-number")
        self.cvv = page.locator("#cvv")
```

### 6. Use Type Hints

```python
from typing import List

class InventoryPage:
    def get_product_names(self) -> List[str]:
        """Get all product names."""
        return [
            el.inner_text() 
            for el in self.product_title.all()
        ]
```

---

## Examples

### E2E Page Object

```python
"""Sauce Demo Cart Page."""

import allure
from playwright.sync_api import Page, expect


class CartPage:
    """Shopping cart page object."""
    
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("#checkout")
        self.continue_shopping = page.locator("#continue-shopping")
        self.remove_button = page.locator("[data-test^='remove']")
    
    @allure.step("Navigate to cart")
    def navigate_to_cart(self):
        """Click cart icon."""
        self.page.locator(".shopping_cart_link").click()
    
    @allure.step("Get cart item count")
    def get_item_count(self) -> int:
        """Return number of items in cart."""
        return self.cart_items.count()
    
    @allure.step("Remove item at index {index}")
    def remove_item(self, index: int = 0):
        """Remove item from cart."""
        self.remove_button.nth(index).click()
    
    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        """Click checkout button."""
        self.checkout_button.click()
        
        from .checkout_page import CheckoutPage
        return CheckoutPage(self.page)
    
    @allure.step("Verify cart has {count} items")
    def verify_item_count(self, count: int):
        """Verify number of items."""
        expect(self.cart_items).to_have_count(count)
```

### API Client (Page Object for APIs)

```python
"""Restful Booker API Client."""

import allure
import requests
from typing import Dict, Any


class RestfulBookerClient:
    """API client for Restful Booker."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
    
    @allure.step("Authenticate")
    def authenticate(self, username: str, password: str) -> str:
        """Get auth token."""
        response = self.session.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        self.token = response.json()["token"]
        return self.token
    
    @allure.step("Create booking")
    def create_booking(self, booking_data: Dict[str, Any]) -> Dict:
        """Create a new booking."""
        response = self.session.post(
            f"{self.base_url}/booking",
            json=booking_data
        )
        response.raise_for_status()
        return response.json()
    
    @allure.step("Get booking {booking_id}")
    def get_booking(self, booking_id: int) -> Dict:
        """Retrieve booking by ID."""
        response = self.session.get(
            f"{self.base_url}/booking/{booking_id}"
        )
        response.raise_for_status()
        return response.json()
```

---

## Advanced Patterns

### 1. Base Page Class

Share common functionality:

```python
"""Base page for all page objects."""

from playwright.sync_api import Page
import allure


class BasePage:
    """Base class with shared functionality."""
    
    def __init__(self, page: Page):
        self.page = page
    
    @allure.step("Navigate to {url}")
    def navigate(self, url: str):
        """Navigate to URL."""
        self.page.goto(url)
    
    @allure.step("Wait for page load")
    def wait_for_load(self):
        """Wait for page to be fully loaded."""
        self.page.wait_for_load_state("networkidle")
    
    def take_screenshot(self, name: str):
        """Take screenshot."""
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )


# Inherit from BasePage
class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.locator("#username")
```

### 2. Component Objects

For reusable components:

```python
"""Header component."""

class HeaderComponent:
    """Reusable header navigation."""
    
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator(".shopping_cart_link")
        self.menu_button = page.locator("#react-burger-menu-btn")
    
    def open_cart(self):
        """Navigate to cart."""
        self.cart_link.click()
    
    def get_cart_count(self) -> int:
        """Get cart badge count."""
        badge = self.page.locator(".shopping_cart_badge")
        return int(badge.inner_text()) if badge.is_visible() else 0


# Use in page objects
class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = HeaderComponent(page)  # Reusable component
    
    def go_to_cart(self):
        """Use header component."""
        self.header.open_cart()
```

### 3. Fluent Interface

Chain method calls:

```python
class CheckoutPage:
    def fill_first_name(self, name: str) -> 'CheckoutPage':
        self.first_name.fill(name)
        return self
    
    def fill_last_name(self, name: str) -> 'CheckoutPage':
        self.last_name.fill(name)
        return self
    
    def submit(self):
        self.continue_button.click()

# Usage: Chain calls
checkout_page \
    .fill_first_name("John") \
    .fill_last_name("Doe") \
    .submit()
```

---

## Testing Page Objects

Page Objects themselves can be tested:

```python
def test_login_page_locators(page):
    """Verify login page locators exist."""
    login = LoginPage(page)
    login.navigate("https://saucedemo.com")
    
    assert login.username_input.is_visible()
    assert login.password_input.is_visible()
    assert login.login_button.is_visible()
```

---

## Common Mistakes

### ❌ Don't Assert in Page Objects

```python
# ❌ Bad: Assert in page object
class LoginPage:
    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()
        assert self.page.url.endswith("/inventory")  # ❌

# ✅ Good: Return state, assert in test
class LoginPage:
    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()
    
    def is_logged_in(self) -> bool:
        return self.page.url.endswith("/inventory")

# Test does assertion
def test_login():
    login_page.login("user", "pass")
    assert login_page.is_logged_in()  # ✅
```

### ❌ Don't Put Test Logic in Page Objects

```python
# ❌ Bad: Business logic in page object
class  CartPage:
    def verify_checkout_flow(self):
        # Too much test logic here
        pass

# ✅ Good: Keep in test
def test_checkout_flow(cart_page):
    cart_page.add_item()
    cart_page.proceed_to_checkout()
    # Test orchestrates the flow
```

---

## Next Steps

- [Testing Guide](TESTING.md) - Run your tests
- [Decorator Guide](DECORATOR_GUIDE.md) - Use Allure steps
- Study existing page objects in `apps/e2e/*/pages/`

---

**Build maintainable tests with Page Objects!** 🏗️
