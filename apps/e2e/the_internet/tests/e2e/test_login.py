"""The Internet Login Tests.

This test suite covers form authentication operations including:
- Successful login with valid credentials
- Login failure with invalid credentials

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("The Internet E2E")
@allure.feature("Authentication")
@allure.story("Form Authentication")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-TI-002")
@pytest.mark.requirement("US-TI-AUTH-001")
@pytest.mark.smoke
@allure.severity(allure.severity_level.CRITICAL)
@allure.description_html(markdown_to_html("""
Verify that a user can successfully log in with valid credentials.

**Test Steps:**
1. Navigate to login page
2. Enter valid username and password
3. Click login button
4. Verify success message appears
5. Verify logout button is visible

**Test Coverage:**
- Successful authentication flow
- Session establishment
- Post-login UI verification

**Business Value:**
Critical user journey for accessing authenticated features.
"""))
def test_login_success(login_page, the_internet_config):
    """TC-TI-002: Test successful login."""
    user = the_internet_config.test_users["default"]

    with allure.step("Navigate to login page"):
        login_page.navigate_to_login(the_internet_config.base_url)

    with allure.step(f"Login with username '{user['username']}'"):
        login_page.login(user["username"], user["password"])

    with allure.step("Verify success message and logout button"):
        assert "You logged into a secure area!" in login_page.get_flash_message()
        expect(login_page.logout_button).to_be_visible()


@allure.epic("The Internet E2E")
@allure.feature("Authentication")
@allure.story("Form Authentication")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-003")
@pytest.mark.requirement("US-TI-AUTH-002")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that login fails with invalid credentials.

**Test Steps:**
1. Navigate to login page
2. Enter invalid username and password
3. Click login button
4. Verify error message appears

**Test Coverage:**
- Invalid credentials handling
- Error message display
- Authentication failure flow

**Business Value:**
Ensures security by rejecting incorrect credentials.
"""))
def test_login_failure(login_page, the_internet_config):
    """TC-TI-003: Test failed login."""

    with allure.step("Navigate to login page"):
        login_page.navigate_to_login(the_internet_config.base_url)

    with allure.step("Attempt login with invalid credentials"):
        login_page.login("wrong", "pass")

    with allure.step("Verify error message"):
        assert "Your username is invalid!" in login_page.get_flash_message()
