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

### Setup Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd playwright-pytest

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Install Playwright browsers
playwright install chromium

# 5. Configure API keys (optional, for OMDb tests)
echo "OMDB_API_KEY=your_key_here" > .env
```

**Note:** ReqRes API key is pre-configured. OMDb requires your own API key from [omdbapi.com](http://www.omdbapi.com/apikey.aspx).

## ⚡ Quick Start

### Run All Tests
```bash
# All tests (E2E + API)
pytest

# With verbose output
pytest -v

# With Allure reporting
pytest --alluredir=test-results/allure-results
```

### Run by Category

```bash
# E2E tests only (45 tests)
pytest apps/e2e/

# API tests only (41 tests)
pytest apps/api/

# Specific application
pytest apps/e2e/sauce_demo/      # 19 Sauce Demo tests
pytest apps/api/restful_booker/  # 13 Restful Booker tests
```

### Run by Test Type

```bash
# All E2E tests
pytest -m e2e

# All API tests
pytest -m api

# Smoke tests only
pytest -m smoke

# Regression tests
pytest -m regression
```

### Advanced Options

```bash
# Headful mode (visible browser)
pytest --headed apps/e2e/

# Record video
pytest --video on apps/e2e/sauce_demo/

# Enable tracing (for debugging)
pytest --tracing on

# Parallel execution (4 workers)
pytest -n 4

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

## 📊 Reports

### Allure Reports

```bash
# Generate and open report
allure generate test-results/allure-results -o test-results/allure-report --clean
allure open test-results/allure-report
```

**Note:** Allure commandline tool required: `npm install -g allure-commandline`

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
pytest -m smoke                   # Smoke tests only
pytest -m "e2e and smoke"         # E2E smoke tests
pytest -m "not slow"              # Exclude slow tests
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:
```bash
# API Keys
OMDB_API_KEY=your_omdb_api_key_here

# Environment selection (optional)
ENV=dev  # dev, staging, or production
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
```

2. **API Test:**
```bash
# Create client
apps/api/your_api/clients/your_client.py

# Create test
apps/api/your_api/tests/test_your_endpoint.py
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
