"""Unified reporting hook for Allure and Playwright integration."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import Page

from infrastructure.utils.allure_helpers import markdown_to_html


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Unified reporting that feeds both Allure and Playwright HTML.

    This hook:
    1. Captures test metadata for Allure
    2. Attaches screenshots to Allure on failure
    3. Attaches Playwright traces to Allure
    4. Categorizes test failures for better triage
    5. Stores report data for custom processing
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

    # Attach artifacts on failure or success
    if report.failed:
        _attach_failure_artifacts(item, report, app_name)
        # Categorize the failure for better triage
        _categorize_failure(item, report)
    elif report.passed:
        # Attach success screenshots for E2E tests only
        _attach_success_artifacts(item, report, app_name)

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

    # 3. Video Recording (if available)
    _attach_video(item, app_name, test_name, timestamp, success=False)

    # 4. HAR File (if available)
    _attach_har(item, app_name, test_name, timestamp)

    # 5. Error message
    if report.longrepr:
        allure.attach(
            str(report.longrepr),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )


def _attach_success_artifacts(item, report, app_name: str) -> None:
    """
    Attach screenshots to Allure on successful E2E test completion.

    This provides:
    - Visual verification of test success
    - Documentation of final application state
    - Useful reference for smoke test verification

    Args:
        item: pytest test item
        report: Test report
        app_name: Name of the app being tested
    """
    # Only for E2E tests (have page object and e2e marker)
    page: Page | None = item.funcargs.get("page")
    if not page:
        return

    # Check if this is an E2E test
    e2e_marker = item.get_closest_marker("e2e")
    if not e2e_marker:
        return

    test_name = _sanitize_filename(item.name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Attach final state screenshot
    _attach_screenshot(page, app_name, test_name, timestamp, success=True)

    # Attach video recording for E2E tests
    _attach_video(item, app_name, test_name, timestamp, success=True)

    # Attach HAR file for E2E tests
    _attach_har(item, app_name, test_name, timestamp)


def _attach_screenshot(page: Page, app_name: str, test_name: str, timestamp: str, success: bool = False) -> None:
    """Attach screenshot to Allure report."""
    screenshot_dir = Path("test-results/screenshots") / app_name
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    # Different naming for success vs failure screenshots
    suffix = "success" if success else "failure"
    screenshot_path = screenshot_dir / f"{test_name}_{timestamp}_{suffix}.png"

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path),
            name="✅ Success Screenshot" if success else "Failure Screenshot",
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


def _attach_video(item, app_name: str, test_name: str, timestamp: str, success: bool = False) -> None:
    """
    Attach video recording to Allure report.

    Args:
        item: pytest test item
        app_name: Name of the app being tested
        test_name: Sanitized test name
        timestamp: Timestamp string
        success: Whether test passed (affects attachment naming)
    """
    # Find video file from output_path fixture
    if "output_path" not in item.funcargs:
        return

    output_path = Path(item.funcargs["output_path"])
    video_files = list(output_path.glob("video*.webm"))

    if not video_files:
        return

    video_path = video_files[0]
    video_dir = Path("test-results/videos") / app_name
    video_dir.mkdir(parents=True, exist_ok=True)

    suffix = "success" if success else "failure"
    organized_video = video_dir / f"{test_name}_{timestamp}_{suffix}.webm"

    try:
        # Copy to organized location
        import shutil
        shutil.copy2(video_path, organized_video)

        allure.attach.file(
            str(organized_video),
            name=f"{'✅ ' if success else ''}Video Recording",
            attachment_type=allure.attachment_type.WEBM
        )
    except Exception as e:
        allure.attach(
            f"Failed to attach video: {e}",
            name="Video Error",
            attachment_type=allure.attachment_type.TEXT
        )


def _attach_har(item, app_name: str, test_name: str, timestamp: str) -> None:
    """
    Attach HAR (HTTP Archive) file to Allure report.

    HAR files contain complete network activity including:
    - All HTTP requests and responses
    - Headers, cookies, timing information
    - Request and response bodies

    Args:
        item: pytest test item
        app_name: Name of the app being tested
        test_name: Sanitized test name
        timestamp: Timestamp string
    """
    # Search for HAR files in multiple locations
    har_files = []

    # 1. Check output_path fixture (pytest-playwright)
    if "output_path" in item.funcargs:
        output_path = Path(item.funcargs["output_path"])
        har_files = list(output_path.glob("*.har"))

    # 2. Check test-results/{test_name}/ directory
    if not har_files:
        test_output_dir = Path("test-results") / test_name
        if test_output_dir.exists():
            har_files = list(test_output_dir.glob("*.har"))

    # 3. Check pytest-playwright's default test-results location
    if not har_files:
        # pytest-playwright creates subdirectories per test
        test_results_base = Path("test-results")
        if test_results_base.exists():
            # Search in subdirectories that match the test name
            for subdir in test_results_base.iterdir():
                if subdir.is_dir() and test_name in subdir.name:
                    har_files = list(subdir.glob("*.har"))
                    if har_files:
                        break

    if not har_files:
        return

    har_path = har_files[0]
    har_dir = Path("test-results/hars") / app_name
    har_dir.mkdir(parents=True, exist_ok=True)

    organized_har = har_dir / f"{test_name}_{timestamp}.har"

    try:
        # Copy to organized location
        import shutil
        shutil.copy2(har_path, organized_har)

        # Get file size for reporting
        file_size_mb = organized_har.stat().st_size / (1024 * 1024)

        allure.attach.file(
            str(organized_har),
            name=f"🌐 Network HAR ({file_size_mb:.2f} MB)",
            attachment_type=allure.attachment_type.JSON  # HAR is JSON-based
        )

        # Also attach a summary of network requests
        _attach_har_summary(organized_har)

    except Exception as e:
        allure.attach(
            f"Failed to attach HAR: {e}",
            name="HAR Error",
            attachment_type=allure.attachment_type.TEXT
        )


def _attach_har_summary(har_path: Path) -> None:
    """
    Attach a human-readable summary of the HAR file.

    Args:
        har_path: Path to the HAR file
    """
    try:
        import json

        with open(har_path) as f:
            har_data = json.load(f)

        # Extract useful information from HAR
        entries = har_data.get("log", {}).get("entries", [])

        # Build summary
        summary_lines = [
            "## Network Activity Summary",
            "",
            f"**Total Requests:** {len(entries)}",
            "",
            "### Request Breakdown by Status:",
            "",
        ]

        # Count by status
        status_counts = {}
        for entry in entries:
            response = entry.get("response", {})
            status = response.get("status", 0)
            status_counts[status] = status_counts.get(status, 0) + 1

        for status in sorted(status_counts.keys(), reverse=True):
            count = status_counts[status]
            emoji = "✅" if 200 <= status < 300 else "⚠️" if 300 <= status < 400 else "❌"
            summary_lines.append(f"- {emoji} Status {status}: {count} requests")

        summary_lines.extend([
            "",
            "### Slowest Requests (Top 10):",
            "",
            "| Status | Method | URL | Time |",
            "|--------|--------|-----|------|",
        ])

        # Sort by total time
        sorted_entries = sorted(
            entries,
            key=lambda e: e.get("timings", {}).get("receive", 0) + e.get("timings", {}).get("wait", 0),
            reverse=True
        )[:10]

        for entry in sorted_entries:
            request = entry.get("request", {})
            response = entry.get("response", {})
            timings = entry.get("timings", {})

            total_time = sum(timings.get(k, 0) for k in ["blocked", "dns", "connect", "send", "wait", "receive"])
            method = request.get("method", "UNKNOWN")
            url = request.get("url", "UNKNOWN")[:60]  # Truncate long URLs
            status = response.get("status", 0)

            summary_lines.append(f"| {status} | {method} | {url} | {total_time:.0f}ms |")

        summary_text = "\n".join(summary_lines)

        allure.attach(
            summary_text,
            name="🌐 Network Summary",
            attachment_type=allure.attachment_type.TEXT
        )

    except Exception as e:
        # If summary fails, just attach a basic message
        allure.attach(
            f"HAR file available but summary generation failed: {e}",
            name="Network Summary (partial)",
            attachment_type=allure.attachment_type.TEXT
        )


def _attach_test_metadata(item, app_name: str) -> None:
    """
    Attach test metadata to Allure.

    Extracts structured metadata from pytest markers and fixtures,
    including test case IDs, requirements, and custom tags.
    """
    # Extract test_id from testcase marker if present
    testcase_marker = item.get_closest_marker("testcase")
    test_id = testcase_marker.args[0] if testcase_marker else item.nodeid

    # Extract requirements from custom markers (format: @pytest.mark.requirement("REQ-123"))
    requirements = []
    for mark in item.iter_markers():
        if mark.name == "requirement" and mark.args:
            requirements.extend(mark.args)

    # Extract user-defined tags (anything that's not a built-in pytest/allure marker)
    built_in_markers = {
        "app", "api", "ui", "e2e", "smoke", "regression", "slow", "critical",
        "flaky", "integration", "testcase", "requirement", "allure_link",
        "allure_label", "allure_description", "allure_step", "allure_title",
        "allure_story", "allure_feature", "allure_epic", "allure_severity",
        "allure_tag", "allure_id", "allure_issue", "allure_tms", "allure_owner",
    }
    custom_tags = [mark.name for mark in item.iter_markers() if mark.name not in built_in_markers]

    metadata: dict[str, Any] = {
        "test_id": test_id,
        "app": app_name,
        "test_name": item.name,
        "file": str(item.fspath),
        "requirements": requirements if requirements else None,
        "tags": custom_tags if custom_tags else None,
    }

    # Remove None values
    metadata = {k: v for k, v in metadata.items() if v is not None}

    allure.attach(
        json.dumps(metadata, indent=2),
        name="📋 Test Metadata",
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


# ============================================================================
# Test Failure Categorization
# ============================================================================

def _categorize_failure(item, report) -> None:
    """
    Categorize test failures for better triage and analysis.

    This function analyzes test failures and assigns them to categories
    based on error type and message. Categories appear in Allure reports
    and help with:
    - Quick identification of failure patterns
    - Separate infrastructure bugs from product bugs
    - Better triage for failed tests

    Categories:
    - Infrastructure Failure: Network errors, API unavailability, timeouts
    - Performance Issue: Slow response times, loading delays
    - Test Code Defect: Flaky tests, wrong setup, test code errors
    - Product Bug: Application logic errors, unexpected behavior

    Args:
        item: pytest test item
        report: Test report
    """
    # Get the error information
    longrepr = report.longrepr
    if not longrepr:
        return

    # Convert to string for pattern matching
    error_message = str(longrepr)
    error_type = None

    # Extract error type from longrepr
    if hasattr(longrepr, "typename"):
        error_type = longrepr.typename
    else:
        # Try to extract error type from string
        match = re.search(r"(\w+Error)", error_message.split("\n")[0])
        if match:
            error_type = match.group(1)

    # Categorize based on error type and message
    category = _determine_category(error_type, error_message, item)

    # Attach category as a label to Allure
    if category:
        allure.label("category", category)
        _attach_category_description(category, error_message)


def _determine_category(error_type: str | None, error_message: str, item) -> str:
    """
    Determine the failure category based on error analysis.

    Args:
        error_type: The exception type
        error_message: Full error message
        item: pytest test item

    Returns:
        Category name
    """
    # Check infrastructure failures first
    if _is_infrastructure_error(error_type, error_message):
        return "Infrastructure Failure"

    # Check performance issues
    if _is_performance_error(error_type, error_message):
        return "Performance Issue"

    # Check test code defects
    if _is_test_defect(error_type, error_message, item):
        return "Test Code Defect"

    # Default to Product Bug
    return "Product Bug"


def _is_infrastructure_error(error_type: str | None, error_message: str) -> bool:
    """Check if error is infrastructure-related."""
    infrastructure_patterns = [
        r"ConnectionError",
        r"NewConnectionError",
        r"MaxRetryError",
        r"TimeoutError",
        r"502 Bad Gateway",
        r"503 Service Unavailable",
        r"504 Gateway Timeout",
        r"Connection refused",
        r"Network.*unreachable",
        r"Host not found",
        r"SSL.*error",
        r"TLS.*error",
        r"playwright.*Timeout",
    ]

    for pattern in infrastructure_patterns:
        if re.search(pattern, error_message, re.IGNORECASE):
            return True

    if error_type:
        infra_types = ["ConnectionError", "NewConnectionError", "MaxRetryError", "ConnectTimeout"]
        return any(t in error_type for t in infra_types)

    return False


def _is_performance_error(error_type: str | None, error_message: str) -> bool:
    """Check if error is performance-related."""
    performance_keywords = ["timeout", "slow", "performance", "latency", "took too long"]

    error_lower = error_message.lower()
    for keyword in performance_keywords:
        if keyword in error_lower:
            return True

    if error_type and "Timeout" in error_type:
        return True

    return False


def _is_test_defect(error_type: str | None, error_message: str, item) -> bool:
    """Check if error is in test code."""
    # Check for flaky marker
    if item.get_closest_marker("flaky"):
        return True

    # Common test code errors
    test_defect_patterns = [
        r"NoneType.*attribute",
        r"KeyError",
        r"NameError.*not defined",
        r"fixture.*not found",
    ]

    for pattern in test_defect_patterns:
        if re.search(pattern, error_message, re.IGNORECASE):
            return True

    # Check if traceback points to test file
    if "tests/" in error_message.lower():
        return True

    return False


def _attach_category_description(category: str, error_message: str) -> None:
    """Attach category description to Allure report."""
    descriptions = {
        "Infrastructure Failure": """
## Infrastructure Failure

This test failed due to infrastructure or environmental issues.

**Common causes:**
- Network connectivity problems
- External API/service unavailability
- DNS resolution failures

**Recommended actions:**
- Verify external services are running
- Check network connectivity
- Re-run test to confirm transient failure
""",
        "Performance Issue": """
## Performance Issue

This test failed due to performance-related problems.

**Common causes:**
- Response time exceeded threshold
- Page load timeout
- Resource loading delay

**Recommended actions:**
- Check system resources
- Verify application performance
- Consider adjusting timeout thresholds
""",
        "Test Code Defect": """
## Test Code Defect

This test failed due to an issue with the test code.

**Common causes:**
- Incorrect test setup
- Missing or incorrect test data
- Flaky test logic

**Recommended actions:**
- Review test code for errors
- Verify test data setup
- Fix test implementation
""",
        "Product Bug": """
## Product Bug

This test failed due to a defect in the application code.

**Common causes:**
- Application logic error
- Unexpected behavior
- Missing functionality

**Recommended actions:**
- Review application logs
- Debug application code
- Create bug ticket if needed
""",
    }

    description = descriptions.get(category, "")
    if description:
        # Convert markdown to HTML for proper rendering in Allure
        html_description = markdown_to_html(description.strip())
        allure.attach(
            html_description,
            name=f"Category: {category}",
            attachment_type=allure.attachment_type.HTML
        )
