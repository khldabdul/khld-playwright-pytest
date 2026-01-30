"""HAR (HTTP Archive) recording fixtures for network debugging.

This module provides fixtures for recording network activity during E2E tests.
HAR files capture complete HTTP traffic including requests, responses, headers, and timing.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext


@pytest.fixture(scope="function")
def har_recording(context: BrowserContext, request):
    """
    Enable HAR recording for the test context.

    This fixture starts HAR recording at the beginning of the test
    and stops it at the end, automatically saving the HAR file
    to the test output directory.

    Usage:
        def test_with_har(page, har_recording):
            page.goto("https://example.com")
            # HAR file will be automatically attached to Allure report

    Note: Requires pytest-playwright plugin.

    Args:
        context: Playwright browser context
        request: pytest request object for test metadata
    """
    # Get test output path from pytest-playwright
    # The plugin creates a unique directory for each test
    test_name = request.node.name.replace("/", "_").replace("\\", "_")
    output_dir = Path("test-results") / test_name
    output_dir.mkdir(parents=True, exist_ok=True)

    har_path = output_dir / "network.har"

    # Check if HAR recording is enabled via environment variable
    # This allows selective HAR recording to avoid large file sizes
    enable_har = os.getenv("PLAYWRIGHT_HAR", "false").lower() in ("true", "1", "on")

    if not enable_har:
        yield False  # HAR recording disabled
        return

    # Start HAR recording
    # Playwright 1.17+ supports context.record_har()
    try:
        context.record_har(
            path=str(har_path),
            content="attach",  # Include request/response bodies
        )
        yield True  # HAR recording enabled
    except AttributeError:
        # Older Playwright versions don't support HAR recording
        yield False
    finally:
        # Stop HAR recording
        try:
            context.stop_har()
        except (AttributeError, Exception):
            # May fail if recording wasn't started or already stopped
            pass
