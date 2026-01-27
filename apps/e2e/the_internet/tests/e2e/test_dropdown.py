"""The Internet Dropdown Tests.

This test suite covers dropdown selection operations including:
- Selecting options from dropdown
- Verifying selected option

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("The Internet E2E")
@allure.feature("Form Elements")
@allure.story("Dropdown")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-011")
@pytest.mark.requirement("US-TI-FORM-002")
@pytest.mark.smoke
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that dropdown options can be selected.

**Test Steps:**
1. Navigate to dropdown page
2. Select Option 1
3. Verify Option 1 is selected
4. Select Option 2
5. Verify Option 2 is selected

**Test Coverage:**
- Dropdown option selection
- Selected value verification

**Business Value:**
Core UI interaction for form controls and selections.
"""))
def test_dropdown_selection(dropdown_page, the_internet_config):
    """TC-TI-011: Test dropdown selection."""

    with allure.step("Navigate to dropdown page"):
        dropdown_page.navigate_to_dropdown(the_internet_config.base_url)

    with allure.step("Select Option 1 and verify"):
        dropdown_page.select_option("1")
        assert dropdown_page.get_selected_option_text() == "Option 1"

    with allure.step("Select Option 2 and verify"):
        dropdown_page.select_option("2")
        assert dropdown_page.get_selected_option_text() == "Option 2"
