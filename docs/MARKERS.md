# Test Markers Guide

Complete guide for using test markers in the automation framework.

## Overview

The framework uses pytest markers for test organization, categorization, and selective execution.

---

## Available Markers

### 1. Test Case ID Marker ✨

**Purpose:** Link tests to test case documentation  
**Format:** `@pytest.mark.testcase("TC-XX-NNN")`

**Test Case ID Patterns:**
- `TC-SD-###` - Sauce Demo
- `TC-TI-###` - The Internet
- `TC-MS-###` - Medusa Store
- `TC-RB-###` - Restful Booker API
- `TC-PS-###` - Petstore API
- `TC-OM-###` - OMDb API
- `TC-RQ-###` - ReqRes API

**Example:**
```python
@pytest.mark.testcase("TC-SD-001")
@pytest.mark.smoke
def test_login_successful():
    """TC-SD-001: Successful login with valid credentials"""
    pass
```

**Benefits:**
- ✅ Traceability to TEST_CASES.md
- ✅ Run tests by case ID: `pytest -m "testcase('TC-SD-001')"`
- ✅ Allure report integration
- ✅ Link to requirements/issues

---

### 2. Sm oke/Regression Markers

**Smoke Tests:**
```python
@pytest.mark.smoke
```
- **Purpose:** Critical path validation
- **Target:** 10-15 tests
- **Execution:** <10 minutes
- **Trigger:** Every PR, every push

**Regression Tests:**
```python
@pytest.mark.regression  # Optional, all tests are regression by default
```
- **Purpose:** Comprehensive coverage
- **Target:** All tests
- **Execution:** Full suite
- **Trigger:** Nightly, manual dispatch

---

### 3. Test Type Markers

**E2E Tests:**
```python
@pytest.mark.e2e
@pytest.mark.ui  # Alternative
```

**API Tests:**
```python
@pytest.mark.api
```

---

### 4. Performance Markers

**Slow Tests:**
```python
@pytest.mark.slow
```
- Tests taking >30 seconds
- Run separately: `pytest -m slow`
- Exclude from smoke: `pytest -m "smoke and not slow"`

---

### 5. Integration Markers

**Multi-component tests:**
```python
@pytest.mark.integration
```
- Tests spanning multiple services/components
- E2E flows involving APIs
- Cross-feature testing

---

### 6. Quality Markers

**Flaky Tests:**
```python
@pytest.mark.flaky
```
- Known unstable tests
- Needs investigation/fixing
- Can be excluded: `pytest -m "not flaky"`

**Critical Path:**
```python
@pytest.mark.critical
```
- Must-pass tests
- Business critical functionality
- Higher priority for failures

---

## Complete Example

```python
\"\"\"Sauce Demo - Authentication Tests.\"\"\"

import pytest
import allure
from playwright.sync_api import expect


@allure.epic("Sauce Demo")
@allure.feature("Authentication")
@allure.story("Login")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-001")
@pytest.mark.smoke
@pytest.mark.critical
def test_successful_login(login_page, inventory_page, sauce_demo_config):
    \"\"\"TC-SD-001: User can login with valid credentials.\"\"\"
    with allure.step("Navigate to login page"):
        login_page.attach()
    
    with allure.step("Enter valid credentials"):
        user = sauce_demo_config.test_users["standard"]
        login_page.login(user["username"], user["password"])
    
    with allure.step("Verify successful login"):
        expect(inventory_page.inventory_list).to_be_visible()
        expect(login_page.page).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )


@allure.epic("Sauce Demo")
@allure.feature("Authentication")
@allure.story("Login")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-002")
def test_invalid_password(login_page, sauce_demo_config):
    \"\"\"TC-SD-002: Login fails with invalid password.\"\"\"
    with allure.step("Navigate to login page"):
        login_page.attach()
    
    with allure.step("Enter invalid password"):
        user = sauce_demo_config.test_users["standard"]
        login_page.login(user["username"], "wrong_password")
    
    with allure.step("Verify error message"):
        error = login_page.get_error_message()
        assert "Username and password do not match" in error
```

---

## Running Tests by Markers

### By Test Case ID

```bash
# Single test case
pytest --testcase-id="TC-SD-001"

# Multiple test cases (using -k keyword matching)
pytest -k "TC-SD-001 or TC-SD-002"

# All Sauce Demo test cases
pytest -k "TC-SD"
```

### By Category

```bash
# Smoke tests only
pytest -m smoke

# Smoke tests, parallel
pytest -m smoke -n auto

# Regression (all tests)
pytest -m regression  # or just: pytest

# API tests only
pytest -m api

# E2E tests only
pytest -m e2e
```

### Combined Markers

```bash
# Smoke E2E tests
pytest -m "smoke and e2e"

# API tests except slow
pytest -m "api and not slow"

# Critical tests only
pytest -m critical

# Non-flaky tests
pytest -m "not flaky"
```

---

## Smoke Test Selection Criteria

✅ **Include in Smoke Suite:**
- Login/authentication flows
- Core API endpoints (GET, POST)
- Critical user journeys
- Fast execution (<30s each)
- Stable, not flaky
- High business value

❌ **Exclude from Smoke Suite:**
- Comprehensive validation tests
- Edge cases and error scenarios
- Slow tests (>30s)
- Tests with external dependencies
- Nice-to-have features

---

## Marker Guidelines

**DO:**
- ✅ Add `@pytest.mark.testcase()` to all tests
- ✅ Mark 10-15 critical tests as smoke
- ✅ Use descriptive test IDs matching TEST_CASES.md
- ✅ Keep smoke suite fast (<10 min total)
- ✅ Document flaky tests

**DON'T:**
- ❌ Over-use smoke marker (keep it selective)
- ❌ Use undefined markers (add to pytest.ini first)
- ❌ Mix test case IDs between apps
- ❌ Skip test case IDs on new tests

---

## Allure Integration

Test case IDs automatically appear in Allure reports:

```python
@pytest.mark.testcase("TC-SD-001")
def test_example():
    pass
```

In Allure report:
- Shows test case ID in test details
- Filterable by test case
- Linkable to external test management tools

---

## Adding Markers to New Tests

**Template:**
```python
@allure.epic("App Name")
@allure.feature("Feature Name")
@pytest.mark.app("app_name")
@pytest.mark.e2e  # or @pytest.mark.api
@pytest.mark.testcase("TC-XX-###")
@pytest.mark.smoke  # Only if critical path
def test_something():
    \"\"\"TC-XX-###: Test description.\"\"\"
    pass
```

---

## Next Steps

1. **Add markers to existing tests** (gradual process)
2. **Update TEST_CASES.md** with test case IDs
3. **Define smoke suite** (10-15 tests)
4. **Run smoke tests** to verify speed
5. **Update CI/CD** to use smoke markers

---

**See also:**
- [pytest.ini](../pytest.ini) - Marker definitions
- [TEST_CASES.md](../apps/*/TEST_CASES.md) - Test case documentation
- [CI/CD Guide](CICD.md) - Workflow integration
