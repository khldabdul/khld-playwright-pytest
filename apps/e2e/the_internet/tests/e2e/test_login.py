"""The Internet Login Tests."""

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("The Internet")
@allure.story("Form Authentication")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_login_success(login_page, the_internet_config):
    """Test successful login."""
    # 1. Navigate
    login_page.navigate_to_login(the_internet_config.base_url)
    
    # 2. Login
    user = the_internet_config.test_users["default"]
    login_page.login(user["username"], user["password"])
    
    # 3. Verify
    assert "You logged into a secure area!" in login_page.get_flash_message()
    expect(login_page.logout_button).to_be_visible()

@allure.feature("The Internet")
@allure.story("Form Authentication")
@pytest.mark.app("the_internet")
@pytest.mark.e2e
def test_login_failure(login_page, the_internet_config):
    """Test failed login."""
    # 1. Navigate
    login_page.navigate_to_login(the_internet_config.base_url)
    
    # 2. Login Invalid
    login_page.login("wrong", "pass")
    
    # 3. Verify
    assert "Your username is invalid!" in login_page.get_flash_message()
