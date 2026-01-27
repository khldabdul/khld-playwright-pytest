# Playwright-Pytest Automation Framework

A production-ready Python automation testing framework using Playwright and pytest with multi-app architecture, Page Object Model, and comprehensive test coverage.

[![Tests](https://img.shields.io/badge/tests-86%2F86-success)](.) 
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](.)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org)
[![Playwright](https://img.shields.io/badge/playwright-latest-green)](https://playwright.dev)

## 📊 Test Statistics

**Total: 92/92 tests passing (100%)**

| Category | Tests | Status |
|----------|-------|--------|
| **E2E Tests** | **51** | ✅ 100% |
| └─ Sauce Demo | 19 | ✅ Complete |
| └─ The Internet | 25 | ✅ Complete |
| └─ Medusa Store | 7 | ✅ Complete |
| **API Tests** | **41** | ✅ 100% |
| └─ Restful Booker | 13 | ✅ Complete |
| └─ Petstore | 9 | ✅ Complete |
| └─ OMDb | 5 | ✅ Complete |
| └─ ReqRes | 14 | ✅ Complete |

**Average Execution Time:** ~3-5 minutes (all tests)  
**Success Rate:** 100%

## 🚀 Features

- **Multi-App Architecture** - Test multiple web applications and APIs from one framework
- **Page Object Model** - Clean separation of test logic and page interactions
- **Allure Reporting** - Rich HTML reports with screenshots, traces, and test history
- **100% Test Coverage** - All implemented tests passing consistently
- **API Testing** - RESTful API tests with full CRUD coverage
- **Environment Support** - Dev, staging, and production configurations
- **Parallel Execution Ready** - pytest-xdist support for faster test runs

## 📁 Project Structure

```
playwright-pytest/
├── apps/                    # All test applications
│   ├── e2e/                 # E2E/UI Tests
│   │   ├── sauce_demo/      # 19 tests - E-commerce flow
│   │   ├── the_internet/    # 25 tests - Component testing
│   │   └── medusa_store/    # 1 test - Modern Next.js checkout
│   └── api/                 # API Tests
│       ├── restful_booker/  # 13 tests - CRUD + Token Auth
│       ├── petstore/        # 9 tests - OpenAPI/Swagger
│       ├── omdb/            # 5 tests - Search & data retrieval
│       └── reqres/          # 14 tests - User/Resource CRUD
├── config/
│   ├── apps/                # Per-app YAML configurations
│   ├── environments.yml     # Environment settings
│   └── test_data.yml        # Shared test data
├── infrastructure/
│   ├── fixtures/            # Shared pytest fixtures
│   ├── hooks/               # Allure integration hooks
│   └── utils/               # Utility functions
├── pages/                   # Shared/base page objects
├── docs/
│   ├── SETUP.md            # Detailed setup instructions
│   ├── TESTING.md          # Test execution guide
│   ├── PAGE_OBJECTS.md     # Page Object patterns
│   └── DECORATOR_GUIDE.md  # Pytest vs Allure decorators
├── conftest.py             # Root pytest configuration
├── pytest.ini              # Pytest settings
└── pyproject.toml          # Python project config
```

## 🛠 Installation

### Prerequisites
- Python 3.11+ ([pyenv](https://github.com/pyenv/pyenv) recommended)
- Git

### ⚠️ Virtual Environment Note

**All `python`, `pip`, and `pytest` commands require your virtual environment to be activated.**

Look for the `(.venv)` prefix in your terminal prompt. If you don't see it, activate first:

```bash
# Activate virtual environment (run this whenever you open a new terminal)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# You should see (.venv) in your prompt now
```

### pyenv Setup (if using pyenv)

If you have pyenv installed but `python` command is not found, you need to initialize it:

```bash
# Install Python 3.11 (if not already installed)
pyenv install 3.11

# Set it as global or local version
pyenv local 3.11  # Creates .python-version file

# Initialize pyenv in your current shell
eval "$(pyenv init -)"

# Verify Python is available
python --version
```

**Make it permanent:** Add this to your shell config (`~/.zshrc` or `~/.bashrc`):
```bash
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### Setup Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd playwright-pytest

# 2. Create virtual environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
# You should now see (.venv) in your prompt

# 3. Install dependencies
(.venv) $ pip install -e ".[dev]"

# 4. Install Playwright browsers
(.venv) $ playwright install chromium

# 5. Configure API keys (optional, for OMDb tests)
(.venv) $ echo "OMDB_API_KEY=your_key_here" > .env
```

**Note:** ReqRes API key is pre-configured. OMDb requires your own API key from [omdbapi.com](http://www.omdbapi.com/apikey.aspx).

**Version Compatibility Note:**
- The framework requires `pytest >= 8.0.0, < 9.0.0` and `allure-pytest >= 2.15.0` for proper Allure integration
- These versions are automatically installed when running `make setup` or `pip install -e ".[dev]"`
- Pytest 9.0+ has breaking API changes that are incompatible with current allure-pytest versions

## ⚡ Quick Start

**Ensure virtual environment is activated before running any commands:**
```bash
source venv/bin/activate  # You should see (.venv) in prompt
```

### 🚀 Using Make Shortcuts (Recommended!)

The project includes a **Makefile** with convenient shortcuts so you don't need to remember long commands.

```bash
# See all available commands
$ make help
```

**Common commands:**

| Command | What it does |
|---------|--------------|
| `make setup` | Full setup (install deps + browsers) |
| `make test` | Run all tests with Allure results |
| `make test-smoke` | Run smoke tests only |
| `make test-api` | Run API tests (parallel) |
| `make test-e2e` | Run E2E tests only |
| `make test-sauce-demo` | Run Sauce Demo tests |
| `make test-the-internet` | Run The Internet tests |
| `make test-parallel` | Run all tests in parallel |
| `make test-headed` | Run tests with visible browser |
| `make report` | **Generate and open Allure report** ⭐ |
| `make report-serve` | Serve Allure report (auto-reloads) |
| `make clean` | Clean all test artifacts |

**Note:** Make commands work regardless of venv activation. Python commands inside the Makefile will use your system's Python, so ensure your venv is active first OR the Makefile is configured to use the venv Python.

**Examples:**

```bash
# One-time setup
$ source venv/bin/activate
(.venv) $ make setup

# Run tests and view report
(.venv) $ make test
(.venv) $ make report

# Quick smoke test
(.venv) $ make test-smoke

# Clean everything and start fresh
(.venv) $ make clean
```

**Passing custom arguments to pytest:**

```bash
# Run specific test file
(.venv) $ make test ARGS='apps/e2e/sauce_demo/tests/e2e/test_login.py'

# Run tests matching a keyword
(.venv) $ make test ARGS='-k "test_login"'

# Run with visible browser
(.venv) $ make test ARGS='--headed'

# Run specific test with verbose output
(.venv) $ make test ARGS='apps/api/reqres/tests/test_users.py::test_get_users -v'

# Stop on first failure
(.venv) $ make test ARGS='-x'

# Combine multiple options
(.venv) $ make test ARGS='apps/e2e/sauce_demo/ -k "login" --headed -x'
```

---

### Direct Pytest Commands

If you prefer to run pytest directly without make:

### Run All Tests
```bash
# All tests (E2E + API)
(.venv) $ pytest

# With verbose output
(.venv) $ pytest -v

# With Allure reporting (IMPORTANT: run tests FIRST to generate results)
(.venv) $ pytest --alluredir=test-results/allure-results
```

### Run by Category

```bash
# E2E tests only (45 tests)
(.venv) $ pytest apps/e2e/

# API tests only (41 tests)
(.venv) $ pytest apps/api/

# Specific application
(.venv) $ pytest apps/e2e/sauce_demo/      # 19 Sauce Demo tests
(.venv) $ pytest apps/api/restful_booker/  # 13 Restful Booker tests
```

### Run by Test Type

```bash
# All E2E tests
(.venv) $ pytest -m e2e

# All API tests
(.venv) $ pytest -m api

# Smoke tests only
(.venv) $ pytest -m smoke

# Regression tests
(.venv) $ pytest -m regression
```

### Advanced Options

```bash
# Headful mode (visible browser)
(.venv) $ pytest --headed apps/e2e/

# Record video
(.venv) $ pytest --video on apps/e2e/sauce_demo/

# Enable tracing (for debugging)
(.venv) $ pytest --tracing on

# Parallel execution (4 workers)
(.venv) $ pytest -n 4

# Stop on first failure
(.venv) $ pytest -x

# Run last failed tests
(.venv) $ pytest --lf
```

## 📊 Reports

### Allure Reports

**🎯 Recommended: Use `make report`**

```bash
(.venv) $ make report
```

This single command handles everything - runs tests, generates the report, and opens it in your browser.

---

**Manual Process (for understanding):**

Allure is a TWO-step process:

#### Step 1: Run Tests to Generate Results
```bash
# Run tests with --alluredir flag to collect test results
(.venv) $ pytest --alluredir=allure-results

# This creates the allure-results directory in the project root with test data
```

#### Step 2: Generate and View Report
```bash
# Now you can generate the HTML report from the results
$ allure generate allure-results -o test-results/allure-report --clean
# Note: allure command does NOT need venv - it's a standalone tool

# Open the report in your browser
$ allure open test-results/allure-report
```

#### Complete Example
```bash
# 1. Run tests with Allure results collection
(.venv) $ pytest --alluredir=allure-results

# 2. Generate report (only after tests have run)
$ allure generate allure-results -o test-results/allure-report --clean

# 3. View report
$ allure open test-results/allure-report
```

#### Troubleshooting

**Error: `allure-results does not exist`**
- This means you haven't run tests with `--alluredir` flag yet
- Run `pytest --alluredir=allure-results` FIRST, then generate report

**Error: `AttributeError: 'str' object has no attribute 'iter_parents'`**
- This is caused by pytest 9.0+ incompatibility with allure-pytest
- Fix: Downgrade to pytest 8.x: `pip install 'pytest<9.0.0'`
- The framework's pyproject.toml now pins pytest to `< 9.0.0` to prevent this issue
- Verify versions: `pip list | grep -E "(pytest|allure)"` should show `pytest>=8.0.0,<9.0.0` and `allure-pytest>=2.15.0`

**Install Allure CLI (if not installed):**
```bash
# Using npm (recommended)
npm install -g allure-commandline

# Or using Homebrew (macOS)
brew install allure

# Verify installation
allure --version
```

## 🧪 Test Applications

### E2E Applications

| Application | URL | Tests | Description |
|------------|-----|-------|-------------|
| **Sauce Demo** | [saucedemo.com](https://www.saucedemo.com) | 19 | E-commerce flow, login, cart, checkout |
| **The Internet** | [the-internet.herokuapp.com](https://the-internet.herokuapp.com) | 25 | Component testing (alerts, frames, tables, etc.) |
| **Medusa Store** | [next.medusajs.com](https://next.medusajs.com) | 1 | Modern Next.js guest checkout flow |

### API Applications

| Application | URL | Tests | Auth | Description |
|------------|-----|-------|------|-------------|
| **Restful Booker** | [restful-booker.herokuapp.com](https://restful-booker.herokuapp.com) | 13 | Token | CRUD + Auth flow |
| **Petstore** | [petstore.swagger.io](https://petstore.swagger.io) | 9 | None | OpenAPI/Swagger demo |
| **OMDb** | [omdbapi.com](http://www.omdbapi.com) | 5 | API Key | Movie database search |
| **ReqRes** | [reqres.in](https://reqres.in) | 14 | API Key | User/resource CRUD |

## 🏷 Test Markers

Use markers to categorize and filter tests:

```python
@pytest.mark.app("sauce_demo")    # App assignment
@pytest.mark.e2e                  # E2E UI test
@pytest.mark.api                  # API test
@pytest.mark.smoke                # Critical path
@pytest.mark.regression           # Full regression suite
```

**Run examples:**
```bash
(.venv) $ pytest -m smoke                   # Smoke tests only
(.venv) $ pytest -m "e2e and smoke"         # E2E smoke tests
(.venv) $ pytest -m "not slow"              # Exclude slow tests
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:
```bash
(.venv) $ echo "OMDB_API_KEY=your_omdb_api_key_here" > .env
(.venv) $ echo "ENV=dev" >> .env  # Optional: dev, staging, or production
```

Or create manually:
```bash
# .env file contents
OMDB_API_KEY=your_omdb_api_key_here
ENV=dev  # Optional: dev, staging, or production
```

### App Configuration

Each app has a YAML config in `config/apps/`:

```yaml
# config/apps/sauce_demo.yml
name: sauce_demo
display_name: "Sauce Demo"
type: e2e

base_urls:
  dev: "https://www.saucedemo.com"
  staging: "https://www.saucedemo.com"
  production: "https://www.saucedemo.com"

test_users:
  standard:
    username: "standard_user"
    password: "secret_sauce"
  
settings:
  default_timeout: 30000
  screenshot_on_failure: true
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[Testing Guide](docs/TESTING.md)** - Comprehensive test execution examples
- **[Page Objects](docs/PAGE_OBJECTS.md)** - Pattern guide and best practices
- **[Decorator Guide](docs/DECORATOR_GUIDE.md)** - Pytest vs Allure decorators
- **[Test Cases](apps/)** - Each app has `TEST_CASES.md` with scenarios

## 🤝 Contributing

### Adding New Tests

1. **E2E Test:**
```bash
# Create page object
apps/e2e/your_app/pages/your_page.py

# Create test
apps/e2e/your_app/tests/e2e/test_your_feature.py

# Add configuration
config/apps/your_app_config.yml

# Run your new test
(.venv) $ pytest apps/e2e/your_app/tests/e2e/test_your_feature.py -v
```

2. **API Test:**
```bash
# Create client
apps/api/your_api/clients/your_client.py

# Create test
apps/api/your_api/tests/test_your_endpoint.py

# Run your new test
(.venv) $ pytest apps/api/your_api/tests/test_your_endpoint.py -v
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to public methods
- Use Allure steps for reporting

## 📄 License

MIT License

---

**Made with ❤️ using Playwright + Pytest**
