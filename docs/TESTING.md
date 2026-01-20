# Testing Guide

Comprehensive guide for running, organizing, and debugging tests in the Playwright-Pytest framework.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Running Tests](#running-tests) 
- [Test Selection](#test-selection)
- [Parallel Execution](#parallel-execution)
- [Debugging](#debugging)
- [Reporting](#reporting)
- [Best Practices](#best-practices)

---

## Quick Reference

```bash
# All tests
pytest

# Specific app
pytest apps/e2e/sauce_demo/

# By marker
pytest -m smoke

# Parallel (4 workers)
pytest -n 4

# With Allure
pytest --alluredir=test-results/allure-results

# Headful (visible browser)
pytest --headed

# Debug mode
pytest -s --headed --slowmo 1000
```

---

## Running Tests

### Basic Execution

```bash
# Run all tests (86 tests, ~3-5 min)
pytest

# Verbose output with test names
pytest -v

# Very verbose (show print statements)
pytest -vv

# Show local variables on failure
pytest -l

# Exit on first failure
pytest -x

# Exit after N failures
pytest --maxfail=3
```

### By Directory

```bash
# All E2E tests (45 tests)
pytest apps/e2e/

# All API tests (41 tests)
pytest apps/api/

# Specific application
pytest apps/e2e/sauce_demo/        # 19 tests
pytest apps/e2e/the_internet/      # 25 tests
pytest apps/e2e/medusa_store/      # 1 test
pytest apps/api/restful_booker/    # 13 tests
pytest apps/api/petstore/          # 9 tests
pytest apps/api/omdb/              # 5 tests
pytest apps/api/reqres/            # 14 tests
```

### By Test File

```bash
# Single test file
pytest apps/e2e/sauce_demo/tests/e2e/test_login.py

# Multiple files
pytest apps/e2e/sauce_demo/tests/e2e/test_login.py \
       apps/e2e/sauce_demo/tests/e2e/test_cart.py
```

### By Test Name

```bash
# Specific test function
pytest apps/e2e/sauce_demo/tests/e2e/test_login.py::test_login_successful

# Test class
pytest apps/e2e/sauce_demo/tests/e2e/test_login.py::TestLogin

# Pattern matching (-k)
pytest -k "login"           # All tests with "login" in name
pytest -k "not slow"        # Exclude tests with "slow" in name
pytest -k "login and success"  # Combine filters
```

---

## Test Selection

### By Marker

Tests are tagged with markers for easy filtering:

```python
@pytest.mark.app("sauce_demo")   # App assignment
@pytest.mark.e2e                 # E2E UI test
@pytest.mark.api                 # API test
@pytest.mark.smoke               # Critical path
@pytest.mark.regression          # Full regression
```

**Run examples:**
```bash
# All E2E tests
pytest -m e2e

# All API tests
pytest -m api

# Smoke tests only
pytest -m smoke

# Regression suite
pytest -m regression

# Specific app
pytest -m "app == 'sauce_demo'"

# Combine markers
pytest -m "smoke and e2e"
pytest -m "smoke and not slow"
pytest -m "e2e or api"
```

### By Configuration

```bash
# Run tests for specific environment
pytest --env=staging

# Different browser
pytest --browser=firefox
pytest --browser=webkit
```

---

## Parallel Execution

Speed up test execution with pytest-xdist:

```bash
# Run with 4 workers
pytest -n 4

# Auto-detect CPU cores
pytest -n auto

# Distribute by file (faster startup)
pytest -n 4 --dist=loadfile apps/e2e/

# Distribute by test (better balance)
pytest -n 4 --dist=loadscope
```

**Performance comparison:**
```
Sequential:  ~5 minutes (86 tests)
4 workers:   ~1.5 minutes (86 tests)
8 workers:   ~1 minute (86 tests)
```

**Note:** Some E2E tests may be slower in parallel due to browser overhead.

---

## Debugging

### Visual Debugging

```bash
# Headful mode (see browser)
pytest --headed apps/e2e/

# Slow motion (500ms delay between actions)
pytest --headed --slowmo 500

# Pause before closing browser
pytest --headed --pause-on-failure
```

### Debug Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Full stack trace
pytest --tb=long

# Short stack trace
pytest --tb=short

# No stack trace
pytest --tb=no
```

### Capture Artifacts

```bash
# Record video on failure
pytest --video=retain-on-failure

# Record video always
pytest --video=on

# Enable tracing
pytest --tracing=on

# Save screenshots on failure
pytest --screenshot=only-on-failure
```

### Interactive Debugging

```python
# Add to test for breakpoint
def test_example():
    breakpoint()  # Debugger stops here
    assert True
```

```bash
# Run with debugger
pytest --pdb                      # Drop to pdb on failure
pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb  # Use ipdb
```

---

## Reporting

### Terminal Output

```bash
# Quiet mode (minimal output)
pytest -q

# Verbose (show test names)
pytest -v

# Very verbose (detailed output)
pytest -vv

# Show summary
pytest -ra  # All except passes
pytest -rA  # Include passes
```

### Allure Reports

```bash
# 1. Run tests with Allure
pytest --alluredir=test-results/allure-results

# 2. Generate report
allure generate test-results/allure-results \
               -o test-results/allure-report \
               --clean

# 3. Open report
allure open test-results/allure-report
```

**Single command:**
```bash
# Generate and open
allure serve test-results/allure-results
```

### JUnit XML

```bash
# Generate JUnit XML (for CI/CD)
pytest --junit-xml=test-results/junit.xml
```

---

## Test Organization

### Directory Structure

```
apps/
├── e2e/
│   └── sauce_demo/
│       ├── pages/              # Page Objects
│       │   ├── __init__.py
│       │   ├── login_page.py
│       │   └── inventory_page.py
│       ├── tests/
│       │   ├── conftest.py     # App fixtures
│       │   └── e2e/
│       │       ├── test_login.py
│       │       └── test_cart.py
│       ├── conftest.py         # App config
│       └── TEST_CASES.md       # Test scenarios
└── api/
    └── restful_booker/
        ├── clients/            # API clients
        ├── tests/              # API tests
        └── conftest.py
```

### Test Naming Convention

```python
# File naming
test_<feature>.py          # ✅ Good
<feature>_test.py          # ❌ Not recommended

# Class naming (optional)
class TestLogin:           # ✅ PascalCase + Test prefix
class LoginTests:          # ❌ No Test prefix

# Function naming
def test_login_successful():           # ✅ Descriptive
def test_invalid_creds():              # ✅ Short but clear
def test1():                           # ❌ Not descriptive
```

---

## Best Practices

### 1. Organize by Feature

```bash
# Group related tests
apps/e2e/sauce_demo/tests/e2e/
├── test_login.py          # All login scenarios
├── test_cart.py           # All cart scenarios
└── test_checkout.py       # All checkout scenarios
```

### 2. Use Fixtures

```python
# Reuse setup logic
@pytest.fixture
def logged_in_user(login_page):
    """Pre-authenticated user."""
    login_page.login("standard_user", "secret_sauce")
    yield
    # Cleanup after test

def test_add_to_cart(logged_in_user, inventory_page):
    # Test starts already logged in
    inventory_page.add_first_item_to_cart()
```

### 3. Tag Appropriately

```python
@pytest.mark.smoke           # Critical path
@pytest.mark.regression      # Full regression
@pytest.mark.slow            # Long-running test
@pytest.mark.skip("WIP")     # Work in progress
```

### 4. Write Clear Assertions

```python
# ✅ Good: Descriptive message
assert user_name == "John", f"Expected 'John', got '{user_name}'"

# ✅ Good: Use Playwright assertions
expect(page.locator("#username")).to_have_text("John")

# ❌ Bad: No context
assert user_name == "John"
```

### 5. Clean Up Resources

```python
@pytest.fixture
def api_booking(booker_client):
    # Setup
    booking = booker_client.create_booking({...})
    
    yield booking
    
    # Teardown (always runs)
    booker_client.delete_booking(booking["id"])
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          playwright install chromium --with-deps
      
      - name: Run tests
        run: |
          pytest -n auto --alluredir=test-results/allure-results
      
      - name: Generate report
        if: always()
        run: |
          allure generate test-results/allure-results \
                         -o test-results/allure-report
      
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: allure-report
          path: test-results/allure-report
```

---

## Troubleshooting

### Tests Hanging

```bash
# Set timeout
pytest --timeout=300  # 5 minutes per test

# Kill hung processes
pkill -f pytest
```

### Flaky Tests

```bash
# Rerun failures
pytest --reruns 3 --reruns-delay 1

# Run failed tests first
pytest --lf

# Show flaky tests
pytest --alluredir=results
# Check Allure report for retry statistics
```

### Port Conflicts

```bash
# Kill process on port
lsof -ti:3000 | xargs kill -9

# Or change port in config
```

---

## Next Steps

- [Page Objects Guide](PAGE_OBJECTS.md) - Build maintainable tests
- [Decorator Guide](DECORATOR_GUIDE.md) - Use Allure decorators
- [README](../README.md) - Return to main documentation

---

**Happy Testing!** 🧪
