"""Sauce Demo Authentication Tests.

This test suite covers user authentication operations including:
- Successful login with valid credentials
- Login failure with invalid password
- Locked out user handling
- Empty credentials validation

Application: https://www.saucedemo.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("Sauce Demo E2E")
@allure.feature("Authentication")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.testcase("TC-SD-001")
@pytest.mark.requirement("US-AUTH-001")
@pytest.mark.smoke
@allure.severity(allure.severity_level.CRITICAL)
@allure.description_html(markdown_to_html("""
Verify that a user can successfully log in with valid credentials.

**Test Steps:**
1. Navigate to login page
2. Enter valid username and password
3. Click login button
4. Verify redirect to inventory page

**Test Coverage:**
- Successful authentication flow
- Post-login redirect verification
- Session establishment

**Business Value:**
Critical user journey for accessing the application.
"""))
def test_successful_login(login_page, inventory_page, sauce_demo_config):
    """TC-SD-001: Successful login with valid credentials."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Navigate to login page"):
        login_page.attach()

    with allure.step(f"Login as user '{user['username']}'"):
        login_page.login(user["username"], user["password"])

    with allure.step("Verify redirect to inventory page"):
        expect(inventory_page.inventory_list).to_be_visible()
        expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")


@allure.epic("Sauce Demo E2E")
@allure.feature("Authentication")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-002")
@pytest.mark.requirement("US-AUTH-002")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that login fails with invalid password.

**Test Steps:**
1. Navigate to login page
2. Enter valid username with invalid password
3. Click login button
4. Verify error message appears

**Test Coverage:**
- Invalid password handling
- Error message display and clarity

**Business Value:**
Ensures security by rejecting incorrect credentials.
"""))
def test_invalid_password(login_page, sauce_demo_config):
    """TC-SD-002: Login fails with invalid password."""
    user = sauce_demo_config.test_users["standard"]

    with allure.step("Navigate to login page"):
        login_page.attach()

    with allure.step("Attempt login with wrong password"):
        login_page.login(user["username"], "wrong_password")

    with allure.step("Verify error message is displayed"):
        error = login_page.get_error_message()
        assert "Username and password do not match" in error


@allure.epic("Sauce Demo E2E")
@allure.feature("Authentication")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-003")
@pytest.mark.requirement("US-AUTH-003")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that a locked out user cannot log in.

**Test Steps:**
1. Navigate to login page
2. Enter locked out user credentials
3. Click login button
4. Verify locked out error message

**Test Coverage:**
- Account lockout handling
- Security policy enforcement

**Business Value:**
Ensures account security policies are properly enforced.
"""))
def test_locked_out_user(login_page, sauce_demo_config):
    """TC-SD-003: Locked out user cannot login."""
    user = sauce_demo_config.test_users["locked"]

    with allure.step("Navigate to login page"):
        login_page.attach()

    with allure.step("Attempt login with locked user"):
        login_page.login(user["username"], user["password"])

    with allure.step("Verify locked out error message"):
        error = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error


@allure.epic("Sauce Demo E2E")
@allure.feature("Authentication")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "sauce_demo")
@pytest.mark.app("sauce_demo")
@pytest.mark.e2e
@pytest.mark.testcase("TC-SD-004")
@pytest.mark.requirement("US-AUTH-004")
@allure.severity(allure.severity_level.NORMAL)
@allure.description_html(markdown_to_html("""
Verify that login fails with empty credentials.

**Test Steps:**
1. Navigate to login page
2. Leave username and password fields empty
3. Click login button
4. Verify validation error appears

**Test Coverage:**
- Empty field validation
- Required field enforcement

**Business Value:**
Ensures proper form validation for required fields.
"""))
def test_empty_credentials(login_page):
    """TC-SD-004: Login fails with empty credentials."""
    with allure.step("Navigate to login page"):
        login_page.attach()

    with allure.step("Attempt login with empty credentials"):
        login_page.login("", "")

    with allure.step("Verify validation error"):
        error = login_page.get_error_message()
        assert "Username is required" in error
