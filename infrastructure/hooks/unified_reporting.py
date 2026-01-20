"""Unified reporting hook for Allure and Playwright integration."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import Page


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

    # Attach artifacts on failure
    if report.failed:
        _attach_failure_artifacts(item, report, app_name)

    # Always attach metadata
    _attach_test_metadata(item, app_name)


def _attach_failure_artifacts(item, report, app_name: str) -> None:
    """
    Attach screenshots, traces, and videos to Allure on failure.

    Args:
        item: pytest test item
        report: Test report
        app_name: Name of the app being tested
    """
    # Skip if no page object (e.g., API tests)
    page: Page | None = item.funcargs.get("page")
    if not page:
        # For API tests, just attach error details
        if report.longrepr:
            allure.attach(
                str(report.longrepr),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
        return

    test_name = _sanitize_filename(item.name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Screenshot
    _attach_screenshot(page, app_name, test_name, timestamp)

    # 2. Playwright Trace (if available)
    _attach_trace(item, app_name, test_name, timestamp)

    # 3. Error message
    if report.longrepr:
        allure.attach(
            str(report.longrepr),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )


def _attach_screenshot(page: Page, app_name: str, test_name: str, timestamp: str) -> None:
    """Attach screenshot to Allure report."""
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


def _attach_trace(item, app_name: str, test_name: str, timestamp: str) -> None:
    """Attach Playwright trace to Allure report."""
    trace_dir = Path("test-results/traces") / app_name
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Find trace file from output_path fixture
    if "output_path" in item.funcargs:
        output_path = Path(item.funcargs["output_path"])
        trace_files = list(output_path.glob("trace*.zip"))

        if trace_files:
            trace_path = trace_files[0]
            organized_trace = trace_dir / f"{test_name}_{timestamp}_trace.zip"

            try:
                # Copy to organized location
                import shutil
                shutil.copy2(trace_path, organized_trace)

                allure.attach.file(
                    str(organized_trace),
                    name="Playwright Trace (open with: npx playwright show-trace)",
                    attachment_type=allure.attachment_type.ZIP
                )
            except Exception as e:
                allure.attach(
                    f"Failed to attach trace: {e}",
                    name="Trace Error",
                    attachment_type=allure.attachment_type.TEXT
                )


def _attach_test_metadata(item, app_name: str) -> None:
    """Attach test metadata to Allure."""
    metadata: dict[str, Any] = {
        "test_id": item.nodeid,
        "app": app_name,
        "markers": [mark.name for mark in item.iter_markers()],
        "file": str(item.fspath),
        "function": item.name,
    }

    allure.attach(
        json.dumps(metadata, indent=2),
        name="Test Metadata",
        attachment_type=allure.attachment_type.JSON
    )


def _sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be used as a filename.

    Args:
        name: Original name

    Returns:
        Sanitized filename
    """
    # Replace problematic characters
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '[', ']']:
        name = name.replace(char, '_')
    return name[:100]  # Limit length


@pytest.fixture
def attach_screenshot(page: Page):
    """
    Fixture to manually attach screenshot during test.

    Usage:
        def test_example(attach_screenshot):
            # ... do something
            attach_screenshot("After clicking button")
    """
    def _attach(name: str = "Screenshot", full_page: bool = False) -> None:
        try:
            screenshot = page.screenshot(full_page=full_page)
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass  # Screenshot capture failed, continue

    return _attach


@pytest.fixture
def allure_step():
    """
    Fixture to create Allure steps programmatically.

    Usage:
        def test_example(allure_step):
            with allure_step("Login to application"):
                # ... login code
    """
    return allure.step
