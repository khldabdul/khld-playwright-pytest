"""The Internet Miscellaneous Tests (Uploads, Auth, Forms).

This test suite covers miscellaneous operations including:
- File uploads
- Basic authentication
- Form logout
- Number input controls

Application: https://the-internet.herokuapp.com/
"""

from __future__ import annotations

import pytest
import allure
from playwright.sync_api import expect
from pathlib import Path
import tempfile

from infrastructure.utils.allure_helpers import e2e_test


@allure.epic("The Internet E2E")
@allure.feature("File Operations")
@allure.story("File Upload")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@e2e_test(
    epic="The Internet E2E",
    feature="File Operations",
    story="File Upload",
    testcase="TC-TI-060",
    requirement="US-TI-FILE-001",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Upload a file",
    link="https://the-internet.herokuapp.com/upload",
    description="""
Verify that files can be uploaded via web form.

**Test Steps:**
1. Create a temporary test file
2. Navigate to file upload page
3. Upload the file
4. Verify filename appears on page

**Test Coverage:**
- File upload functionality
- File path handling
- Upload verification

**Business Value:}
Tests file upload capability for document/image handling.
""",
)
def test_file_upload(file_upload_page, the_internet_config):
    """TC-TI-060: Upload a file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test file content")
        test_file_path = f.name

    try:
        with allure.step("Navigate to file upload page"):
            file_upload_page.navigate_to_page(the_internet_config.base_url)

        with allure.step("Upload test file"):
            file_upload_page.upload_file(test_file_path)

        with allure.step("Verify filename appears"):
            filename = Path(test_file_path).name
            uploaded = file_upload_page.get_uploaded_filename()
            assert filename in uploaded
    finally:
        Path(test_file_path).unlink(missing_ok=True)


@allure.epic("The Internet E2E")
@allure.feature("Authentication")
@allure.story("Basic Auth")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@e2e_test(
    epic="The Internet E2E",
    feature="Authentication",
    story="Basic Auth",
    testcase="TC-TI-001",
    requirement="US-TI-AUTH-001",
    app="the_internet",
    severity=allure.severity_level.CRITICAL,
    title="Basic HTTP authentication",
    link="https://the-internet.herokuapp.com/basic_auth",
    description="""
Verify that Basic HTTP authentication works.

**Test Steps:**
1. Get credentials from config
2. Navigate with authentication
3. Verify success message appears

**Test Coverage:**
- Basic HTTP authentication
- Credential handling
- Authenticated content access

**Business Value:}
Tests HTTP authentication flow for protected resources.
""",
    critical=True,
    smoke=True,
)
def test_basic_auth(basic_auth_page, the_internet_config):
    """TC-TI-001: Basic HTTP authentication."""
    username = the_internet_config.extra_config.get("basic_auth", {}).get("username", "admin")
    password = the_internet_config.extra_config.get("basic_auth", {}).get("password", "admin")

    with allure.step(f"Navigate with auth credentials ({username})"):
        basic_auth_page.navigate_with_auth(username, password)

    with allure.step("Verify success message"):
        message = basic_auth_page.get_message()
        assert "Congratulations" in message


@allure.epic("The Internet E2E")
@allure.feature("Authentication")
@allure.story("Logout")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@e2e_test(
    epic="The Internet E2E",
    feature="Authentication",
    story="Logout",
    testcase="TC-TI-004",
    requirement="US-TI-AUTH-003",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Logout functionality",
    link="https://the-internet.herokuapp.com/login",
    description="""
Verify that logout functionality works.

**Test Steps:**
1. Login to the application
2. Click logout button
3. Verify redirect to login page
4. Verify username input is visible

**Test Coverage:**
- Logout functionality
- Session termination
- Post-logout redirect

**Business Value:}
Tests user session management and security.
""",
)
def test_logout(login_page, secure_page, the_internet_config):
    """TC-TI-004: Logout functionality."""
    user = the_internet_config.test_users["default"]

    with allure.step("Login first"):
        login_page.navigate_to_login(the_internet_config.base_url)
        login_page.login(user["username"], user["password"])

    with allure.step("Logout"):
        secure_page.logout()

    with allure.step("Verify back on login page"):
        expect(login_page.page).to_have_url("https://the-internet.herokuapp.com/login")
        expect(login_page.username_input).to_be_visible()


@allure.epic("The Internet E2E")
@allure.feature("Form Elements")
@allure.story("Number Input")
@allure.label("layer", "e2e")
@allure.label("type", "functional")
@allure.label("app", "the_internet")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@e2e_test(
    epic="The Internet E2E",
    feature="Form Elements",
    story="Number Input",
    testcase="TC-TI-012",
    requirement="US-TI-FORM-003",
    app="the_internet",
    severity=allure.severity_level.NORMAL,
    title="Number input field with arrow keys",
    link="https://the-internet.herokuapp.com/inputs",
    description="""
Verify that number input controls work correctly.

**Test Steps:**
1. Navigate to number input page
2. Enter number
3. Verify value
4. Increment using arrow button
5. Verify new value
6. Decrement using arrow button
7. Verify decremented value

**Test Coverage:**
- Number input field
- Arrow button interaction
- Value manipulation

**Business Value:}
Tests numeric input controls and increment/decrement patterns.
""",
)
def test_number_input(number_input_page, the_internet_config):
    """TC-TI-012: Number input field with arrow keys."""

    with allure.step("Navigate to number input page"):
        number_input_page.navigate_to_page(the_internet_config.base_url)

    with allure.step("Enter number and verify"):
        number_input_page.enter_number("5")
        assert number_input_page.get_value() == "5"

    with allure.step("Increment and verify"):
        number_input_page.increment()
        assert number_input_page.get_value() == "6"

    with allure.step("Decrement and verify"):
        number_input_page.decrement()
        assert number_input_page.get_value() == "5"
