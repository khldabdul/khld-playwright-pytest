"""The Internet JavaScript Dialogs Tests.

This test suite covers JavaScript dialog handling including:
- Alert dialogs
- Confirm dialogs (accept/dismiss)
- Prompt dialogs

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="The Internet E2E",
    feature="JavaScript Dialogs",
    story="Alert Handling",
    testcase="TC-TI-040",
    requirement="US-TI-ALERT-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Handle JavaScript alert",
    link="https://the-internet.herokuapp.com/javascript_alerts",
    description="""
Verify that JavaScript alert can be handled.

**Test Steps:**
1. Navigate to JavaScript alerts page
2. Set up dialog handler to accept
3. Trigger alert dialog
4. Verify success message appears

**Test Coverage:**
- Alert dialog handling
- Dialog acceptance
- Result verification

**Business Value:}
Tests browser dialog handling capabilities.
""",
)
def test_js_alert(js_alerts_page, the_internet_config):
    """TC-TI-040: Handle JavaScript alert."""

    with allure.step("Navigate to alerts page"):
        js_alerts_page.navigate_to_alerts(the_internet_config.base_url)

    with allure.step("Set up alert handler and trigger alert"):
        js_alerts_page.page.once("dialog", lambda dialog: dialog.accept())
        js_alerts_page.click_alert()

    with allure.step("Verify result message"):
        result = js_alerts_page.get_result_text()
        assert "You successfully clicked an alert" in result


@e2e_test(
    epic="The Internet E2E",
    feature="JavaScript Dialogs",
    story="Confirm Dialog",
    testcase="TC-TI-041",
    requirement="US-TI-ALERT-002",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Handle JavaScript confirm - Accept",
    link="https://the-internet.herokuapp.com/javascript_alerts",
    description="""
Verify that confirm dialog can be accepted.

**Test Steps:**
1. Navigate to JavaScript alerts page
2. Set up confirm handler to accept
3. Trigger confirm dialog
4. Verify OK result appears

**Test Coverage:**
- Confirm dialog handling
- Accept action
- Result verification

**Business Value:}
Tests user confirmation flow handling.
""",
)
def test_js_confirm_accept(js_alerts_page, the_internet_config):
    """TC-TI-041: Handle JavaScript confirm - Accept."""

    with allure.step("Navigate to alerts page"):
        js_alerts_page.navigate_to_alerts(the_internet_config.base_url)

    with allure.step("Set up confirm handler and accept"):
        js_alerts_page.page.once("dialog", lambda dialog: dialog.accept())
        js_alerts_page.click_confirm()

    with allure.step("Verify OK result message"):
        result = js_alerts_page.get_result_text()
        assert "You clicked: Ok" in result


@e2e_test(
    epic="The Internet E2E",
    feature="JavaScript Dialogs",
    story="Confirm Dialog",
    testcase="TC-TI-042",
    requirement="US-TI-ALERT-003",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Handle JavaScript confirm - Dismiss",
    link="https://the-internet.herokuapp.com/javascript_alerts",
    description="""
Verify that confirm dialog can be dismissed.

**Test Steps:**
1. Navigate to JavaScript alerts page
2. Set up confirm handler to dismiss
3. Trigger confirm dialog
4. Verify Cancel result appears

**Test Coverage:**
- Confirm dialog handling
- Dismiss action
- Result verification

**Business Value:}
Tests user cancellation flow handling.
""",
)
def test_js_confirm_dismiss(js_alerts_page, the_internet_config):
    """TC-TI-042: Handle JavaScript confirm - Dismiss."""

    with allure.step("Navigate to alerts page"):
        js_alerts_page.navigate_to_alerts(the_internet_config.base_url)

    with allure.step("Set up confirm handler and dismiss"):
        js_alerts_page.page.once("dialog", lambda dialog: dialog.dismiss())
        js_alerts_page.click_confirm()

    with allure.step("Verify Cancel result message"):
        result = js_alerts_page.get_result_text()
        assert "You clicked: Cancel" in result


@e2e_test(
    epic="The Internet E2E",
    feature="JavaScript Dialogs",
    story="Prompt Dialog",
    testcase="TC-TI-043",
    requirement="US-TI-ALERT-004",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Handle JavaScript prompt",
    link="https://the-internet.herokuapp.com/javascript_alerts",
    description="""
Verify that prompt dialog can accept text input.

**Test Steps:**
1. Navigate to JavaScript alerts page
2. Set up prompt handler with test text
3. Trigger prompt dialog
4. Verify entered text appears in result

**Test Coverage:**
- Prompt dialog handling
- Text input in dialogs
- Result verification

**Business Value:}
Tests user input handling in dialog flows.
""",
)
def test_js_prompt(js_alerts_page, the_internet_config):
    """TC-TI-043: Handle JavaScript prompt."""
    test_text = "Hello Playwright"

    with allure.step("Navigate to alerts page"):
        js_alerts_page.navigate_to_alerts(the_internet_config.base_url)

    with allure.step(f"Set up prompt handler with text '{test_text}'"):
        js_alerts_page.page.once("dialog", lambda dialog: dialog.accept(test_text))
        js_alerts_page.click_prompt()

    with allure.step("Verify entered text in result"):
        result = js_alerts_page.get_result_text()
        assert f"You entered: {test_text}" in result
