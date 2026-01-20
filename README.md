# Playwright-Pytest Automation Framework

A comprehensive Python-based automation testing framework using Playwright and pytest with multi-app architecture, Page Object Model, and Allure reporting.

## 🚀 Features

- **Multi-App Architecture** - Test multiple web applications and APIs
- **Page Object Model** - Clean separation of test logic and page interactions
- **Allure Reporting** - Rich HTML reports with screenshots, traces, and test history
- **CI/CD Ready** - GitHub Actions workflow with VPS deployment
- **Environment Support** - Dev, staging, and production configurations

## 📁 Project Structure

```
playwright-pytest/
├── apps/                              # All test applications
│   ├── e2e/                           # E2E/UI Tests
│   │   ├── sauce_demo/                # 🥇 E-commerce flow
│   │   ├── the_internet/              # 🥈 Component testing
│   │   └── medusa_store/              # 🥉 Modern Next.js
│   └── api/                           # API Tests
│       ├── restful_booker/            # 🥇 CRUD + Auth
│       ├── reqres/                    # 🥈 Quick mocking
│       ├── petstore/                  # 🥉 OpenAPI/Swagger
│       └── omdb/                      # 📽️ Search & data
├── config/
│   ├── apps/                          # Per-app configuration
│   ├── environments.yml               # Environment settings
│   └── test_data.yml                  # Shared test data
├── infrastructure/
│   ├── fixtures/                      # Shared fixtures
│   ├── hooks/                         # Allure integration
│   └── utils/                         # Utilities
├── pages/                             # Shared/base page objects
├── docs/
│   └── DECORATOR_GUIDE.md             # Pytest vs Allure decorators
├── scripts/
│   ├── setup-vps.sh                   # VPS setup script
│   └── generate-report.sh             # Report generation
├── .github/workflows/
│   └── e2e-tests.yml                  # CI/CD workflow
├── conftest.py                        # Root configuration
├── pytest.ini                         # Pytest settings
└── pyproject.toml                     # Python project config
```

## 🛠 Installation

```bash
# Clone the repository
git clone <repository-url>
cd playwright-pytest

# Create virtual environment with Python 3.11+
pyenv local 3.11.9
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Install Playwright browsers
playwright install chromium
```

## ⚡ Quick Start

### Run All Tests
```bash
pytest
```

### Run E2E Tests
```bash
pytest apps/e2e/                      # All E2E tests
pytest apps/e2e/sauce_demo/           # Sauce Demo only
pytest apps/e2e/the_internet/         # The Internet only
```

### Run API Tests
```bash
pytest apps/api/                      # All API tests
pytest apps/api/restful_booker/       # Restful Booker only
pytest apps/api/reqres/               # ReqRes only
```

### Run by Marker
```bash
pytest -m smoke                       # Smoke tests only
pytest -m regression                  # Regression tests
pytest -m "smoke and not slow"        # Smoke except slow
```

### Run with Options
```bash
pytest --headed                       # Visible browser
pytest --video on                     # Record video
pytest --tracing on                   # Enable tracing
```

## 📊 Reports

### Generate Allure Report
```bash
make report
# Or manually:
allure generate test-results/allure-results -o test-results/allure-report
allure open test-results/allure-report
```

## 🧪 Test Applications

### E2E Apps

| App | URL | Description |
|-----|-----|-------------|
| **Sauce Demo** | saucedemo.com | E-commerce flow, stable |
| **The Internet** | the-internet.herokuapp.com | Component isolation |
| **Medusa Store** | next.medusajs.com | Modern Next.js |

### API Apps

| App | URL | Description |
|-----|-----|-------------|
| **Restful Booker** | restful-booker.herokuapp.com | CRUD + Token Auth |
| **ReqRes** | reqres.in | Quick mocking |
| **Petstore** | petstore.swagger.io | OpenAPI/Swagger |
| **OMDb** | omdbapi.com | Search & data (key required) |

## 🏷 Decorators

See [docs/DECORATOR_GUIDE.md](docs/DECORATOR_GUIDE.md) for detailed usage.

### Quick Reference

```python
import allure
import pytest

@allure.epic("Sauce Demo")              # Report grouping
@allure.feature("Authentication")       # Report grouping
@pytest.mark.app("sauce_demo")          # App assignment
@pytest.mark.smoke                      # Test selection
class TestLogin:
    
    @allure.title("Login with valid credentials")
    def test_login(self, current_app):
        with allure.step("Navigate to login"):
            current_app.navigate("/")
```

## 📝 Makefile Commands

```bash
make test                 # Run all tests
make test-smoke           # Run smoke tests
make test-admin           # Run admin portal tests
make report               # Generate and open report
make clean                # Clean artifacts
```

## ⚙️ Configuration

### Environment Variables

```bash
# .env file
OMDB_API_KEY=your_key_here
```

### App Configs

Each app has a YAML config in `config/apps/`:

```yaml
# config/apps/sauce_demo.yml
name: sauce_demo
base_urls:
  dev: "https://www.saucedemo.com"
test_users:
  standard:
    username: "standard_user"
    password: "secret_sauce"
```

## 📚 Documentation

- [Decorator Guide](docs/DECORATOR_GUIDE.md) - Pytest vs Allure decorators
- [Test Cases](apps/) - Each app has a `TEST_CASES.md`

## 📄 License

MIT License
