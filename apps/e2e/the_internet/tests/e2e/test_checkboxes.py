"""The Internet Checkboxes Tests.

This test suite covers checkbox interaction operations including:
- Checking and unchecking checkboxes
- Verifying checkbox state

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import e2e_test


@e2e_test(
    epic="The Internet E2E",
    feature="Form Elements",
    story="Checkboxes",
    testcase="TC-TI-010",
    requirement="US-TI-FORM-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    smoke=True,
    title="Checkbox toggle",
    link="https://the-internet.herokuapp.com/",
    description="""
    Verify that checkboxes can be checked and unchecked.

    **Test Steps:**
    1. Navigate to checkboxes page
    2. Toggle checkbox 1 to checked
    3. Toggle checkbox 2 to unchecked
    4. Verify both states

    **Test Coverage:**
    - Checkbox state manipulation
    - State verification after toggle

    **Business Value:**
    Core UI interaction for form controls and settings.
    """,
)
def test_checkboxes(checkboxes_page, the_internet_config):
    """TC-TI-010: Test checkbox interactions."""

    with allure.step("Navigate to checkboxes page"):
        checkboxes_page.navigate_to_checkboxes(the_internet_config.base_url)

    with allure.step("Toggle checkbox 1 to checked"):
        checkboxes_page.toggle_checkbox(0, True)
        assert checkboxes_page.is_checked(0)

    with allure.step("Toggle checkbox 2 to unchecked"):
        checkboxes_page.toggle_checkbox(1, False)
        assert not checkboxes_page.is_checked(1)
