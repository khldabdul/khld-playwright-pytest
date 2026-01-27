"""
Root conftest.py for Playwright-Pytest Automation Framework.

This module provides:
- CLI options for multi-app and multi-environment testing
- App marker registration and filtering
- Session-scoped fixtures for shared resources
- Browser context configuration
- Environment information attachment for Allure reports
"""

import json
import os
import platform
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Playwright

# Import fixtures from infrastructure
from infrastructure.fixtures.session import (
    environment,
    env_config,
    test_data,
    test_results_dir,
    screenshots_dir,
    traces_dir,
    videos_dir,
)
from infrastructure.fixtures.app_factory import (
    app_configs,
    current_app,
)
# Import unified reporting hooks for enhanced Allure integration
from infrastructure.hooks.unified_reporting import (
    pytest_runtest_makereport,
    attach_screenshot,
    allure_step,
)


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
        choices=["dev", "staging", "production"],
        help="Environment to run tests against (dev/staging/production)"
    )
    parser.addoption(
        "--all-apps",
        action="store_true",
        help="Run tests for all configured apps"
    )


def pytest_configure(config):
    """Configure pytest for multi-app testing."""
    # Register custom markers
    config.addinivalue_line(
        "markers", "app(name): mark test as belonging to a specific app"
    )
    config.addinivalue_line(
        "markers", "smoke: smoke tests - quick validation"
    )
    config.addinivalue_line(
        "markers", "regression: regression tests - comprehensive coverage"
    )
    config.addinivalue_line(
        "markers", "api: API tests"
    )
    config.addinivalue_line(
        "markers", "ui: UI/E2E tests"
    )
    config.addinivalue_line(
        "markers", "slow: slow running tests"
    )
    config.addinivalue_line(
        "markers", "flaky: flaky test that may fail intermittently"
    )
    config.addinivalue_line(
        "markers", "critical: critical path tests"
    )

    # Create test results directories
    results_dir = Path("test-results")
    results_dir.mkdir(exist_ok=True)
    Path("allure-results").mkdir(exist_ok=True)  # Allure results in root
    (results_dir / "screenshots").mkdir(exist_ok=True)
    (results_dir / "traces").mkdir(exist_ok=True)
    (results_dir / "videos").mkdir(exist_ok=True)


def pytest_collection_modifyitems(items, config):
    """
    Filter tests by app if --app specified.

    This enables running tests for specific apps only:
        pytest --app admin_portal --app customer_portal
    """
    selected_apps = config.getoption("--app")
    all_apps = config.getoption("--all-apps")

    if all_apps or not selected_apps:
        return  # No filtering requested

    selected = []
    deselected = []

    for item in items:
        app_marker = item.get_closest_marker("app")
        if app_marker and app_marker.args[0] in selected_apps:
            selected.append(item)
        elif not app_marker:
            # Include tests without app marker (shared tests)
            selected.append(item)
        else:
            deselected.append(item)

    items[:] = selected

    if deselected:
        config.hook.pytest_deselected(items=deselected)


def pytest_report_header(config):
    """Add app and environment info to test report header."""
    apps = config.getoption("--app")
    env = config.getoption("--env")
    all_apps = config.getoption("--all-apps")

    lines = []
    lines.append("=" * 60)
    lines.append("Playwright-Pytest Automation Framework")
    lines.append("=" * 60)

    if all_apps:
        lines.append("Apps: All configured apps")
    elif apps:
        lines.append(f"Apps: {', '.join(apps)}")
    else:
        lines.append("Apps: All (no filter)")

    lines.append(f"Environment: {env}")
    lines.append("=" * 60)

    return lines


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, env_config):
    """
    Extend base browser context with framework configuration.

    This fixture is recognized by pytest-playwright and used to
    configure all browser contexts.
    """
    viewport = env_config.get("viewports", {}).get("desktop", {"width": 1920, "height": 1080})

    return {
        **browser_context_args,
        "viewport": viewport,
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, env_config):
    """
    Extend browser launch args with framework configuration.

    This fixture is recognized by pytest-playwright and used to
    configure browser launch options.
    """
    return {
        **browser_type_launch_args,
        "slow_mo": 0,  # Can be set via --slowmo CLI option
    }


@pytest.fixture(scope="session", autouse=True)
def attach_environment_information(request):
    """
    Attach environment information to Allure report.

    This fixture automatically attaches comprehensive environment details
    to every test run, including:
    - System information (OS, platform, hostname)
    - Python and pytest versions
    - Test environment (dev/staging/production)
    - Parallel execution worker ID (if applicable)

    This information is crucial for:
    - Reproducing failed tests accurately
    - Tracking flakiness across environments
    - Understanding test execution context
    """
    import sys

    env_info = {
        "environment": request.config.getoption("--env", "dev"),
        "python_version": sys.version,
        "platform": platform.platform(),
        "system": f"{platform.system()} {platform.release()}",
        "processor": platform.processor(),
        "python_implementation": platform.python_implementation(),
        "hostname": platform.node(),
    }

    # Add pytest version
    try:
        env_info["pytest_version"] = pytest.__version__
    except AttributeError:
        env_info["pytest_version"] = "unknown"

    # Add parallel execution info (if using xdist)
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "master")
    if worker_id != "master":
        env_info["worker_id"] = worker_id
        env_info["parallel_execution"] = True
    else:
        env_info["parallel_execution"] = False

    # Add CI/CD information (if available)
    if os.getenv("CI"):
        env_info["ci_environment"] = True
        env_info["ci_provider"] = os.getenv("CI_PROVIDER", "unknown")
        if os.getenv("GITHUB_ACTIONS"):
            env_info["ci_provider"] = "GitHub Actions"
            env_info["run_id"] = os.getenv("GITHUB_RUN_ID", "unknown")
        elif os.getenv("GITLAB_CI"):
            env_info["ci_provider"] = "GitLab CI"
        elif os.getenv("JENKINS_HOME"):
            env_info["ci_provider"] = "Jenkins"

    # Attach to Allure report
    allure.attach(
        json.dumps(env_info, indent=2, default=str),
        name="🖥️ Environment Information",
        attachment_type=allure.attachment_type.JSON,
    )

    # Also attach as a human-readable table
    env_table = "\n".join([
        "## Environment Information",
        "",
        f"| Key | Value |",
        f"|-----|-------|",
        f"| Environment | {env_info['environment']} |",
        f"| Python | {env_info['python_version'].split()[0]} |",
        f"| Platform | {env_info['platform']} |",
        f"| System | {env_info['system']} |",
        f"| Hostname | {env_info['hostname']} |",
        f"| Pytest | {env_info['pytest_version']} |",
        f"| Parallel | {'Yes (' + worker_id + ')' if env_info['parallel_execution'] else 'No'} |",
    ] + [
        f"| CI | {env_info.get('ci_provider', 'N/A')} |",
    ] if env_info.get("ci_environment") else [])

    allure.attach(
        env_table,
        name="🖥️ Environment (Summary)",
        attachment_type=allure.attachment_type.TEXT,
    )


# Re-export fixtures to make them available
__all__ = [
    "environment",
    "env_config",
    "test_data",
    "test_results_dir",
    "screenshots_dir",
    "traces_dir",
    "videos_dir",
    "app_configs",
    "current_app",
    "attach_screenshot",
    "allure_step",
]
