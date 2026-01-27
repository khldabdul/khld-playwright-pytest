"""
Allure reporting helpers for enhanced test reports.

This module provides utilities for attaching rich debugging information
to Allure reports, including HTTP requests/responses, performance data,
and test metadata.
"""

from __future__ import annotations

import functools
import json
import re
import time
from typing import Any, Callable

import allure
import pytest


def attach_http_request(
    method: str,
    url: str,
    headers: dict | None = None,
    body: Any = None,
    description: str | None = None,
) -> None:
    """
    Attach HTTP request details to Allure report.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        url: Request URL
        headers: Request headers (sanitized)
        body: Request body/payload
        description: Optional description of the request
    """
    # Sanitize headers to remove sensitive data
    safe_headers = _sanitize_headers(headers or {})

    request_info = {
        "method": method.upper(),
        "url": _sanitize_url(url),
        "headers": safe_headers,
        "body": _sanitize_body(body),
    }

    if description:
        request_info["description"] = description

    allure.attach(
        json.dumps(request_info, indent=2, default=str),
        name=f"📤 Request: {method.upper()} {url}",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_http_response(
    status_code: int,
    headers: dict | None = None,
    body: Any = None,
    response_time_ms: int | None = None,
    description: str | None = None,
) -> None:
    """
    Attach HTTP response details to Allure report.

    Args:
        status_code: HTTP status code
        headers: Response headers
        body: Response body
        response_time_ms: Response time in milliseconds
        description: Optional description of the response
    """
    # Determine status icon
    if 200 <= status_code < 300:
        status_icon = "✅"
        status_label = "Success"
    elif 300 <= status_code < 400:
        status_icon = "↪️"
        status_label = "Redirect"
    elif 400 <= status_code < 500:
        status_icon = "⚠️"
        status_label = "Client Error"
    elif 500 <= status_code < 600:
        status_icon = "❌"
        status_label = "Server Error"
    else:
        status_icon = "❓"
        status_label = "Unknown"

    response_info = {
        "status_code": status_code,
        "status_label": status_label,
        "headers": headers or {},
        "body": _truncate_body(body),
    }

    if response_time_ms is not None:
        response_info["response_time_ms"] = response_time_ms

    if description:
        response_info["description"] = description

    name = f"{status_icon} Response: {status_code} {status_label}"
    if response_time_ms is not None:
        name += f" ({response_time_ms}ms)"

    allure.attach(
        json.dumps(response_info, indent=2, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_performance_metric(
    operation: str,
    duration_ms: int,
    threshold_ms: int | None = None,
) -> bool:
    """
    Attach performance metric to Allure report.

    Args:
        operation: Operation name (e.g., "GET /booking/:id")
        duration_ms: Actual duration in milliseconds
        threshold_ms: Optional threshold for pass/fail determination

    Returns:
        True if within threshold (or no threshold), False otherwise
    """
    passed = threshold_ms is None or duration_ms <= threshold_ms
    status_icon = "✅" if passed else "⏱️"

    metric = {
        "operation": operation,
        "duration_ms": duration_ms,
        "status": "PASS" if passed else "SLOW",
    }

    if threshold_ms is not None:
        metric["threshold_ms"] = threshold_ms
        metric["diff_ms"] = duration_ms - threshold_ms

    allure.attach(
        json.dumps(metric, indent=2),
        name=f"{status_icon} Performance: {operation}",
        attachment_type=allure.attachment_type.JSON,
    )

    return passed


def attach_test_metadata(
    test_id: str | None = None,
    test_case: str | None = None,
    requirements: list[str] | None = None,
    tags: list[str] | None = None,
) -> None:
    """
    Attach test metadata to Allure report.

    Args:
        test_id: Unique test identifier
        test_case: Test case ID from test management system
        requirements: List of requirement IDs
        tags: List of test tags
    """
    metadata: dict[str, Any] = {}

    if test_id:
        metadata["test_id"] = test_id
    if test_case:
        metadata["test_case"] = test_case
    if requirements:
        metadata["requirements"] = requirements
    if tags:
        metadata["tags"] = tags

    if metadata:
        allure.attach(
            json.dumps(metadata, indent=2),
            name="📋 Test Metadata",
            attachment_type=allure.attachment_type.JSON,
        )


def attach_error_context(
    error: Exception,
    context: dict[str, Any] | None = None,
) -> None:
    """
    Attach error context to Allure report.

    Args:
        error: The exception that occurred
        context: Additional context data
    """
    error_info = {
        "type": type(error).__name__,
        "message": str(error),
        "context": context or {},
    }

    allure.attach(
        json.dumps(error_info, indent=2, default=str),
        name="❌ Error Context",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_json_data(
    data: Any,
    name: str = "JSON Data",
) -> None:
    """Attach JSON data to Allure report."""
    allure.attach(
        json.dumps(data, indent=2, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_text(
    text: str,
    name: str = "Text",
) -> None:
    """Attach plain text to Allure report."""
    allure.attach(
        text,
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


# Context manager for timed operations
class TimedOperation:
    """Context manager for timing operations and attaching to Allure."""

    def __init__(self, operation_name: str, threshold_ms: int | None = None):
        """
        Initialize timed operation.

        Args:
            operation_name: Name of the operation being timed
            threshold_ms: Optional threshold for performance warning
        """
        self.operation_name = operation_name
        self.threshold_ms = threshold_ms
        self.start_time = None
        self.duration_ms = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            self.duration_ms = int((time.time() - self.start_time) * 1000)
            attach_performance_metric(
                operation=self.operation_name,
                duration_ms=self.duration_ms,
                threshold_ms=self.threshold_ms,
            )
        return False


# Helper functions
def _sanitize_headers(headers: dict) -> dict:
    """Sanitize headers to remove sensitive information."""
    sensitive_keys = {
        "authorization",
        "token",
        "api-key",
        "apikey",
        "x-api-key",
        "cookie",
        "set-cookie",
    }

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_keys:
            sanitized[key] = "***REDACTED***"
        else:
            sanitized[key] = value

    return sanitized


def _sanitize_url(url: str) -> str:
    """Sanitize URL to remove sensitive query parameters."""
    # Remove API keys and tokens from URL
    import re

    # Pattern to match common sensitive query params
    patterns = [
        (r"([?&])(api[_-]?key|token|auth|password)[=][^&]*", r"\1\2=***REDACTED***"),
    ]

    sanitized = url
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized


def _sanitize_body(body: Any) -> Any:
    """Sanitize request body to remove sensitive fields."""
    if not body:
        return body

    if isinstance(body, dict):
        sanitized = {}
        sensitive_keys = {
            "password",
            "token",
            "api_key",
            "secret",
            "auth",
            "credit_card",
            "ssn",
        }

        for key, value in body.items():
            if key.lower() in sensitive_keys:
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = _sanitize_body(value)
            elif isinstance(value, list):
                sanitized[key] = [_sanitize_body(item) for item in value]
            else:
                sanitized[key] = value

        return sanitized

    if isinstance(body, list):
        return [_sanitize_body(item) for item in body]

    return body


def _truncate_body(body: Any, max_size: int = 10000) -> Any:
    """Truncate body if too large for attachment."""
    body_str = json.dumps(body, default=str)

    if len(body_str) <= max_size:
        return body

    # Return truncated version
    return {
        "data": body_str[:max_size],
        "_truncated": True,
        "_original_size": len(body_str),
    }


def markdown_to_html(markdown: str) -> str:
    """
    Convert markdown to HTML for use in Allure descriptions.

    Supports common markdown elements:
    - Headers (##, ###)
    - Bold (**text**)
    - Italic (*text*)
    - Lists (- item)
    - Code blocks (```code```)
    - Inline code (`code`)
    - Links [text](url)

    Args:
        markdown: Markdown formatted string

    Returns:
        HTML formatted string
    """
    if not markdown:
        return ""

    html = markdown

    # Escape HTML characters first (but preserve our markdown)
    html = html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Headers (##, ###)
    html = re.sub(r"^### (.+)$", r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Bold (**text**)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)

    # Italic (*text*)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # Code blocks (```code```)
    html = re.sub(
        r"```(\w*)\n(.+?)```",
        r"<pre><code>\2</code></pre>",
        html,
        flags=re.DOTALL,
    )

    # Inline code (`code`)
    html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)

    # Links [text](url)
    html = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r'<a href="\2">\1</a>', html)

    # Unordered lists (- item)
    lines = html.split("\n")
    in_list = False
    result_lines = []

    for line in lines:
        if line.strip().startswith("- "):
            if not in_list:
                result_lines.append("<ul>")
                in_list = True
            content = line.strip()[2:]
            result_lines.append(f"  <li>{content}</li>")
        else:
            if in_list:
                result_lines.append("</ul>")
                in_list = False
            result_lines.append(line)

    if in_list:
        result_lines.append("</ul>")

    html = "\n".join(result_lines)

    # Paragraphs (double newline)
    paragraphs = html.split("\n\n")
    html = "</p><p>".join(p.strip() for p in paragraphs if p.strip())
    html = f"<p>{html}</p>"

    # Clean up empty paragraphs
    html = html.replace("<p></p>", "")
    html = html.replace("<p><ul>", "<ul>")
    html = html.replace("</ul></p>", "</ul>")
    html = html.replace("<p><h", "<h")
    html = html.replace("</h4></p>", "</h4>")
    html = html.replace("</h3></p>", "</h3>")
    html = html.replace("<p><pre>", "<pre>")
    html = html.replace("</pre></p>", "</pre>")

    return html


def markdown_description(markdown_text: str) -> Callable:
    """
    Decorator that converts markdown to HTML and sets as Allure description.

    Usage:
        @markdown_description(\"\"\"
        ## Test Overview

        This test verifies **important functionality**.

        - Check item 1
        - Check item 2
        \"\"\")
        def test_something():
            pass
    """

    def decorator(func: Callable) -> Callable:
        html = markdown_to_html(markdown_text.strip())

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Apply the HTML description using allure's description_html
        allure.description_html(html)(wrapper)
        return wrapper

    return decorator


def api_test(
    epic: str,
    feature: str,
    story: str,
    testcase: str,
    requirement: str,
    severity: str = allure.severity_level.NORMAL,
    description: str = "",
    title: str = "",
    link: str | None = None,
    link_name: str = "API Docs",
    critical: bool = False,
    smoke: bool = False,
    regression: bool = False,
) -> Callable:
    """
    Composite decorator for API tests that combines common Allure decorators.

    Reduces decorator bloat from 12+ lines to a single line.

    Args:
        epic: Epic name (e.g., "Petstore API")
        feature: Feature name (e.g., "Authentication")
        story: Story name (e.g., "User Login")
        testcase: Test case ID (e.g., "TC-PS-001")
        requirement: Requirement ID (e.g., "US-AUTH-001")
        severity: Severity level (default: NORMAL)
        description: Markdown description (optional)
        title: Test title (optional, defaults to function name)
        link: URL link to documentation (optional)
        link_name: Name for the link (default: "API Docs")
        critical: Whether test is critical (default: False)
        smoke: Whether test is smoke test (default: False)
        regression: Whether test is regression test (default: False)

    Usage:
        @api_test(
            epic="Petstore API",
            feature="Authentication",
            story="User Login",
            testcase="TC-PS-001",
            requirement="US-AUTH-001",
            severity=allure.severity_level.CRITICAL,
            title="Login with valid credentials",
            link="https://api.example.com/docs/login",
            description=\"\"\"
            Verify user can login with valid credentials.

            **Test Steps:**
            1. Send login request
            2. Verify token returned

            **Business Value:**
            Core authentication flow.
            \"\"\",
            smoke=True
        )
        def test_login(client):
            pass
    """
    def decorator(func: Callable) -> Callable:
        # Apply all decorators
        func = allure.epic(epic)(func)
        func = allure.feature(feature)(func)
        func = allure.story(story)(func)
        func = allure.label("layer", "api")(func)
        func = allure.label("type", "functional")(func)
        func = pytest.mark.api(func)
        func = pytest.mark.testcase(testcase)(func)
        func = pytest.mark.requirement(requirement)(func)
        func = allure.severity(severity)(func)

        if description:
            func = allure.description_html(markdown_to_html(description))(func)
        if title:
            func = allure.title(title)(func)
        if link:
            func = allure.link(link, name=link_name)(func)
        if critical:
            func = pytest.mark.critical(func)
        if smoke:
            func = pytest.mark.smoke(func)
        if regression:
            func = pytest.mark.regression(func)

        return func

    return decorator


def e2e_test(
    epic: str,
    feature: str,
    story: str,
    testcase: str,
    requirement: str,
    app: str,
    severity: str = allure.severity_level.NORMAL,
    description: str = "",
    title: str = "",
    link: str | None = None,
    link_name: str = "App",
    critical: bool = False,
    smoke: bool = False,
    regression: bool = False,
) -> Callable:
    """
    Composite decorator for E2E tests that combines common Allure decorators.

    Reduces decorator bloat from 12+ lines to a single line.

    Args:
        epic: Epic name (e.g., "Sauce Demo E2E")
        feature: Feature name (e.g., "Authentication")
        story: Story name (e.g., "User Login")
        testcase: Test case ID (e.g., "TC-SD-001")
        requirement: Requirement ID (e.g., "US-AUTH-001")
        app: Application name (e.g., "sauce_demo")
        severity: Severity level (default: NORMAL)
        description: Markdown description (optional)
        title: Test title (optional, defaults to function name)
        link: URL link to documentation (optional)
        link_name: Name for the link (default: "App")
        critical: Whether test is critical (default: False)
        smoke: Whether test is smoke test (default: False)
        regression: Whether test is regression test (default: False)

    Usage:
        @e2e_test(
            epic="Sauce Demo E2E",
            feature="Authentication",
            story="User Login",
            testcase="TC-SD-001",
            requirement="US-AUTH-001",
            app="sauce_demo",
            severity=allure.severity_level.CRITICAL,
            title="Login with valid credentials",
            link="https://www.saucedemo.com/",
            description=\"\"\"
            Verify user can login with valid credentials.

            **Test Steps:**
            1. Navigate to login page
            2. Enter credentials
            3. Verify redirect to inventory

            **Business Value:**
            Core authentication flow.
            \"\"\",
            smoke=True
        )
        def test_login(login_page, inventory_page):
            pass
    """
    def decorator(func: Callable) -> Callable:
        # Apply all decorators
        func = allure.epic(epic)(func)
        func = allure.feature(feature)(func)
        func = allure.story(story)(func)
        func = allure.label("layer", "e2e")(func)
        func = allure.label("type", "functional")(func)
        func = allure.label("app", app)(func)
        func = pytest.mark.app(app)(func)
        func = pytest.mark.e2e(func)
        func = pytest.mark.testcase(testcase)(func)
        func = pytest.mark.requirement(requirement)(func)
        func = allure.severity(severity)(func)

        if description:
            func = allure.description_html(markdown_to_html(description))(func)
        if title:
            func = allure.title(title)(func)
        if link:
            func = allure.link(link, name=link_name)(func)
        if critical:
            func = pytest.mark.critical(func)
        if smoke:
            func = pytest.mark.smoke(func)
        if regression:
            func = pytest.mark.regression(func)

        return func

    return decorator
