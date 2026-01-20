# Decorator Guide

This guide explains the decorators used in the test framework and when to use each.

---

## Quick Reference

| Decorator | Purpose | Required? |
|-----------|---------|-----------|
| `@pytest.mark.app("name")` | Assign test to an app | **Yes** for app-specific tests |
| `@pytest.mark.smoke` | Tag as smoke test | Optional |
| `@allure.epic("Name")` | Top-level grouping in report | Optional |
| `@allure.feature("Name")` | Feature grouping in report | Optional |
| `@allure.title("...")` | Test title in report | Optional |

---

## Pytest Markers (Test Selection)

**Purpose**: Control which tests run via command line.

### `@pytest.mark.app("app_name")`

Assigns a test to a specific application. The test will use that app's configuration.

```python
@pytest.mark.app("sauce_demo")
def test_login(current_app):
    current_app.navigate("/")  # Uses sauce_demo base URL
```

**CLI usage**:
```bash
pytest apps/e2e/sauce_demo/  # Run by directory
pytest -m "app"              # All app-marked tests
```

### `@pytest.mark.smoke`

Quick validation tests. Run these for fast feedback.

```python
@pytest.mark.smoke
def test_homepage_loads(page):
    ...
```

**CLI usage**:
```bash
pytest -m smoke              # Only smoke tests
pytest -m "smoke and app"    # Smoke tests with app marker
```

### `@pytest.mark.regression`

Comprehensive tests for full coverage.

```python
@pytest.mark.regression
def test_all_form_validations(page):
    ...
```

### Other markers

| Marker | Use case |
|--------|----------|
| `@pytest.mark.slow` | Tests that take >30 seconds |
| `@pytest.mark.flaky` | Known unstable tests |
| `@pytest.mark.api` | API tests |
| `@pytest.mark.ui` | UI/E2E tests |

---

## Allure Decorators (Report Organization)

**Purpose**: Organize and enhance Allure HTML reports. No effect on test execution.

### `@allure.epic("Epic Name")`

Top-level grouping. Usually the application or product area.

```python
@allure.epic("Sauce Demo")
class TestLogin:
    ...
```

### `@allure.feature("Feature Name")`

Feature or module within the epic.

```python
@allure.epic("Sauce Demo")
@allure.feature("Authentication")
class TestLogin:
    ...
```

### `@allure.story("Story Name")`

User story or scenario within the feature.

```python
@allure.story("User Login")
def test_successful_login():
    ...
```

### `@allure.title("Descriptive Title")`

Human-readable test title (replaces function name in report).

```python
@allure.title("Login with valid credentials")
def test_login_valid():
    ...
```

### `@allure.description("...")`

Detailed test description.

```python
@allure.description("This test verifies that users can login with valid credentials")
def test_login():
    ...
```

### `@allure.severity(level)`

Test importance level.

```python
from allure import severity_level

@allure.severity(severity_level.CRITICAL)
def test_checkout():
    ...

# Levels: BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL
```

---

## Complete Example

```python
import allure
import pytest


@allure.epic("Sauce Demo")
@allure.feature("Authentication")
@pytest.mark.app("sauce_demo")
@pytest.mark.smoke
class TestLogin:
    """Test suite for Sauce Demo login functionality."""

    @allure.story("Successful Login")
    @allure.title("Login with standard_user credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, current_app):
        """Test successful login with valid credentials."""
        with allure.step("Navigate to login page"):
            current_app.navigate("/")

        with allure.step("Enter credentials"):
            # ... login logic

        with allure.step("Verify dashboard"):
            # ... verification

    @allure.story("Failed Login")
    @allure.title("Login fails with invalid password")
    @pytest.mark.regression
    def test_invalid_password(self, current_app):
        ...
```

---

## Using `allure.step` for Detailed Reporting

Use `with allure.step()` to create step-by-step logs in the report:

```python
def test_checkout_flow(self, current_app):
    with allure.step("Add product to cart"):
        # ... add product

    with allure.step("Navigate to cart"):
        # ... go to cart

    with allure.step("Complete checkout"):
        # ... checkout steps
```

---

## Best Practices

1. **Always use `@pytest.mark.app`** for app-specific tests
2. **Use `@allure.epic` at class level** for consistent grouping
3. **Use `@allure.title`** for human-readable test names
4. **Use `allure.step()`** for important actions within tests
5. **Combine pytest markers** for flexible test selection:
   ```bash
   pytest -m "smoke and not slow"
   ```

---

## Viewing Reports

```bash
# Generate and open Allure report
make report

# Or manually
allure generate test-results/allure-results -o test-results/allure-report
allure open test-results/allure-report
```
