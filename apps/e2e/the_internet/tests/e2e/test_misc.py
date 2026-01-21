"""The Internet Miscellaneous Tests (Uploads, Auth, Forms)."""

import pytest
import allure
from playwright.sync_api import expect
from pathlib import Path
import tempfile


@allure.feature("The Internet")
@allure.story("File Upload")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-060")
def test_file_upload(file_upload_page, the_internet_config):
    """TC-TI-060: Upload a file."""
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test file content")
        test_file_path = f.name
    
    try:
        # Navigate
        file_upload_page.navigate_to_page(the_internet_config.base_url)
        
        # Upload file
        file_upload_page.upload_file(test_file_path)
        
        # Verify filename appears
        filename = Path(test_file_path).name
        uploaded = file_upload_page.get_uploaded_filename()
        assert filename in uploaded
    finally:
        # Cleanup
        Path(test_file_path).unlink(missing_ok=True)


@allure.feature("The Internet")
@allure.story("Authentication")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-001")
def test_basic_auth(basic_auth_page, the_internet_config):
    """TC-TI-001: Basic HTTP authentication."""
    # Get credentials from config
    username = the_internet_config.extra_config.get("basic_auth", {}).get("username", "admin")
    password = the_internet_config.extra_config.get("basic_auth", {}).get("password", "admin")
    
    # Navigate with auth
    basic_auth_page.navigate_with_auth(username, password)
    
    # Verify success message
    message = basic_auth_page.get_message()
    assert "Congratulations" in message


@allure.feature("The Internet")
@allure.story("Authentication")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-004")
def test_logout(login_page, secure_page, the_internet_config):
    """TC-TI-004: Logout functionality."""
    # Login first
    login_page.navigate_to_login(the_internet_config.base_url)
    user = the_internet_config.test_users["default"]
    login_page.login(user["username"], user["password"])
    
    # Logout
    secure_page.logout()
    
    # Verify back on login page
    expect(login_page.page).to_have_url("https://the-internet.herokuapp.com/login")
    expect(login_page.username_input).to_be_visible()


@allure.feature("The Internet")
@allure.story("Form Elements")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
@pytest.mark.testcase("TC-TI-012")
def test_number_input(number_input_page, the_internet_config):
    """TC-TI-012: Number input field with arrow keys."""
    # Navigate
    number_input_page.navigate_to_page(the_internet_config.base_url)
    
    # Enter number
    number_input_page.enter_number("5")
    assert number_input_page.get_value() == "5"
    
    # Increment
    number_input_page.increment()
    assert number_input_page.get_value() == "6"
    
    # Decrement
    number_input_page.decrement()
    assert number_input_page.get_value() == "5"
