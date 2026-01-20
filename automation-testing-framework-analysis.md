# Automation Testing Framework Analysis
## Architectural Analysis of Playwright, pytest, and playwright-pytest

**Analysis Date:** 2025-01-20
**Target:** Building a Python-Based Automation Testing Framework

---

## Executive Summary

This analysis examines three foundational repositories for building a modern Python automation testing framework:

1. **[pytest-dev/pytest](https://github.com/pytest-dev/pytest)** - The core testing framework with fixture system, plugin architecture, and test discovery
2. **[microsoft/playwright](https://github.com/microsoft/playwright)** - Browser automation library with cross-browser support
3. **[microsoft/playwright-pytest](https://github.com/microsoft/playwright-pytest)** - pytest plugin integrating Playwright with pytest

---

## 1. pytest Core Architecture

### 1.1 Fixture System (`src/_pytest/fixtures.py`)

The fixture system is pytest's most powerful feature, providing:

**Fixture Scope Hierarchy:**
```
session > package > module > class > function
```

**Key Classes:**
- `FixtureDef`: Container for fixture definition with cached results
- `FixtureRequest`: Abstract base for accessing test context
- `TopRequest`: Request type for test functions
- `SubRequest`: Request type for fixtures depending on other fixtures
- `FixtureManager`: Manages fixture definitions and resolution

**Critical Fixture Lifecycle Methods:**

| Method | Purpose |
|--------|---------|
| `execute(request)` | Return fixture value, executing if not cached |
| `cache_key(request)` | Generate cache key (uses `request.param` for parametrized fixtures) |
| `addfinalizer(fn)` | Register teardown callback |
| `finish(request)` | Execute all finalizers and clear cache |

**Fixture Resolution Algorithm:**
```python
# From getfixtureclosure() - builds transitive dependency closure
def process_argname(argname: str) -> None:
    # 1. Check if already processed (optimization)
    # 2. Get fixturedefs for argname
    # 3. Handle override chains (negative indexing)
    # 4. Recursively process dependencies
    # 5. Sort by scope (highest scopes first)
```

**Key Design Patterns:**
- **Dependency Injection**: Fixtures declare dependencies via function parameters
- **Lazy Evaluation**: Fixtures execute only when requested
- **Scope-based Caching**: Values cached based on fixture scope
- **Override Chain**: Fixtures can override same-name fixtures in narrower scopes

### 1.2 Plugin System (`src/_pytest/hookspec.py`)

**Hook Specification Categories:**

| Category | Key Hooks | Purpose |
|----------|-----------|---------|
| **Initialization** | `pytest_addoption`, `pytest_configure`, `pytest_sessionstart` | Setup and configuration |
| **Collection** | `pytest_collection_modifyitems`, `pytest_collect_file`, `pytest_pycollect_makeitem` | Test discovery and filtering |
| **Runtest** | `pytest_runtest_setup`, `pytest_runtest_call`, `pytest_runtest_teardown`, `pytest_runtest_makereport` | Test execution lifecycle |
| **Fixtures** | `pytest_fixture_setup`, `pytest_fixture_post_finalizer` | Fixture lifecycle management |
| **Reporting** | `pytest_terminal_summary`, `pytest_report_teststatus` | Output customization |

**Hook Wrapper Pattern:**
```python
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Modify report or attach artifacts
```

**Conftest Discovery:**
- Searches upward from test directories
- Loads conftest modules in parent directory order
- `FSHookProxy` optimizes calls by excluding irrelevant conftests

### 1.3 Parametrization System

**CallSpec2 Structure:**
```python
params: dict[str, object]      # arg name -> arg value
indices: dict[str, int]        # arg name -> param index
_arg2scope: Mapping[str, Scope] # Parameter scope override
_idlist: Sequence[str]          # ID parts for test naming
marks: list[Mark]              # Marks for the test item
```

**Cartesian Product Mechanism:**
Each `@pytest.mark.parametrize` call multiplies existing parametrizations, creating a complete test matrix.

**Indirect Parametrization:**
```python
@pytest.mark.parametrize("browser", ["chromium", "firefox"], indirect=True)
def test_with_browser(browser):  # browser is now a fixture
    pass
```

### 1.4 Markers and Test Selection

**Built-in Markers:**
- `skip` / `skipif` - Conditional test skipping
- `xfail` - Expected failures
- `parametrize` - Parameter injection
- `usefixtures` - Auto-apply fixtures
- `filterwarnings` - Warning filtering

**Custom Marker Registration:**
```python
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
```

---

## 2. Playwright-Pytest Plugin Architecture

### 2.1 Core Fixture Hierarchy (`pytest_playwright/pytest_playwright/pytest_playwright.py`)

**Fixture Dependency Chain:**
```
playwright (session)
  └─> browser_type (session)
      └─> launch_browser (session)
          └─> browser (session)
              └─> new_context (function)
                  └─> context (function)
                      └─> page (function)
```

**Session-scoped Fixtures:**

| Fixture | Type | Purpose |
|---------|------|---------|
| `playwright` | `Playwright` | Main API entry point |
| `browser_type` | `BrowserType` | Chromium/Firefox/WebKit selector |
| `browser` | `Browser` | Browser instance (headless by default) |
| `is_chromium/is_firefox/is_webkit` | `bool` | Browser detection helpers |
| `browser_channel` | `str | None` | Chrome/Edge channel support |
| `device` | `str | None` | Device emulation descriptor |

**Function-scoped Fixtures:**

| Fixture | Type | Purpose |
|---------|------|---------|
| `context` | `BrowserContext` | Isolated storage/cookies |
| `page` | `Page` | Single browser tab |
| `output_path` | `str` | Test-specific artifact directory |

### 2.2 Browser Context Arguments (`browser_context_args`)

**Default Context Configuration:**
```python
@pytest.fixture(scope="session")
def browser_context_args(
    pytestconfig, playwright, device, base_url, _pw_artifacts_folder
) -> Dict:
    context_args = {}
    if device:
        context_args.update(playwright.devices[device])  # Device emulation
    if base_url:
        context_args["base_url"] = base_url
    if video_option in ["on", "retain-on-failure"]:
        context_args["record_video_dir"] = _pw_artifacts_folder.name
    return context_args
```

**Override Pattern via Marker:**
```python
@pytest.mark.browser_context_args(user_agent="custom", locale="en-US")
def test_with_custom_context(page):
    pass
```

### 2.3 Artifacts Recorder

**The `ArtifactsRecorder` class manages:**

1. **Screenshots** - Captured on failure or always
2. **Traces** - Comprehensive execution recordings
3. **Videos** - Page execution recordings

**Lifecycle:**
```python
def on_did_create_browser_context(context):
    # Start tracing if enabled
    context.tracing.start(title=slugify(request.node.nodeid), ...)

def on_will_close_browser_context(context):
    # Stop tracing, capture screenshots
    context.tracing.stop(path=trace_path)

def did_finish_test(failed):
    # Retain or delete artifacts based on config
    if failed and video_option == "retain-on-failure":
        video.save_as(path=output_path)
```

### 2.4 CLI Options

**Command-line Interface:**
```bash
--browser {chromium,firefox,webkit}    # Browser selection
--headed                              # Show browser window
--browser-channel {chrome,msedge}     # Use branded browsers
--slowmo MILLISECONDS                  # Slow execution
--device DEVICE_NAME                   # Device emulation
--output DIR                          # Artifact directory
--tracing {on,off,retain-on-failure}  # Trace recording
--video {on,off,retain-on-failure}    # Video recording
--screenshot {on,off,only-on-failure} # Screenshot capture
--full-page-screenshot                 # Full page captures
```

---

## 3. Framework Design Recommendations

### 3.1 Core Architecture Pattern

**Recommended Layered Architecture:**

```
┌─────────────────────────────────────────────────────┐
│              Test Layer (tests/)                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ E2E Tests  │  │ API Tests  │  │ Unit Tests │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│            Page Object Model (pages/)               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ BasePage   │  │ LoginPage  │  │ ...Page    │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         Test Infrastructure (infrastructure/)        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ fixtures/  │  │  utils/    │  │  config/   │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 3.2 Essential Fixtures to Implement

**Session-scoped Infrastructure:**

```python
# infrastructure/fixtures/session.py
import pytest
from playwright.sync_api import Browser, BrowserContext

@pytest.fixture(scope="session")
def test_config(pytestconfig):
    """Load test configuration from environment or config files."""
    return {
        "base_url": pytestconfig.getoption("--base-url"),
        "timeout": int(pytestconfig.getoption("--timeout", default=30000)),
    }

@pytest.fixture(scope="session")
def auth_context(browser_type, browser_type_launch_args, test_config):
    """Shared authenticated context for session-scoped login."""
    context = browser_type.launch(**browser_type_launch_args)
    # Perform login once, reuse across tests
    yield context
    context.close()

@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON/YAML files."""
    return load_test_data()
```

**Function-scoped Page Objects:**

```python
# infrastructure/fixtures/pages.py
import pytest
from pages.base_page import BasePage

@pytest.fixture
def login_page(page, test_config):
    """Provide LoginPage with automatic navigation."""
    from pages.login_page import LoginPage
    page.goto(test_config["base_url"] + "/login")
    return LoginPage(page)
```

### 3.3 Page Object Model Pattern

**Base Page Class:**

```python
# pages/base_page.py
from playwright.sync_api import Page, Locator, expect
from typing import Optional

class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = 5000

    def navigate(self, url: str):
        """Navigate to URL."""
        self.page.goto(url)

    def wait_for_load_state(self, state: str = "load"):
        """Wait for specified load state."""
        self.page.wait_for_load_state(state)

    def click_element(self, locator: str):
        """Click element with wait."""
        self.page.locator(locator).click()

    def fill_text(self, locator: str, text: str):
        """Fill input field."""
        self.page.locator(locator).fill(text)

    def get_text(self, locator: str) -> str:
        """Get element text content."""
        return self.page.locator(locator).text_content()

    def is_visible(self, locator: str) -> bool:
        """Check element visibility."""
        return self.page.locator(locator).is_visible()

    def wait_for_element(self, locator: str):
        """Wait for element to be attached."""
        self.page.wait_for_selector(locator)
```

**Example Page Implementation:**

```python
# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for Login page."""

    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"

    def __init__(self, page):
        super().__init__(page)
        self.url = "/login"

    def login(self, username: str, password: str):
        """Perform login action."""
        self.fill_text(self.USERNAME_INPUT, username)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        self.wait_for_load_state()

    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        return self.page.locator(self.LOGIN_BUTTON).is_enabled()
```

### 3.4 Custom Hooks for Framework Enhancement

**Test Result Reporting Hook:**

```python
# infrastructure/hooks/reporting.py
import pytest
from typing import Dict, Any

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test result for custom reporting."""
    outcome = yield
    report = outcome.get_result()

    # Store report on item for access in fixtures
    setattr(item, f"rep_{report.when}", report)

    # Custom processing on test completion
    if report.when == "call":
        test_results[item.nodeid] = {
            "outcome": report.outcome,
            "duration": report.duration,
            "failed": report.failed,
        }

@pytest.fixture
def test_report(request):
    """Access test report in fixtures."""
    return getattr(request.node, "rep_call", None)
```

**Screenshot on Failure Hook:**

```python
# infrastructure/hooks/screenshots.py
import pytest
from pathlib import Path

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get page fixture if available
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = Path("test-results/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = screenshot_dir / f"{item.name}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

            # Add to report
            report.extra = getattr(report, "extra", [])
            report.extra.append(pytest_html.extras.image(str(screenshot_path)))
```

### 3.5 Configuration Management

**Project Structure:**
```
framework/
├── config/
│   ├── __init__.py
│   ├── environments.yml      # Environment-specific configs
│   └── test_data.yml         # Test data sets
├── conftest.py               # Root conftest with global fixtures
├── infrastructure/
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── session.py        # Session-scoped fixtures
│   │   └── pages.py          # Page object fixtures
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── reporting.py      # Custom hooks
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py
│       └── logger.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── e2e/
│   ├── api/
│   └── unit/
└── pytest.ini
```

### 3.6 Advanced Patterns from Analysis

**1. Fixture Override Chain (from pytest fixtures.py):**
```python
# Base fixture in conftest.py
@pytest.fixture(scope="session")
def api_client():
    return BaseAPIClient()

# Override in tests/integration/conftest.py
@pytest.fixture(scope="session")
def api_client(api_client):
    # Extend base client with integration-specific setup
    api_client.set_auth_token(get_integration_token())
    return api_client
```

**2. Parametrized Browser Testing (from playwright-pytest):**
```python
@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_cross_browser_compatibility(page, browser_name):
    # Test runs on all three browsers
    assert page.evaluate("window.navigator.userAgent") is not None
```

**3. Dynamic Fixture Creation:**
```python
@pytest.fixture
def dynamic_page(browser, base_url):
    """Create page with dynamic URL."""
    page = browser.new_page()
    page.goto(base_url)
    yield page
    page.close()
```

### 3.7 Best Practices Summary

| Practice | Rationale |
|----------|-----------|
| **Use Page Object Model** | Separates test logic from page structure |
| **Session-scoped shared resources** | Expensive resources (DB, browser) reused |
| **Function-scoped page instances** | Test isolation, no state leakage |
| **Explicit fixture dependencies** | Clear initialization order, better debugging |
| **Yield-based fixtures** | Proper teardown, even on failures |
| **Marker-based test organization** | Easy selection of test subsets |
| **Hookimpl wrapper pattern** | Non-invasive extension of pytest behavior |
| **Artifact recording on failure** | Debugging without cluttering passing tests |

### 3.8 Multi-Web-Application Architecture Pattern

**Use Case:** When testing multiple web applications (e.g., admin portal, customer portal, API dashboard), the framework needs app-specific isolation while sharing core infrastructure.

#### 3.8.1 Multi-App Project Structure

```
framework/
├── config/
│   ├── apps/
│   │   ├── admin_portal_config.yml      # Admin portal specific config
│   │   ├── customer_portal_config.yml   # Customer portal specific config
│   │   └── api_dashboard_config.yml     # API dashboard specific config
│   └── environments.yml                 # Environment (dev/staging/prod)
│
├── apps/                                  # App-isolated modules
│   ├── admin_portal/
│   │   ├── __init__.py
│   │   ├── conftest.py                   # Admin-specific fixtures
│   │   ├── pages/                        # Admin portal page objects only
│   │   │   ├── __init__.py
│   │   │   ├── base_page.py
│   │   │   ├── login_page.py
│   │   │   └── dashboard_page.py
│   │   ├── fixtures/                     # Admin-specific fixtures
│   │   │   ├── __init__.py
│   │   │   └── auth.py                   # Admin auth flow
│   │   └── tests/                        # Admin tests grouped here
│   │       ├── e2e/
│   │       │   └── test_login.py
│   │       └── api/
│   │
│   ├── customer_portal/
│   │   ├── pages/
│   │   ├── fixtures/
│   │   └── tests/
│   │
│   └── api_dashboard/
│       └── ...
│
├── infrastructure/                        # Shared infrastructure
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── session.py                   # Browser, test config
│   │   └── app_factory.py               # Creates app instances
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── reporting.py
│   └── utils/
│
├── conftest.py                            # Root conftest with app discovery
└── pytest.ini
```

#### 3.8.2 App Factory Pattern

```python
# infrastructure/fixtures/app_factory.py
import pytest
from typing import Protocol
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    """Configuration for a single web application."""
    name: str
    base_url: str
    auth_required: bool = True
    default_timeout: int = 30000
    screenshot_on_failure: bool = True
    storage_state_path: str | None = None

class AppInterface(Protocol):
    """Interface that all app modules must implement."""

    @property
    def config(self) -> AppConfig:
        """Return app configuration."""
        ...

    def get_page_class(self, page_name: str) -> type:
        """Get page object class by name."""
        ...

@pytest.fixture(scope="session")
def app_configs(pytestconfig) -> dict[str, AppConfig]:
    """
    Load all app configurations.

    Config can be loaded from YAML files or environment variables.
    """
    env = pytestconfig.getoption("--env", default="dev")

    return {
        "admin_portal": AppConfig(
            name="admin_portal",
            base_url="https://admin.example.com",
            auth_required=True,
            storage_state_path=f"config/apps/admin_portal_{env}_auth.json",
        ),
        "customer_portal": AppConfig(
            name="customer_portal",
            base_url="https://portal.example.com",
            auth_required=True,
            default_timeout=60000,  # Slower app
        ),
        "api_dashboard": AppConfig(
            name="api_dashboard",
            base_url="https://dashboard.internal.com",
            auth_required=False,
        ),
    }

@pytest.fixture
def current_app(request, app_configs, page):
    """
    Get the app instance for the current test based on @pytest.mark.app marker.

    Usage:
        @pytest.mark.app("admin_portal")
        def test_admin_login(current_app):
            login_page = current_app.pages.LoginPage(current_app.page)
            login_page.login("admin", "password")
    """
    marker = request.node.get_closest_marker("app")
    if not marker:
        pytest.fail("Test must specify @pytest.mark.app('app_name')")

    app_name = marker.args[0]
    if app_name not in app_configs:
        pytest.fail(f"Unknown app: {app_name}. Available: {list(app_configs.keys())}")

    config = app_configs[app_name]

    # Import the app module dynamically
    try:
        app_module = __import__(f"apps.{app_name}", fromlist=['pages', 'fixtures'])
    except ImportError as e:
        pytest.fail(f"App module not found: apps.{app_name}. Error: {e}")

    return AppInstance(config, app_module, page)

class AppInstance:
    """
    Runtime instance of an app for a single test.

    Provides access to app-specific pages, fixtures, and configuration.
    """

    def __init__(self, config: AppConfig, app_module, page):
        self.config = config
        self._app_module = app_module
        self.page = page

    @property
    def pages(self):
        """Access to app-specific page objects."""
        return self._app_module.pages

    @property
    def fixtures(self):
        """Access to app-specific fixtures."""
        return self._app_module.fixtures

    def navigate(self, path: str = ""):
        """Navigate to a path in this app."""
        url = self.config.base_url + path
        self.page.goto(url)

    def wait_for_load_state(self, state: str = "load"):
        """Wait for specified load state with app-specific timeout."""
        self.page.wait_for_load_state(state, timeout=self.config.default_timeout)
```

#### 3.8.3 Test Usage Examples

```python
# apps/admin_portal/tests/e2e/test_login.py
import pytest
from apps.admin_portal.pages.login_page import LoginPage
from apps.admin_portal.pages.dashboard_page import DashboardPage

@pytest.mark.app("admin_portal")
def test_admin_successful_login(current_app):
    """Test login for admin portal."""
    login_page = LoginPage(current_app.page)
    dashboard_page = DashboardPage(current_app.page)

    current_app.navigate("/login")
    login_page.login("admin@example.com", "secure_password")

    assert dashboard_page.is_loaded()
    assert dashboard_page.get_welcome_message() == "Welcome, Admin!"

@pytest.mark.app("admin_portal")
def test_admin_logout(current_app):
    """Test logout functionality."""
    from apps.admin_portal.pages.dashboard_page import DashboardPage

    current_app.navigate("/dashboard")
    dashboard = DashboardPage(current_app.page)
    dashboard.logout()

    assert current_app.page.url.endswith("/login")

# apps/customer_portal/tests/e2e/test_search.py
@pytest.mark.app("customer_portal")
def test_customer_search_functionality(current_app):
    """Test search for customer portal (different auth flow)."""
    from apps.customer_portal.pages.search_page import SearchPage

    search_page = SearchPage(current_app.page)
    current_app.navigate("/")

    results = search_page.search("playwright automation")
    assert len(results) > 0
    assert all("playwright" in r.title.lower() for r in results)

# apps/api_dashboard/tests/e2e/test_public_access.py
@pytest.mark.app("api_dashboard")
def test_api_dashboard_no_auth_required(current_app):
    """Test that API dashboard is publicly accessible."""
    current_app.navigate("/metrics")

    # No auth needed, direct access
    assert current_app.page.locator("h1").text_content() == "API Metrics"
```

#### 3.8.4 Per-App conftest for Custom Fixtures

```python
# apps/admin_portal/conftest.py
import pytest
from playwright.sync_api import BrowserContext

@pytest.fixture(scope="session")
def admin_auth_context(browser, app_configs):
    """
    Admin portal requires special authentication context.

    This fixture is automatically used for all admin_portal tests
    due to pytest_plugins in __init__.py or explicit import.
    """
    config = app_configs["admin_portal"]

    context = browser.new_context(
        base_url=config.base_url,
        storage_state=config.storage_state_path,
        viewport={"width": 1920, "height": 1080},
    )

    yield context
    context.close()

# apps/customer_portal/conftest.py
import pytest

@pytest.fixture(scope="session")
def customer_api_client(app_configs):
    """
    Customer portal also has API testing capabilities.
    Different apps = different testing approaches.
    """
    import requests

    config = app_configs["customer_portal"]
    session = requests.Session()
    session.headers.update({"X-App-Origin": config.base_url})

    yield session
    session.close()

# apps/api_dashboard/conftest.py
import pytest

@pytest.fixture
def dashboard_test_data():
    """API dashboard has specific test data requirements."""
    return {
        "test_api_key": "test-key-12345",
        "test_endpoints": ["/users", "/metrics", "/health"],
    }
```

#### 3.8.5 Root conftest with App Discovery

```python
# conftest.py
import pytest
from pathlib import Path

def pytest_addoption(parser):
    """Add custom CLI options for multi-app testing."""
    parser.addoption(
        "--app",
        action="append",
        help="Run tests only for specified app(s). Can be specified multiple times."
    )
    parser.addoption(
        "--env",
        default="dev",
        help="Environment to run tests against (dev/staging/prod)"
    )

def pytest_configure(config):
    """Register app marker and auto-discover app conftests."""
    # Register custom marker
    config.addinivalue_line(
        "markers", "app(name): mark test as belonging to a specific app"
    )

    # Auto-discover all app conftests
    apps_dir = Path(__file__).parent / "apps"
    if apps_dir.exists():
        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir() and (app_dir / "conftest.py").exists():
                # Import triggers conftest loading
                try:
                    __import__(f"apps.{app_dir.name}.conftest")
                except ImportError:
                    pass  # Skip apps with import errors

def pytest_collection_modifyitems(items, config):
    """
    Filter tests by app if --app specified.

    This enables running tests for specific apps only:
        pytest --app admin_portal --app customer_portal
    """
    selected_apps = config.getoption("--app")

    if not selected_apps:
        return  # No filtering requested

    selected = []
    deselected = []

    for item in items:
        app_marker = item.get_closest_marker("app")
        if app_marker and app_marker.args[0] in selected_apps:
            selected.append(item)
        else:
            deselected.append(item)

    items[:] = selected

    if deselected:
        config.hook.pytest_deselected(items=deselected)

def pytest_report_header(config):
    """Add app info to test report header."""
    apps = config.getoption("--app")
    env = config.getoption("--env")

    lines = []
    if apps:
        lines.append(f"Testing apps: {', '.join(apps)}")
    lines.append(f"Environment: {env}")
    return lines
```

#### 3.8.6 Running Tests Across Apps

```bash
# Run all tests for a specific app
pytest tests/ -m "admin_portal" --app admin_portal

# Run tests across multiple apps
pytest tests/ --app admin_portal --app customer_portal

# Run all apps (integration testing across all apps)
pytest tests/ --all-apps

# Run with different environments
pytest tests/ --app admin_portal --env staging
pytest tests/ --app admin_portal --env production

# Combine with other pytest options
pytest tests/ --app customer_portal --browser firefox --headed -v

# Run only smoke tests across all apps
pytest tests/ -m smoke --all-apps
```

#### 3.8.7 App Configuration File Example

```yaml
# config/apps/admin_portal_config.yml
name: admin_portal
display_name: "Admin Portal"
base_urls:
  dev: "https://admin-dev.example.com"
  staging: "https://admin-staging.example.com"
  production: "https://admin.example.com"
auth:
  type: "form_based"
  login_page: "/admin/login"
  username_field: "#username"
  password_field: "#password"
  submit_button: "button[type='submit']"
default_timeout: 30000
screenshot_on_failure: true
test_data:
  admin_user: "admin@example.com"
  admin_password: "${ADMIN_PASSWORD}"  # From environment
  test_users:
    - email: "user1@example.com"
      role: "editor"
    - email: "user2@example.com"
      role: "viewer"
```

#### 3.8.8 Multi-App Testing Best Practices

| Practice | Rationale |
|----------|-----------|
| **App isolation via separate modules** | Prevents namespace collisions, clear ownership |
| **App marker on every test** | Explicit app association, enables filtering |
| **Shared infrastructure, app-specific pages** | Reuse browser/fixtures, isolate page logic |
| **Per-app conftest** | App-specific fixtures override when needed |
| **Factory pattern for app instances** | Consistent interface across all apps |
| **Environment-aware configuration** | Same tests, different environments |
| **App-specific test data** | Each app has different data models/flows |

### 3.9 Unified Reporting Stack: Allure + Playwright HTML

**Recommended Reporting Stack:**

```
┌────────────────────────────────────────────────────────────────┐
│                     Test Execution                             │
│                    (pytest + playwright)                        │
└────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────────┐
│              pytest_runtest_makereport Hook                    │
│         (Data Capture & Artifact Collection Layer)              │
│  - Capture test outcomes                                       │
│  - Attach screenshots on failure                                │
│  - Attach Playwright traces                                     │
│  - Enrich Allure metadata                                       │
└────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────────┐   ┌───────────────────────────────┐
│   Allure Report       │   │   Playwright HTML Reporter    │
│   (test-results/)      │   │   (test-results/index.html)   │
│ - Rich HTML           │   │ - Timeline viewer             │
│ - Test history        │   │ - Trace inspection            │
│ - Categories          │   │ - Network requests            │
│ - Attachments         │   │ - Screenshots + videos        │
└───────────────────────┘   └───────────────────────────────┘
```

#### 3.9.1 Installation and Configuration

**Dependencies:**

```bash
# Install Allure pytest plugin
pip install allure-pytest

# Install Allure commandline (macOS)
brew install allure

# Install Allure commandline (Linux)
wget https://github.com/allure-framework/allure2/releases/download/2.x.x/allure-2.x.x.tgz
tar -zxvf allure-2.x.x.tgz

# Install Allure commandline (Windows)
# Download from: https://github.com/allure-framework/allure2/releases
```

**pytest.ini Configuration:**

```ini
# pytest.ini
[pytest]
# Pytest options
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# Allure configuration
--alluredir=test-results/allure-results
--allure-threads=4

# Playwright configuration
--base-url=http://localhost:3000
--browser=chromium
--headed=false
--screenshot=only-on-failure
--video=retain-on-failure
--tracing=retain-on-failure

# Markers
markers =
    app(name): mark test as belonging to a specific app
    smoke: smoke tests
    regression: regression tests
    api: API tests
    ui: UI tests
    slow: slow running tests
    flaky: flaky test that may fail intermittently
```

**Playwright Configuration (for HTML Reporter):**

```python
# conftest.py - Configure Playwright HTML Reporter
def pytest_configure(config):
    """Configure Playwright HTML reporter output."""
    # Ensure test-results directory exists
    from pathlib import Path
    results_dir = Path("test-results")
    results_dir.mkdir(exist_ok=True)
```

#### 3.9.2 Unified Reporting Hook Implementation

```python
# infrastructure/hooks/unified_reporting.py
import pytest
import allure
from pathlib import Path
from typing import Optional
from datetime import datetime
import json

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Unified reporting that feeds both Allure and Playwright HTML.

    This hook:
    1. Captures test metadata for Allure
    2. Attaches screenshots to Allure on failure
    3. Attaches Playwright traces to Allure
    4. Stores report data for custom processing
    """
    outcome = yield
    report = outcome.get_result()

    # Store report for pytest native access
    setattr(item, f"rep_{report.when}", report)

    # Only process call phase (actual test execution)
    if report.when != "call":
        return

    # Extract test metadata
    app_marker = item.get_closest_marker("app")
    app_name = app_marker.args[0] if app_marker else "unknown"

    # Set Allure environment info
    allure.environment(
        app=app_name,
        browser=item.funcargs.get("browser_name", "chromium"),
        test_run=datetime.now().isoformat(),
    )

    # Attach artifacts on failure
    if report.failed:
        _attach_failure_artifacts(item, report, app_name)

    # Always attach metadata
    _attach_test_metadata(item, app_name)

def _attach_failure_artifacts(item, report, app_name: str):
    """Attach screenshots, traces, and videos to Allure on failure."""
    page = item.funcargs.get("page")
    if not page:
        return

    test_name = item.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Screenshot
    screenshot_dir = Path("test-results/screenshots") / app_name
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        allure.attach(
            f"Failed to capture screenshot: {e}",
            name="Screenshot Error",
            attachment_type=allure.attachment_type.TEXT
        )

    # 2. Playwright Trace (if available)
    trace_dir = Path("test-results/traces") / app_name
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Find trace file from output_path fixture
    if "output_path" in item.funcargs:
        output_path = Path(item.funcargs["output_path"])
        trace_files = list(output_path.glob("trace*.zip"))

        if trace_files:
            trace_path = trace_files[0]
            # Copy to organized location
            organized_trace = trace_dir / f"{test_name}_{timestamp}_trace.zip"
            trace_path.rename(organized_trace)

            # Attach to Allure
            allure.attach.file(
                str(organized_trace),
                name="Playwright Trace (open in Playwright)",
                attachment_type=allure.attachment_type.ZIP
            )

def _attach_test_metadata(item, app_name: str):
    """Attach test metadata to Allure."""
    metadata = {
        "test_id": item.nodeid,
        "app": app_name,
        "markers": [mark.name for mark in item.iter_markers()],
        "timeout": getattr(item, "_timeout", "not set"),
    }

    allure.attach(
        json.dumps(metadata, indent=2),
        name="Test Metadata",
        attachment_type=allure.attachment_type.JSON
    )

@pytest.fixture
def attach_screenshot(page):
    """Fixture to manually attach screenshot during test."""
    def _attach(name: str = "Screenshot"):
        screenshot_path = Path("test-results/screenshots") / f"{name}.png"
        page.screenshot(path=str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    return _attach
```

#### 3.9.3 Enhanced Page Object with Allure Integration

```python
# pages/base_page.py
import allure
from playwright.sync_api import Page, Locator

class BasePage:
    """Base page class with Allure reporting integration."""

    def __init__(self, page: Page, app_name: str = "unknown"):
        self.page = page
        self.app_name = app_name

    def navigate(self, url: str):
        """Navigate to URL with Allure step tracking."""
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)

    def click_element(self, locator: str, name: str = None):
        """Click element with Allure step and screenshot."""
        element_name = name or locator
        with allure.step(f"Click {element_name}"):
            try:
                self.page.locator(locator).click()
                # Attach screenshot after action
                self._attach_step_screenshot(f"After clicking {element_name}")
            except Exception as e:
                self._attach_step_screenshot(f"Failed clicking {element_name}")
                raise

    def fill_text(self, locator: str, text: str, name: str = None):
        """Fill input with Allure step tracking."""
        element_name = name or locator
        with allure.step(f"Fill {element_name} with '{text}'"):
            self.page.locator(locator).fill(text)

    def wait_for_element(self, locator: str, timeout: int = 5000):
        """Wait for element with Allure step."""
        with allure.step(f"Wait for {locator} (timeout: {timeout}ms)"):
            self.page.wait_for_selector(locator, timeout=timeout)

    def _attach_step_screenshot(self, name: str):
        """Attach screenshot to current Allure step."""
        try:
            screenshot = self.page.screenshot()
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass  # Screenshot capture failed, continue

    def verify_element_visible(self, locator: str, name: str = None):
        """Verify element is visible with Allure assertion."""
        element_name = name or locator
        with allure.step(f"Verify {element_name} is visible"):
            is_visible = self.page.locator(locator).is_visible()
            assert is_visible, f"{element_name} is not visible"
```

#### 3.9.4 Test Examples with Allure Annotations

```python
# apps/admin_portal/tests/e2e/test_login.py
import pytest
import allure
from apps.admin_portal.pages.login_page import LoginPage
from apps.admin_portal.pages.dashboard_page import DashboardPage

@allure.epic("Admin Portal")
@allure.feature("Authentication")
@allure.story("User Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.app("admin_portal")
@pytest.mark.regression
def test_admin_successful_login(current_app):
    """Test that admin can successfully log in."""

    # Test data
    username = "admin@example.com"
    password = "secure_password"

    # Allure: Add test parameters
    allure.attach.json(
        {"username": username, "password": "***"},
        name="Test Parameters"
    )

    with allure.step("Initialize pages"):
        login_page = LoginPage(current_app.page)
        dashboard_page = DashboardPage(current_app.page)

    with allure.step("Navigate to login page"):
        current_app.navigate("/login")

    with allure.step("Perform login"):
        login_page.login(username, password)

    with allure.step("Verify successful login"):
        assert dashboard_page.is_loaded()
        welcome_msg = dashboard_page.get_welcome_message()
        assert "Admin" in welcome_msg

        # Attach final screenshot
        current_app.page.screenshot(path="test-results/screenshots/successful_login.png")
        allure.attach.file(
            "test-results/screenshots/successful_login.png",
            name="Final State",
            attachment_type=allure.attachment_type.PNG
        )

@allure.epic("Admin Portal")
@allure.feature("Authentication")
@allure.story("User Login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.app("admin_portal")
@pytest.mark.smoke
def test_admin_invalid_credentials(current_app):
    """Test that invalid credentials show error message."""

    with allure.step("Initialize login page"):
        login_page = LoginPage(current_app.page)
        current_app.navigate("/login")

    with allure.step("Attempt login with invalid credentials"):
        login_page.login("invalid@example.com", "wrong_password")

    with allure.step("Verify error message displayed"):
        error_msg = login_page.get_error_message()
        assert "invalid" in error_msg.lower()
```

#### 3.9.5 Running Tests and Generating Reports

```bash
# 1. Run tests (generates both Allure results and Playwright HTML)
pytest tests/ --app admin_portal --browser chromium

# 2. Generate and open Allure report
allure generate test-results/allure-results --clean -o test-results/allure-report
allure open test-results/allure-report

# 3. Open Playwright HTML report
# This is auto-generated in test-results/index.html
open test-results/index.html

# 4. Generate Allure report with history (compare runs)
allure generate test-results/allure-results \
    --clean \
    -o test-results/allure-report \
    --history=test-results/allure-history

# 5. Run with specific markers and generate report
pytest tests/ -m smoke --app admin_portal
allure generate test-results/allure-results --clean -o test-results/allure-report

# 6. Run tests in parallel with xdist and generate combined report
pytest tests/ --app admin_portal --app customer_portal \
    -n auto \
    --alluredir=test-results/allure-results
allure generate test-results/allure-results --clean -o test-results/allure-report
```

#### 3.9.6 Allure Report Features Usage

**Categories and Tags:**

```python
# infrastructure/fixtures/allure_tags.py
import allure
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_allure_environment(app_configs):
    """Set global Allure environment variables."""
    allure.environment(
        python_version="3.11+",
        pytest_version="8.0+",
        playwright_version="1.40+",
    )

@pytest.fixture
def assign_allure_labels(request):
    """
    Helper to assign Allure labels programmatically.

    Usage:
        def test_example(assign_allure_labels):
            assign_allure_labels({
                "epic": "Shopping",
                "feature": "Cart",
                "story": "Add to Cart",
                "severity": "critical"
            })
    """
    def _assign(labels: dict):
        for label_type, value in labels.items():
            if label_type == "epic":
                allure.epic(value)(request.node)
            elif label_type == "feature":
                allure.feature(value)(request.node)
            elif label_type == "story":
                allure.story(value)(request.node)
            elif label_type == "severity":
                severity = getattr(allure.severity_level, value.upper(), allure.severity_level.NORMAL)
                allure.severity(severity)(request.node)
            elif label_type == "tag":
                allure.tag(value)(request.node)

    return _assign
```

**Test Link Integration:**

```python
# conftest.py
@pytest.fixture(scope="session")
def configure_allure_links():
    """Configure external test management system links."""
    # TMS (Test Management System) integration
    allure.link(
        "https://tms.example.com/projects/WEB/tests",
        name="TMS Project",
        link_type=allure.link_type.LINK
    )

    # JIRA integration
    allure.link(
        "https://jira.example.com/browse/WEB",
        name="JIRA Board",
        link_type=allure.link_type.LINK
    )

# Usage in tests
@allure.link("https://tms.example.com/test/TC-1234", name="Test Case", link_type=allure.link_type.TMS)
@allure.issue("WEB-456", name="Bug Report")
def test_with_links():
    pass
```

#### 3.9.7 Report Structure After Test Run

```
test-results/
├── allure-results/              # Allure raw data
│   ├── environment.properties   # Test environment info
│   ├── categories.json          # Test categories
│   ├── *.json                   # Test result files
│   └── attachment/              # Screenshots, traces, etc.
│       ├── screenshot1.png
│       ├── trace1.zip
│       └── ...
├── allure-report/               # Generated HTML report
│   ├── index.html
│   ├── data/                    # JavaScript, CSS
│   └── history/                 # Historical data (if enabled)
├── screenshots/                 # Organized by app
│   ├── admin_portal/
│   │   ├── test_login_20250120_143022.png
│   │   └── ...
│   └── customer_portal/
│       └── ...
├── traces/                      # Organized by app
│   ├── admin_portal/
│   │   ├── test_login_20250120_143022_trace.zip
│   │   └── ...
│   └── ...
└── index.html                   # Playwright HTML Reporter
```

#### 3.9.8 Viewing Both Reports

**Allure Report:**
- Rich HTML with test history
- Categories, severity filtering
- Timeline view
- Attachment gallery (screenshots, traces)
- Environment information

**Playwright HTML Report:**
- Per-test timeline
- Interactive trace viewer
- Network request inspector
- Console logs
- Before/after screenshots
- Video playback

**Workflow:**

```
1. Run tests
   ↓
2. Open Allure report (overall status, history)
   ↓
3. Identify failed test
   ↓
4. Click Allure attachment: "Playwright Trace"
   ↓
5. Opens in Playwright Trace Viewer (detailed inspection)
   ↓
6. Or open Playwright HTML Report for full timeline
```

#### 3.9.9 CI/CD Integration

**GitHub Actions Example:**

```yaml
# .github/workflows/test.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest-playwright allure-pytest
          playwright install chromium

      - name: Run tests
        run: |
          pytest tests/ --alluredir=allure-results --video on --tracing on

      - name: Generate Allure Report
        if: always()
        run: |
          allure generate allure-results --clean -o allure-report

      - name: Upload Allure Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: allure-report/

      - name: Upload Playwright Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: test-results/
```

#### 3.9.10 Reporting Best Practices Summary

| Practice | Benefit |
|----------|---------|
| **Use Allure for history** | Track test trends over time |
| **Use Playwright HTML for debugging** | Deep trace inspection |
| **Attach traces to Allure** | One-click from report to trace |
| **Organize artifacts by app** | Easier navigation in large projects |
| **Use Allure steps for actions** | Better test documentation |
| **Set environment info** | Reproducible test results |
| **Use severity markers** | Prioritize fixing failed tests |
| **Link to external systems** | Integration with TMS/JIRA |

---

## 4. Key Takeaways for Framework Design

### 4.1 From pytest

1. **Fixture dependency injection** enables composable, reusable test components
2. **Conftest hierarchy** allows directory-local configuration and fixtures
3. **Parametrization** generates comprehensive test coverage from concise definitions
4. **Hook system** provides non-intrusive customization points
5. **Scope ordering** (session→function) ensures efficient resource utilization

### 4.2 From Playwright-Pytest

1. **Session-scoped browser, function-scoped context/page** balances performance and isolation
2. **Artifact recorder pattern** automatically captures debugging evidence
3. **Context argument override** via markers allows per-test configuration
4. **Browser channel support** enables testing against Chrome/Edge specifically
5. **Device emulation** built into context configuration

### 4.3 Recommended Starter Fixtures

```python
# conftest.py - Minimal starter set

@pytest.fixture(scope="session")
def env_config():
    """Environment configuration (URLs, credentials)."""
    return load_config()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, env_config):
    """Extend base context with project-specific config."""
    return {
        **browser_context_args,
        "base_url": env_config["base_url"],
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture
def authenticated_page(browser, browser_context_args, env_config):
    """Provide pre-authenticated page for tests."""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    page.goto(env_config["base_url"] + "/login")
    # Perform login
    yield page
    context.close()
```

---

## Appendix: Code Reference Locations

| Repository | File | Key Functions |
|------------|------|---------------|
| pytest | `src/_pytest/fixtures.py` | `FixtureDef.execute()`, `FixtureManager.getfixtureclosure()` |
| pytest | `src/_pytest/hookspec.py` | All hook specifications |
| playwright-pytest | `pytest_playwright/pytest_playwright/pytest_playwright.py` | `playwright()`, `browser()`, `context()`, `page()` |
| playwright-pytest | `pytest_playwright/pytest_playwright/pytest_playwright.py` | `ArtifactsRecorder` class |
| playwright-pytest | `tests/conftest.py` | `HTTPTestServer` for local testing |
| playwright-pytest | `tests/test_sync.py` | Comprehensive fixture usage examples |

---

**Document Version:** 1.2
**Updates:**
  - Added Section 3.8 - Multi-Web-Application Architecture Pattern
  - Added Section 3.9 - Unified Reporting Stack (Allure + Playwright HTML)
**Generated for:** Python Automation Testing Framework Development
