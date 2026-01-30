# Setup Guide

Complete installation and configuration guide for the Playwright-Pytest Automation Framework.

## Prerequisites

### Required Software
- **Python 3.11+** - [Download](https://www.python.org/downloads/) or use [pyenv](https://github.com/pyenv/pyenv)
- **Git** - [Download](https://git-scm.com/downloads)
- **Node.js 16+** - [Download](https://nodejs.org/) (for Allure reports)

### Recommended
- **pyenv** - Python version management
- **VS Code** or **PyCharm** - IDE with Python support
- **iTerm2** or **Windows Terminal** - Better terminal experience

---

## Installation Steps

### 1. Clone Repository

```bash
git clone <repository-url>
cd playwright-pytest
```

### 2. Python Version Setup

**Using pyenv (Recommended):**
```bash
# Install Python 3.11.9
pyenv install 3.11.9

# Set local version
pyenv local 3.11.9

# Verify
python --version  # Should show 3.11.9
```

**Without pyenv:**
Ensure Python 3.11 or later is installed and active.

### 3. Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation (should show project path)
which python
```

### 4. Install Dependencies

```bash
# Install framework with dev dependencies
pip install -e ".[dev]"

# This installs:
# - playwright
# - pytest and plugins
# - allure-pytest
# - requests
# - python-dotenv
# - pyyaml
```

### 5. Install Playwright Browsers

```bash
# Install Chromium (default browser)
playwright install chromium

# Optional: Install all browsers
playwright install
```

### 6. Verify Installation

```bash
# Verify pytest
pytest --version  # Should show: pytest 9.0.2

# Verify playwright
playwright --version  # Should show: 1.57.0

# Test API smoke suite (quick verification)
pytest apps/api/ -m smoke --collect-only
# Should collect 7 smoke tests

# Run a simple API test
pytest apps/api/omdb/tests/test_search.py::TestOmdbSearch::test_search_movie -v
# ✅ Should PASS

# Optional: Run a full E2E test (slower)
pytest apps/e2e/sauce_demo/tests/e2e/test_authentication.py::TestAuthentication::test_successful_login -v
```

**Quick Health Check:**
```bash
# Collect all smoke tests
pytest -m smoke --collect-only
# Expected: 15 tests collected (8 E2E + 7 API)
```

---

## Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Optional: OMDb API key (for OMDb tests)
OMDB_API_KEY=your_key_here

# Optional: Environment selection
ENV=dev  # Options: dev, staging, production
```

**Get OMDb API Key:** http://www.omdbapi.com/apikey.aspx (free tier available)

### Verify Configuration

```bash
# List all configured apps
pytest --co  # Shows test collection

# Should see apps:
# - sauce_demo
# - the_internet
# - medusa_store
# - restful_booker
# - petstore
# - omdb
# - reqres
```

---

## IDE Setup

### VS Code

**Recommended Extensions:**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "littlefoxteam.vscode-python-test-adapter",
    "tamasfe.even-better-toml"
  ]
}
```

**Settings (.vscode/settings.json):**
```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "."
  ],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true
}
```

### PyCharm

1. **Mark directories as Sources Root:**
   - Right-click `apps/` → Mark Directory as → Sources Root
   - Right-click `infrastructure/` → Mark Directory as → Sources Root

2. **Configure pytest:**
   - Settings → Tools → Python Integrated Tools
   - Set Default test runner: pytest

3. **Set Python interpreter:**
   - Settings → Project → Python Interpreter
   - Select `venv/bin/python`

---

## Optional Tools

### Allure Reports

```bash
# Install Allure commandline (macOS)
brew install allure

# Install Allure commandline (Linux)
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Install Allure commandline (Windows)
scoop install allure

# Or via npm (all platforms)
npm install -g allure-commandline
```

**Verify:**
```bash
allure --version
# Should show: 2.x.x
```

### Parallel Execution

Already included if you installed with `[dev]`:
```bash
# Run tests in parallel (4 workers)
pytest -n 4

# Auto-detect CPU cores
pytest -n auto
```

---

## Troubleshooting

### Playwright Installation Issues

**Error: `playwright install` fails**
```bash
# Install system dependencies (Linux)
sudo playwright install-deps chromium

# Or use official script
python -m playwright install-deps
```

### Import Errors

**Error: `ModuleNotFoundError`**
```bash
# Reinstall in editable mode
pip install -e ".[dev]"

# Verify installation
pip list | grep playwright
```

### Browser Launch Fails

**Error: Browser not found**
```bash
# Reinstall browsers
playwright install chromium --force
```

---

## Next Steps

- [Testing Guide](TESTING.md) - Learn how to run and organize tests
- [Page Objects Guide](PAGE_OBJECTS.md) - Understand the Page Object Model
- [Contributing](../README.md#contributing) - Start adding your own tests

---

**Setup complete!** 🎉 You're ready to run tests.
